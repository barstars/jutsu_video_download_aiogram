import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

class Jutdotsu():
	def __init__(self, url, user):
		self.headers = {
		"Referer":"https://jut.su/",
		"Sec-Ch-Ua":'Not(A:Brand";v="24", "Chromium";v="122"',
		"Sec-Ch-Ua-Mobile":"?0",
		"Sec-Ch-Ua-Platform":"Windows",
		"Upgrade-Insecure-Requests":'1',
		"User-Agent":UserAgent().chrome}
		self.url = url
		self.user = user

	def method_1(self,res):
		video_url = self.url_videos(res)
		print(video_url)
		return self.video_download(video_url)

	def video_download(self,url):
		response = requests.get(url, stream=True, headers=self.headers)
		with open(f"{self.user}/{self.user}.mp4", 'wb') as file:
			for chunk in response.iter_content(chunk_size=(1024**3)):
				file.write(chunk)
		return f"{self.user}/{self.user}.mp4"

	def url_videos(self,res):
		response = requests.get(url=self.url, headers=self.headers)
		soup = BS(response.text, "lxml")

		video_url = soup.find("source", res=res)

		return video_url.get("src")
