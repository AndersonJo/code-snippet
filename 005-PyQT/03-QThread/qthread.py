import sys
from datetime import datetime
from multiprocessing import Process, Queue

import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QStatusBar


def producer(que: Queue):
    for i in range(100000):
        data = ''.join([str(np.random.rand()) for _ in range(20)])
        que.put(data)


class Consumer(QThread):
    poped = pyqtSignal(str)

    def __init__(self, que: Queue):
        super().__init__()
        self.que = que

    def run(self):
        while True:
            if not self.que.empty():
                data = self.que.get()
                self.poped.emit(data)


class MyWindow(QMainWindow):
    def __init__(self, que):
        super().__init__()
        self.setWindowTitle('Test Haha')
        self.setGeometry(200, 200, 300, 200)
        self.statusBar().showMessage('Hello!')
        self.statusBar().setStyleSheet('border:1px solid #333333;')

        self.consumer = Consumer(que)
        self.consumer.poped.connect(self.process_data)
        self.consumer.start()
        self.cnt = 0

    @pyqtSlot(str)
    def process_data(self, data):
        self.cnt += 1
        self.statusBar().showMessage(str(self.cnt))
        if self.cnt >= 100000:
            QCoreApplication.instance().quit()


if __name__ == '__main__':
    start_dt = datetime.now()
    que = Queue()
    p = Process(name='producer', target=producer, args=(que,), daemon=True)
    p.start()

    # Main Application
    app = QApplication(sys.argv)
    window = MyWindow(que)
    window.show()
    app.exec_()

    print((datetime.now() - start_dt).total_seconds())
