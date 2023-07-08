from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6.QtGui import QIcon, QPainter, QPen, QBrush, QColor, QColorConstants, QPolygon
from PyQt6.QtCore import Qt, QRect, QPoint
import geometry

class Window(QWidget):
    def __int__(self):
        super().__int__()

        self.geometry(200,200,400,300)
        self.setWindowTitle("PyQt6 Drawing")
        self.setWindowIcon("face72t.png")


    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColorConstants.Red)
        painter.setPen(pen)
        painter.setBrush(QColor(0,0,240,100))
        points = QPolygon([
            QPoint(10,10),
            QPoint(100,10),
            QPoint(100,100),
            QPoint(10,100)
        ])
        painter.drawPolygon(points)


App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())