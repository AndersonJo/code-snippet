import os
import platform
import re
import sys
from multiprocessing import Process, set_executable
from pprint import pprint


def main():
    print('Main Prefix:', sys.exec_prefix)
    print('Main executable:', sys.executable)
    print('Main Architecture:', platform.architecture())

    # 1) set_excutable을 통해서 실행하려는 vitual environment의 python을 실행
    set_executable(r'C:\Users\anderson\anaconda3\envs\zeta64\python.exe')
    job = Process(target=worker)
    job.daemon = True
    job.start()
    job.join()


def worker():
    # PATH environment 뿐만아니라 sys.path 도 변형해줘야 함
    paths = [re.sub(r'\\zeta', r'\\zeta64', i) for i in os.environ['PATH'].split(';')]
    os.environ['PATH'] = ';'.join(paths)
    sys.path = [re.sub(r'\\zeta', r'\\zeta64', i) for i in sys.path]

    print()
    print('Worker Prefix:', sys.exec_prefix)
    print('Worker executable  :', sys.executable)
    print('Worker Architecture:', platform.architecture())

    import numpy as np
    import lightgbm
    from lightgbm import LGBMClassifier
    LGBMClassifier()
    print('Worker Numpy       :', np.__version__)
    print('Worker LightGBM    :', lightgbm.__version__)


if __name__ == '__main__':
    main()
