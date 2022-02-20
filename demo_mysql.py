# 异步 mysql
# pip install aiomysql

import asyncio
import aiomysql

async def execute():
    print('开始执行')
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='123')
    cur = await conn.cursor()
    await cur.execute('SELECT host,User FROM user')
    result = await cur.fetchall()
    print(result)

    await cur.close()
    conn.close()

# asyncio.run(execute())

task_list = [
    execute('47.93.4.197:6379', 'root!2345'),
    execute('47.93.4.197:6379', 'root!2345')
]

asyncio.run(asyncio.wait(task_list))