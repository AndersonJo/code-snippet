from datetime import datetime
from multiprocessing import get_context, Process
from multiprocessing import Queue
from multiprocessing.shared_memory import SharedMemory
from typing import Optional

from tqdm import tqdm


class SharedQueue:

    def __init__(self, queue: Queue, sq_name=None, shared_size=1024 * 1024 * 8):
        self.queue = queue
        if sq_name is None:
            self.shm = SharedMemory(create=True, size=shared_size)
        else:
            self.shm = SharedMemory(name=sq_name)
        self._shared_size = shared_size - 1
        self._cur_idx = 0

    @property
    def name(self):
        return self.shm.name

    def get(self, block: bool = True, timeout: Optional[float] = None, encoding='euc-kr') -> Optional[bytes]:
        r = self.queue.get(block=block, timeout=timeout)
        if r is None:
            return None

        start, end = r
        return self.shm.buf[start:end].tobytes()

    def put(self, obj: bytes, block: bool = True, timeout: Optional[float] = None):
        start = self._cur_idx
        end = start + len(obj)
        if end >= self._shared_size:
            start, end = 0, len(obj)
        self._cur_idx = end

        self.shm.buf[start:end] = obj
        self.queue.put((start, end), block=block, timeout=timeout)


def daemon_run1(queue: Queue, sq_name: str):
    answer = '{0}안녕하세요 파이썬! 123456789 !@#$%^&*() 하하! 제타벨류 가즈아!'
    cnt = 0

    sq = SharedQueue(queue, sq_name=sq_name)
    while True:
        btext = sq.get()
        try:
            text = btext.decode('euc-kr')
        except UnicodeDecodeError as e:
            print(e)
            print(btext)
            continue

        if text == 'end':
            break
        assert text == answer.format(cnt), f'ERROR: text:{text}'
        cnt += 1


def daemon_run2(queue: Queue):
    answer = '{0}안녕하세요 파이썬! 123456789 !@#$%^&*() 하하! 제타벨류 가즈아!'
    cnt = 0

    while True:
        text = queue.get()
        if text == 'end':
            break
        assert text == answer.format(cnt), f'ERROR: text:{text}'
        cnt += 1


def main():
    s = '{0}안녕하세요 파이썬! 123456789 !@#$%^&*() 하하! 제타벨류 가즈아!'

    # SharedMemoryQueue 테스트
    queue = Queue()
    sq = SharedQueue(queue, shared_size=1024 * 1024 * 128)  # 낮은 값 설정시 에러가 난다
    p = Process(target=daemon_run1, args=(queue, sq.name))
    p.start()

    start = datetime.now()
    for i in tqdm(range(1000000)):
        sq.put(bytes(s.format(i), encoding='euc-kr'), block=False)
    sq.put('end'.encode('euc-kr'), block=True)
    p.join()

    print('SharedQueue:', (datetime.now() - start).total_seconds())

    # 기존 Queue 테스트
    queue = Queue()
    p = Process(target=daemon_run2, args=(queue,))
    p.start()

    start = datetime.now()
    for i in tqdm(range(1000000)):
        queue.put(s.format(i), block=False)
    queue.put('end', block=True)
    p.join()

    print('Queue:', (datetime.now() - start).total_seconds())


if __name__ == '__main__':
    main()
