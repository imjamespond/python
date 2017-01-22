# -*- coding: utf-8 -*- 
'''
Created on 2016年11月28日

@author: metasoft
'''
import tensorflow as tf
import numpy
import math
import os

if __name__ == '__main__':
  tf.logging.set_verbosity(tf.logging.INFO)
  
  weights_ = tf.Variable(tf.truncated_normal([9, 2], stddev=1.0 / math.sqrt(float(3))))
  images_1 = tf.to_float(tf.constant(numpy.array([[1, 2, 3, 4, 5, 6 ,7, 8, 9]])), "img1")
  images_2 = tf.to_float(tf.constant(numpy.array([[9, 8, 7, 6, 5, 4, 3, 2, 1]])), "img2")
  
  matmul_ = tf.matmul(images_1, weights_)
  relu_ = tf.nn.relu(matmul_)
  softmax_matmul_ = tf.nn.softmax(matmul_)
  labels = tf.to_int64(tf.constant(numpy.array([1,2])))
  cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(matmul_, labels, name='xentropy')
  loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')#计算交叉熵
  optimizer = tf.train.GradientDescentOptimizer(0.5)
  train = optimizer.minimize(loss)
  
  init_op = tf.initialize_all_variables()
  
  with tf.Session() as sess:
    sess.run(init_op)
    #print sess.run([weights_])
    print sess.run([matmul_])
    #print sess.run([softmax_matmul_])
    print sess.run(relu_)
    '''
    for step in xrange(100):
      sess.run(train)
      if step % 20 == 0:
        print(step, sess.run(weights_))'''
        