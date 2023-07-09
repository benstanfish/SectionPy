import numpy
from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6.QtGui import QIcon, QPainter, QPen, QBrush, QColor, QColorConstants, QPolygon
from PyQt6.QtCore import Qt, QRect, QPoint
from math import pi, radians
import geometry as gm

class Window(QWidget):
    def __int__(self):
        super().__int__()
        self.geometry(200,200,400,300)
        self.setWindowTitle("PyQt6 Drawing")


    def paintEvent(self, event):
        painter = QPainter(self)
        # qp = QPolygon()
        # qp.append(QPoint(10,20))
        # qp.append(QPoint(50,30))
        # qp.append(QPoint(70,20))
        # painter.drawPolygon(qp)

        # circ = gm.close_polygon(gm.circle_points(50))
        # circ = gm.translate(circ,numpy.array([300,300]))
        # qp = QPolygon()
        # print(circ.shape[0])
        # for i in range(0,circ.shape[0]):
        #     qp.append(QPoint(circ[i][0],circ[i][1]))
        # painter.drawPolygon(qp)

        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor(30,144,255))

        circ = gm.close_polygon(gm.circle_points(50,30,3*pi/2))
        circ = gm.rotate(circ, radians(0))
        circ = gm.translate(circ,numpy.array([300,150]))
        qp = gm.getQPolygon(circ)


        painter.setPen(pen)
        painter.setBrush(QColor(30,144,255,150))
        painter.drawPolygon(qp)

        painter.drawEllipse(100,100,100,100)


App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())