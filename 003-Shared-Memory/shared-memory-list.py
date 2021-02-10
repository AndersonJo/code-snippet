from multiprocessing.shared_memory import ShareableList
import numpy as np
from multiprocessing import Process


def daemon_run(name):
    a = ShareableList(name=name)
    data = np.array(a)
    print(f'[Processor] data: {data[:4]} | size: {len(data)}')  # [Processor] data: [255  11   0 100] | size: 4096
    for i, v in enumerate(['def', -9999999999, 0.123456789123456, 8889999]):
        a[i] = v


def main():
    # Shared Memory 생성
    a = ShareableList(['abc', 9999999, -100, 0.123456789])

    p = Process(target=daemon_run, args=(a.shm.name,))  # 프로세서를 열고, shared memory 를 읽어서 출력한다.
    p.start()
    p.join()

    data = np.array(a)
    print(f'[Main]      data: {data[:4]} | size: {len(a)}')  # [Main]      data: [1 2 3 4] | size: 10


if __name__ == '__main__':
    main()
