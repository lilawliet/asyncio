import asyncio
import uvloop

# asyncio事件循环的替代方案。 效率 > 默认 asyncio 事件循环
# 这句代码会实现事件循环替换
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 后面代码照常编写