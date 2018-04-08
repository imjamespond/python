# -*- coding: utf-8 -*- 
'''
Created on 2017年2月17日

@author: metasoft
'''
from PyQt5 import QtWidgets
from codechiev.painter import Painter
import codechiev.mnist_conv as mnist

if __name__ == '__main__':
  import sys
  app = QtWidgets.QApplication(sys.argv)
  painter = Painter()
  painter.learn = mnist.learn
  painter.identify = mnist.identify
  painter.trainExample = mnist.trainExample
  sys.exit(app.exec_())