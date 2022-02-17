import time
import asyncio
import concurrent.futures

# 基于 协程异步编程 + Mysql(不支持协程，线程/进程异步编程)

def func1():
	time.sleep(2)
	return 'func1'

async def main():
	loop = asyncio.get_running_loop()

	# 第一步： 内部先调用 ThreadPoolExecutor 的 submit 方法去线程池中申请一个线程执行 func1 ，并返回
	# concurrent.futures.Future 对象
	# 第二步： 调用 asyncio.wrap_future 将 concurrent.futures.Future 对象包装为 asycio.Future 对象，
	# 因为 concurrent.futures.Future 对象不支持 await 语法，所以需要包装为 asycio.Future 对象才能使用
	fut = loop.run_in_executor(None, func1)
	result = await fut
	print('default thread pool', result)

asyncio.run( main())