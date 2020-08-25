import sys
from typing import Optional

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *


class WidgetGallery(QDialog):

    def __init__(self, parent: Optional[QObject] = None):
        super(WidgetGallery, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())
