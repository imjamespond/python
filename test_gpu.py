# -*- coding: utf-8 -*-
'''
Created on 2017年2月17日

@author: codechiev
'''

import tensorflow as tf

def getAB():
  a = tf.placeholder(tf.int32, shape=[2])
  b = tf.placeholder(tf.int32, shape=[2])
  return a,b

graph = tf.Graph()

with graph.as_default():
  a,b = getAB()

  with tf.device('/gpu:0'):
    c = tf.constant([3,4], tf.int32)
    sumABC = a+b+c
  sumAB = a + b
    

with tf.Session(graph=graph) as session:
  init_op = tf.global_variables_initializer()
  session.run(init_op)
  print(session.run(sumAB, {a:[1,2], b:[2,3]}))
  print(session.run(sumABC, {a:[1,2], b:[2,3]}))