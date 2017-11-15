# -*- coding: utf-8 -*- 
'''
Created on 2016年11月28日

@author: metasoft
'''
import tensorflow as tf
import numpy as np

arr1 = [i for i in range(10)]
print(arr1)
print(arr1[5:])
print(arr1[1:2])
print(arr1[:2])

arr2 = ["one", "two"]
pairs = [(x, arr2[i]) for i,x in enumerate(arr1[:2])]
print(dict(pairs))