# 协程

aiohttp 异步爬虫框架

协程：部署操作系统提供的，是认为创造的用户态上下文切换技术。（用一个线程在代码间切换游走）

实现方法：
* greeniet、早期
* yield 关键字
* asyncio装饰器 （py3.4)
* async、await 关键字 （py3.5)


协程意义：在一个线程中减少IO等待时间，利用空闲时间做点别的事

协程函数 async def 函数名
协程对象 执行 协程函数() 得到的协程对象

```
import asyncio

async def func():
    print('abc')

result = func()

# 3.7 之前
# loop = asyncio.get_event_loop()
# loop.run_until_complete(result)  # 协程函数代码，必须要写成对象交给循环来处理

# 3.7 之后
asyncio.run(result)
```

**await** + 可等待对象：

* 协程对象
* Future
* Task对象->IO等待
```
# 示例1
import asyncio

async def func():
    print('开始')
    response = await asyncio.sleep(2)
    print('结束', response)
    
asyncio.run( func())
```
```
# 示例2
import asyncio

async def others():
    print('start')
    await asyncio.sleep(2)
    print('end')
    return '返回量'
    
async def func():
    print('协程内部代码')
    response = await others()
    print('IO请求结束，结果为', response)

asyncio.run( func())
```
```
# 示例3
import asyncio

async def others():
    print('start')
    await asyncio.sleep(2)
    print('end')
    return '返回量'
    
async def func():
    print('协程内部代码')
    response1 = await others()
    print('IO请求结束，结果为', response1)
    response2 = await others()
    print('IO请求结束，结果为', response2)

asyncio.run( func())
```

**Task对象**
在事件循环中添加多个任务(py3.7)
立即将某个任务放入事件循环
```
# 示例
import asyncio

async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return '返回值'
    
async def main():
    print('main开始')
    
    task1 = asyncio.create_task(func())
    task2 = asyncio.create_task(func())
    
    print('main结束')
    
    ret1 = await task1
    ret2 = await task2
    print(ret1, ret2)
    
asyncio.run(main())
```
```
示例2
import asyncio

async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return '返回值'
    
async def main():
    print('main开始')
    
    task_list = [
        asyncio.create_task(func(), name='t1'),
        asyncio.create_task(func(), name='t2')
    ]
    
    print('main结束')
    # done 就是任务返回值集合
    done, pending = await asyncio.wait(task_list, timeout=None)
    print(done)
    
asyncio.run(main())
```

**future**
Task继承Future, Task对象内部await结果的处理基于Future对象来的。
```
import asyncio

async def set_after(fut):
    await asyncio.sleep(2)
    fut.set_result('555')
    
async def main():
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    
    await loop.create_task( set_after(fut))
    
    data = await fut
    print(data)
    
asyncio.run( main())
```
**concurrent.futures.Future对象**
使用线程池、**进程池**实现异步操作
```
import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor

def func(value):
    time.sleep(1)
    print(value)
    return 123
    
# 创建线程池
pool = ThreadPoolExecutor(max_workers=5)

for i in range(10):
    fut = pool.submit(func, i)
    print(fut)
```
```
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
```
**异步迭代器**
实现了 __aiter__() 和 __anext__() 方法的对象， __anext__ 必须返回一个 awaitable 对象。 async_for 会处理异步迭代器的 __anext__() 方法所返回的可等待对象，直到其引发一个 StopAsyncIteration 异常。由 PEP492 引入。
**异步可迭代对象**
可在 async_for 语句中被使用的对象。必须通过它的 __aiter__() 方法返回一个 asynchronous_iterator 。由 PEP492引入。
```
import asyncio

class Reader(object):
	"""自定义异步迭代器，同时也是异步可迭代对象"""
	def __init__(self):
		self.count = 0

	async def readline(self):
		# await asyncio.sleep(1)
		self.count += 1
		if self.count == 100:
			return None
		return self.count

	def __aiter__(self):
		return self 

	async def __anext__(self):
		val = await self.readline()
		if val == None:
			raise StopAsyncIteration
		return val

async def func():
	obj = Reader()	
	async for item in obj:  # async 语句必须写在 async 函数中
		print(item)

asyncio.run(func())
```
**异步上下文管理**
此种对象定义了 __aenter__() 和 __aexit__() 方法来对 async_with 语句中的环境进行控制，由 PEP492 引入
```
import asyncio

# 异步上下文管理器
class AsyncContextManager:
	def __init__(self, conn):
		self.conn = conn

	async def do_something(self):
		# 协程操作数据库
		return 666

	async def __aenter__(self):
		# 异步连接数据库
		# self.conn = await asyncio.sleep(1)
		return self

	async def __aexit__(self, exc_type, exc, tb):
		await asyncio.sleep(1)

async def func():
	async with AsyncContextManager() as f:
		result = await f.do_something()
		print(result)

asyncio.run(func())
```

**uvloop**
asyncio事件循环的替代方案。 效率 > 默认 asyncio 事件循环
pip install uvloop
```
import asyncio
import uvloop

# asyncio事件循环的替代方案。 效率 > 默认 asyncio 事件循环
# 这句代码会实现事件循环替换
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 后面代码照常编写
```
* asgi 异步框架快 -> uvicorn 底层 -> uvloop

