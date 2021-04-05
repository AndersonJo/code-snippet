from multiprocessing.shared_memory import SharedMemory
import numpy as np
from multiprocessing import Process


def daemon_run(name):
    shm = SharedMemory(name=name)
    data = np.array(shm.buf)
    print(f'[Processor] data: {data[:4]} | size: {len(data)}')  # [Processor] data: [255  11   0 100] | size: 4096
    shm.buf[:4] = bytearray([1, 2, 3, 4])


def main():
    # Shared Memory 생성
    shm = SharedMemory(create=True, size=1024*1024*8)
    shm.buf[:4] = bytearray([255, 11, 0, 100])  # 값은 [0~256) 사이의 값만 가능

    p = Process(target=daemon_run, args=(shm.name,))  # 프로세서를 열고, shared memory 를 읽어서 출력한다.
    p.start()
    p.join()

    data = np.array(shm.buf)
    print(f'[Main]      data: {data[:4]} | size: {len(shm.buf)}')  # [Main]      data: [1 2 3 4] | size: 10

    import ipdb
    ipdb.set_trace()


if __name__ == '__main__':
    main()
