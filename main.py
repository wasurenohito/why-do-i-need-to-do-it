from PIL import Image, ImageDraw
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QPushButton, QMenuBar, QStatusBar
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from random import randint
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(813, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.image = QLabel(self.centralwidget)
        self.image.setObjectName(u"image")
        self.image.setGeometry(QRect(10, 0, 791, 521))
        self.circle_btn = QPushButton(self.centralwidget)
        self.circle_btn.setObjectName(u"circle_btn")
        self.circle_btn.setGeometry(QRect(10, 530, 791, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 813, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.image.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.circle_btn.setText(QCoreApplication.translate("MainWindow", u"yellow circle 💀", None))
    # retranslateUi


class BaseWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.img = None
        self.setupUi(self)
        self.img_size = (self.image.size().width(), self.image.size().height())
        self.circle_btn.clicked.connect(self.circle)

    def update_image(self):
        self.pixmap = pil2pixmap(self.img)
        self.image.setPixmap(self.pixmap)
    
    def circle(self):
        self.img = Image.new('RGB', self.img_size, 'white')
        
        d = ImageDraw.Draw(self.img)
        r = randint(10, 40)
        x, y = (
            randint(0, self.img_size[0] - r),
            randint(0, self.img_size[1] - r)
        )
        d.ellipse((
            (x - r, y - r),
            (x + r, y + r)
        ), (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.update_image()


def pil2pixmap(im: Image.Image) -> QPixmap:
    '''Converts PIL.Image to QtGui.QPixmap'''

    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif  im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")

    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BaseWindow()
    ex.show()
    sys.exit(app.exec())