from multiprocessing.shared_memory import SharedMemory
import numpy as np
from multiprocessing import Process


def daemon_run(in_name, out_name):
    in_shm = SharedMemory(name=in_name)
    out_shm = SharedMemory(name=out_name)
    xb = in_shm.buf[:1024].tobytes()
    text = xb.decode('euc-kr').strip()
    print(f'[Processor] data: {text} | byte: {len(xb)}')  # [Processor] data: [255  11   0 100] | size: 4096
    assert text == '한글1234 ABC %^&'

    xb = '프로세서에서 리턴된 스트링 1234!'.encode('euc-kr')
    out_shm.buf[:len(xb)] = xb


def main():
    # Shared Memory 생성
    shm1 = SharedMemory(create=True, size=1024 * 1024 * 64)
    shm2 = SharedMemory(create=True, size=1024 * 1024 * 64)

    shm1.buf[:] = (' ' * len(shm1.buf)).encode('euc-kr')
    shm2.buf[:] = (' ' * len(shm2.buf)).encode('euc-kr')

    x = '한글1234 ABC %^&'
    xb = x.encode('euc-kr')
    shm1.buf[:len(xb)] = xb  # 값은 [0~256) 사이의 값만 가능
    p = Process(target=daemon_run, args=(shm1.name, shm2.name))  # 프로세서를 열고, shared memory 를 읽어서 출력한다.
    p.start()

    ob = shm2.buf[:1024].tobytes()
    text = ob.decode('euc-kr').strip()
    print(f'[Main     ] data: {text} | byte: {len(ob)}')  # [Main]      data: [1 2 3 4] | size: 10

    assert text == '프로세서에서 리턴된 스트링 1234!'

    shm1.close()
    shm2.close()
    p.join()


if __name__ == '__main__':
    main()
