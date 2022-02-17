import asyncio
import requests

async def download(url):
	print('开始下载 ', url)

	loop = asyncio.get_event_loop()
	# 线程池
	future = loop.run_in_executor(None, requests.get, url)

	response = await future
	print('下载完成')

	file_name = url.rsplit('_')[-1]
	with open(file_name, mode='wb') as file_object:
		file_object.write(response.content)

if __name__ == '__main__':
	url_list = [
	]

	tasks = [download(url) for url in url_list]

	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))

