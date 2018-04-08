'''
Created on 2017年2月17日

@author: metasoft
'''
from PyQt5 import QtWidgets,QtCore,QtGui
from six.moves import xrange 
import numpy as np

class Painter(QtWidgets.QWidget):
    '''
    classdocs
    '''
    
    lastPoint = QtCore.QPoint()
    penColor = QtCore.Qt.white
    learn = None
    identify = None
    trainExample = None
    
    labelInput = None
    
    def drawLineTo(self, endPoint):
      painter = QtGui.QPainter()
      painter.begin(self.image)
      painter.setPen(QtGui.QPen(self.penColor, 30,#QtGui.QColor(255,0,0)
          QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
      painter.drawLine(self.lastPoint, endPoint)
      painter.end()
      self.lastPoint = QtCore.QPoint(endPoint)
      self.update()
    
    def mousePressEvent(self, event):
      self.lastPoint = QtCore.QPoint(event.pos())
    def mouseMoveEvent(self, event):
      self.drawLineTo(event.pos())
    def mouseReleaseEvent(self, event):
      self.drawLineTo(event.pos())
    def paintEvent(self, event):
      painter = QtGui.QPainter(self)
      painter.drawImage(event.rect(), self.image)
      
    def onClear(self):
      self.image.fill(QtGui.qRgb(0, 0, 0))
      self.update()
    def onLearn(self):
      label = self.labelInput.text()
      if(self.learn is not None and len(label) ):
        print("label", label)
        self.learn(self.getImage(), int(label))   
    def onIdentify(self,image):
      if(self.identify is not None ):
        self.identify(self.getImage())   
    def onPickColor(self):
      newColor = QtWidgets.QColorDialog.getColor(self.penColor)
      if newColor.isValid():
        self.penColor = newColor
    def onTrainExample(self):
      if(self.trainExample is not None ):
        self.trainExample()   
        
    def getImage(self):
      newImage = QtGui.QImage(self.image.size(), QtGui.QImage.Format_RGB32)
      painter = QtGui.QPainter()
      painter.begin(newImage)
      painter.drawImage(QtCore.QPoint(0, 0), self.image)
      painter.end()
      newImage = newImage.scaled(28, 28, QtCore.Qt.KeepAspectRatio)
      imgData = []
      for h in xrange(newImage.height()):
        for w in xrange(newImage.width()):
          pixel = newImage.pixel(w, h)   
          imgData.append( QtGui.qGray(pixel)/255 )
      newImage.save("test.png", 'png')
      return imgData
    def getRightTo(self, widget, margin):
      return widget.x()+widget.width()+margin

    def __init__(self):
        '''
        Constructor
        '''
        super(Painter, self).__init__()
        self.resize(400, 400)
        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
        self.onClear()
        
        btn1 = QtWidgets.QPushButton("clear")
        btn2 = QtWidgets.QPushButton("learn")
        btn3 = QtWidgets.QPushButton("identify")
        btn4 = QtWidgets.QPushButton("pen color")
        btn5 = QtWidgets.QPushButton("train")
        label1 = QtWidgets.QLabel("foobar")
        input1 = QtWidgets.QLineEdit()
        self.labelInput = input1
        btn1.setMaximumSize(50, 20)
        btn2.setMaximumSize(50, 20)
        btn3.setMaximumSize(50, 20)
        btn4.setMaximumSize(60, 20)
        btn5.setMaximumSize(50, 20)
        input1.setMaximumSize(30, 20)
        btn1.clicked.connect(self.onClear) 
        btn2.clicked.connect(self.onLearn) 
        btn3.clicked.connect(self.onIdentify) 
        btn4.clicked.connect(self.onPickColor) 
        btn5.clicked.connect(self.onTrainExample) 
      
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(btn1,0, 0,1,1,  QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeft)
        
        self.setLayout(mainLayout)
        self.show()
        
        input1.move(QtCore.QPoint(10,5))
        input1.setParent(self)
        input1.show()
        btn2.move(QtCore.QPoint(self.getRightTo(input1,10),5))
        btn2.setParent(self)
        btn2.show()
        btn3.move(QtCore.QPoint(self.getRightTo(btn2,10),5))
        btn3.setParent(self)
        btn3.show()
        btn4.move(QtCore.QPoint(self.getRightTo(btn3,10),5))
        btn4.setParent(self)
        btn4.show()
        btn5.move(QtCore.QPoint(self.getRightTo(btn4,10),5))
        btn5.setParent(self)
        btn5.show()