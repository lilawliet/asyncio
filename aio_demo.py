import aiohttp
import asyncio

async def fetch(session, url):
	print('发送请求：', url)
	async with session.get(url, verify_ssl=False) as response:
		content = await response.content.read()
		file_name = url.rsplit('_')[-1]
		with open(file_name, mode='wb') as file_object:
			file_object.write(content)
		print('下载完成', url)

async def main():
	async with aiohttp.ClientSession() as session:
		url_list = [
		'https://i0.hdslb.com/bfs/sycp/creative_img/202202/a27c9d162fc2ea7fed32b2cded4f2295.jpg',
		'https://i0.hdslb.com/bfs/feed-admin/44a40db955336e480c1c9089229ce04fe7ef1e47.jpg@336w_190h_1c.webp',
		'https://i0.hdslb.com/bfs/sycp/creative_img/202112/dc57cedccfe9af17f60ef2fd1dcc45ad.jpg'
		]
		tasks = [asyncio.create_task(fetch(session, url)) for url in url_list]

		await asyncio.wait(tasks)


if __name__ == '__main__':
	asyncio.run(main())