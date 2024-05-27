from aiogram import Bot, Dispatcher, executor, types
from respons import Jutdotsu
import os
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Инициализация бота
bot = Bot('5653379571:AAHxBnsmvFSdr8Iq7P_iof7-nlIGOIL2WTU')
dp = Dispatcher(bot)

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


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
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

@dp.message_handler(content_types=['text'])
async def send_video(message: types.Message):
    try:
        userid = str(message.chat.id)
        if not os.path.exists(userid):
            os.makedirs(userid)
        else:
            os.remove(userid)
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
                    with open(f"{userid}/{i}", 'rb') as video_file:
                        await message.answer_video(video_file)

            await message.answer("Видео успешно отправлено.")

            # Удаляем файл после отправки
            os.remove(userid)
        except Exception as e:
            await message.answer(f"Произошла ошибка при отправке видео: {e}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    

executor.start_polling(dp)
