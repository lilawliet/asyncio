# 异步 redis
# pip install aioredis

import asyncio
import aioredis

async def execute(address, password):
    print('开始执行', address)
    redis = await aioredis.create_redis(address, password=password)

    await redis.hmset_dict('car', key1=1, key2=2, key3=3)

    result = await redis.hgetall('car', encoding='utf-8')
    print(result)

    redis.close()
    await redis.wait_closed()
    print('结束', address)

task_list = [
    execute('redis://47.93.4.197:6379', 'root!2345'),
    execute('redis://47.93.4.197:6379', 'root!2345')
]

asyncio.run(asyncio.wait(task_list))