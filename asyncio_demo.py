import asyncio

# 遇到 IO 阻塞自动切换

@asyncio.coroutine
def func1():
	print(1)
	yield from asyncio.sleep(2)
	print(2)

@asyncio.coroutine
def func2():
	print(3)
	yield from asyncio.sleep(2)
	print(4)



if __name__ == '__main__':
	tasks = [
		asyncio.ensure_future(func1()),
		asyncio.ensure_future(func2())
	]

	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))