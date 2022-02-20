import os
import threading
import time

def sing(num):
    thread = threading.current_thread() # 获取当前线程
    print(thread)
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
    st = threading.Thread(target=sing, args=(2,))
    # st = threading.Thread(target=sing, args=(2,))
    dt = threading.Thread(target=dance, kwargs={'num':3}, daemon=True)

    st.setDaemon(True) # 将子进程设置成守护进程，主进程结束则子进程自动销毁

    '''
        必须要将所有子线程设置成守护线程，主线程结束才能全部结束
    '''
    st.start()
    dt.start()

    time.sleep(1)
    print('主线程结束')