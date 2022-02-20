:mport asyncio

from sys import maxsize
import uvicorn
import aioredis
from aioredis import Redis
from fastapi import FastAPI

app = FastAPI()

REDIS_POOL = aioredis.ConnectionsPool('redis://127.0.0.1:6379', password='root123', minsize=1, maxsize=10)

@app.get('/')
def index():
    return {'messsage', 'hello world'}

@app.get('/red')
async def red():
    await asyncio.sleep(3)

    conn = await REDIS_POOL.acquire()
    redis = Redis(conn)

    await redis.hmset_dict('car', key1=1, key2=2)

    result = await redis.hgetall('car', encoding='utf-8')
    REDIS_POOL.release(conn)

    return result

if __name__ == '__main__':
    uvicorn.run('demo_fastapi:app', host='127.0.0.1', port=5000, log_level='info')