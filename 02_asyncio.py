import asyncio

async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return '返回值'

task_list = [
    func(),
    func()
]
    
done, pending = asyncio.run(asyncio.wait(task_list))
print(done)