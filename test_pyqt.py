'''
Created on 2016/11/28

@author: metasoft
'''
from PyQt5 import QtWidgets,QtCore,QtGui
from six.moves import xrange 
import numpy as np

window = None
lastPoint = QtCore.QPoint()
penColor = QtCore.Qt.red

def drawLineTo(endPoint):
  global lastPoint
  painter = QtGui.QPainter()
  painter.begin(window.image)
  painter.setPen(QtGui.QPen(penColor, 30,#QtGui.QColor(255,0,0)
      QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
  painter.drawLine(lastPoint, endPoint)
  painter.end()
  lastPoint = QtCore.QPoint(endPoint)
  window.update()

def mousePressEvent( event):
  global lastPoint
  lastPoint = QtCore.QPoint(event.pos())
def mouseMoveEvent( event):
  drawLineTo(event.pos())
def mouseReleaseEvent( event):
  drawLineTo(event.pos())
def paintEvent( event):
  painter = QtGui.QPainter(window)
  painter.drawImage(event.rect(), window.image)
def onClear():
  window.image.fill(QtGui.qRgb(0, 0, 0))
  window.update()
def onLearn():
  newImage = QtGui.QImage(window.image.size(), QtGui.QImage.Format_RGB32)
  painter = QtGui.QPainter()
  painter.begin(newImage)
  painter.drawImage(QtCore.QPoint(0, 0), window.image)
  painter.end()
  newImage = newImage.scaled(28, 28, QtCore.Qt.KeepAspectRatio)
  imgData = []
  for h in xrange(newImage.height()):
    row = []
    for w in xrange(newImage.width()):
      pixel = newImage.pixel(w, h)   
      row.append( QtGui.qGray(pixel) )
    imgData.append(row)
  print("pixel", np.array(imgData))
  newImage.save("test.png", 'png')
  
def onIdentify():
  return
def onPickColor():
  global penColor
  newColor = QtWidgets.QColorDialog.getColor(penColor)
  if newColor.isValid():
    penColor = newColor
    
def getRightTo(widget, margin):
  return widget.x()+widget.width()+margin

if __name__ == '__main__':

  import sys
  app = QtWidgets.QApplication(sys.argv)
  window = QtWidgets.QWidget()
  window.resize(400, 300)
  window.image = QtGui.QImage(QtCore.QSize(400, 300), QtGui.QImage.Format_RGB32)
  
  window.mousePressEvent = mousePressEvent
  window.mouseMoveEvent = mouseMoveEvent
  window.mouseReleaseEvent = mouseReleaseEvent
  window.paintEvent = paintEvent
  
  btn1 = QtWidgets.QPushButton("clear")
  btn2 = QtWidgets.QPushButton("learn")
  btn3 = QtWidgets.QPushButton("identify")
  btn4 = QtWidgets.QPushButton("pen color")
  label1 = QtWidgets.QLabel("foobar")
  input1 = QtWidgets.QLineEdit()
  btn1.setMaximumSize(60, 20)
  btn2.setMaximumSize(60, 20)
  btn3.setMaximumSize(60, 20)
  btn4.setMaximumSize(60, 20)
  input1.setMaximumSize(30, 20)
  btn1.clicked.connect(onClear) 
  btn2.clicked.connect(onLearn) 
  btn3.clicked.connect(onIdentify) 
  btn4.clicked.connect(onPickColor) 

  mainLayout = QtWidgets.QGridLayout()
  mainLayout.addWidget(btn1,0, 0,1,1,  QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeft)
  
  window.setLayout(mainLayout)
  window.show()
  
  input1.move(QtCore.QPoint(10,5))
  input1.setParent(window)
  input1.show()
  btn2.move(QtCore.QPoint(getRightTo(input1,10),5))
  btn2.setParent(window)
  btn2.show()
  btn3.move(QtCore.QPoint(getRightTo(btn2,10),5))
  btn3.setParent(window)
  btn3.show()
  btn4.move(QtCore.QPoint(getRightTo(btn3,10),5))
  btn4.setParent(window)
  btn4.show()


  
  sys.exit(app.exec_())
  
  '''
  painter = QtGui.QPainter(window.image)
  painter.setPen(QtCore.Qt.blue)
  painter.setFont(QtGui.QFont("Arial", 30))
  painter.drawText(QtCore.QPoint(0,10), "aaaaaaaaaaaaaaaaaaaaaaa")
  window.update()
  '''
