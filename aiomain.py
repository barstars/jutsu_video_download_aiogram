from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.types.input_file import FSInputFile

from respons import Jutdotsu
import os
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import shutil
import asyncio

# Инициализация бота
bot = Bot('TOKEN')
dp = Dispatcher()

# ID пользователя, которому вы хотите отправить видео
#userid = 5713655983

def split_video(video_path, userid, res):
    video = VideoFileClip(video_path)
    total_duration = video.duration
    if res == "360":
        end_time_old = 900
    elif res == "480":
        end_time_old = 600
    elif res == "720":
        end_time_old = 300
    elif res == "1080":
        end_time_old = 100

    start_time = 0
    i = 0
    while start_time < total_duration:
        end_time = start_time + end_time_old
        i += 1
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=f"{userid}/{str(i)}_{start_time}_{end_time}.mp4")
        #os.remove(f'{userid}/cut.mp4')
        start_time = end_time


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("""Первый страка это метод:
1: это url прямого видео
второй строка url(url и метод должны совпадать)
качества видео:
    360
    480
    720
    1080
Например:
1
https://jut.su/shingekii-no-kyojin/season-1/episode-1.html
360""")

@dp.message()
async def send_video(message: Message):
    try:
        userid = str(message.chat.id)
        if os.path.exists(userid):
            shutil.rmtree(userid)
        os.makedirs(userid)
        method, url, res = (message.text).split("\n")
        try:
            await message.answer("Видео скачивается.")
            resp = Jutdotsu(url, userid)
            local_video_path = getattr(resp, f'method_{method}')(res)

            await message.answer("Скачивание завершено. Вырезается видео.")
            video_chunks = split_video(local_video_path, userid, res)
            await message.answer("Видео успешно вырезано. Видео отправляется.")
            for i in os.listdir(userid):
                if i != f"{userid}.mp4":
                    video_input = FSInputFile(path=f"{userid}/{i}")
                    await bot.send_video(chat_id=message.chat.id, video=video_input)

            await message.answer("Видео успешно отправлено.")

            # Удаляем файл после отправки
            shutil.rmtree(userid)
        except Exception as e:
            await message.answer(f"Произошла ошибка при отправке видео: {e}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())
