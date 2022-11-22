from PIL import Image, ImageDraw
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from random import randint
import sys


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.img = None
        self.initUI()

    def initUI(self):
        uic.loadUi('./UI.ui', self)
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
        ), 'yellow')
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