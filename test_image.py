'''
Created on 2016/11/28

@author: metasoft
'''
import numpy as np
import PIL.Image as Image
if __name__ == '__main__':
  a = np.arange(6).reshape((3, 2))
  print(a)
  image = Image.open("img/2-1.png")
  image = image.resize((16,16))
  print(image)
  image = np.array(image)
  print(image)
  arr = []
  arr.append(image)
  arr = np.array(arr)
  print(arr)
  arr = arr.reshape(1,256)
  print(arr)