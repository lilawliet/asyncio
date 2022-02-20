import os
import multiprocessing
import time

def sing(num):
    for i in range(1, 10):
        print(i, '唱歌', num, os.getpid(), os.getppid())
        time.sleep(0.5)
    print('sing 结束')

def dance(num):
    for i in range(1, 10):
        print(i, '跳舞', num, os.getpid(), os.getppid())
        time.sleep(0.5)
    print('dance 结束')


if __name__ == '__main__':
    sp = multiprocessing.Process(target=sing, args=(2,))
    dp = multiprocessing.Process(target=dance, kwargs={'num':3})

    sp.daemon = True # 将子进程设置成守护进程，主进程结束则子进程自动销毁

    sp.start()
    dp.start()

    time.sleep(1)
    print('主进程结束')