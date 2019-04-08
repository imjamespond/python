# -*- coding: utf-8 -*- 
'''
Created on 2016年11月28日 
'''
import numpy as np

random_choice = lambda: np.random.choice(list('0123456789')) # size Default is None, in which case a single value is returned.
print(random_choice())
random_randint = [random_choice() for i in range(np.random.randint(1, 3 + 1))] 
print(random_randint)

arr1 = [i for i in range(10)]
print(arr1)
print(arr1[5:])
print(arr1[1:2])
print(arr1[:2])

arr2 = ["one", "two"]
pairs = [(x, arr2[i]) for i,x in enumerate(arr1[:2])]
print(dict(pairs))