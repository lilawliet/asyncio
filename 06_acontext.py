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