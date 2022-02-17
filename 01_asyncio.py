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