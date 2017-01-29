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
  #一张图4个像素,每个像素对应10个维度证据
  weights_ = tf.Variable(tf.truncated_normal([4, 10], stddev=1.0 / math.sqrt(float(3))))
  bias_ = tf.Variable(tf.zeros([10]), name='biases')
  #一张图4个像素,batch为3即3行,对应3个lable
  batch_images = tf.to_float(tf.constant([[1, 0, 1, 0], [ 1 ,1, 0, 0], [ 0 ,1, 1, 0]]), "batch_img")
  
  matmul_ = tf.matmul(batch_images, weights_)
  relu_ = tf.nn.relu(matmul_+bias_)
  #指数归一,分别分配机率给几个不同物体之一的模型
  softmax_matmul_ = tf.nn.softmax(relu_)#
  
  labels = tf.to_int64(tf.constant(numpy.array([1,2,9])))
  #计算交叉熵,描述模型距离目标的远近度
  cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(matmul_, labels, name='xentropy')
  loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')#和label对比
  optimizer = tf.train.GradientDescentOptimizer(0.5)
  train = optimizer.minimize(loss)#梯度调整w,b
  
  test_images = tf.placeholder(tf.float32)
  test_softmax_ = tf.nn.softmax(tf.nn.relu(tf.matmul(test_images, weights_)))
  correct_prediction = tf.equal(tf.argmax(softmax_matmul_,1), tf.argmax(test_softmax_,1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  
  init_op = tf.initialize_all_variables()
  
  with tf.Session() as sess:
    sess.run(init_op)
    #print sess.run([weights_])
    #print sess.run([matmul_])
    print sess.run([softmax_matmul_])

    for step in xrange(100):
      _,loss_rs = sess.run([train,loss])
      if step % 20 == 0:
        print(step, loss_rs)
    #经过训练,将weight调到对应的lable
    print sess.run([softmax_matmul_])
    
    #evaluate 评估
    print(sess.run([tf.argmax(test_softmax_,1), correct_prediction, accuracy], feed_dict={test_images: [[1, 0, 1, 0]]}))
    print(sess.run([tf.argmax(test_softmax_,1), correct_prediction, accuracy], feed_dict={test_images: [[1 ,1, 0, 0]]}))
    print(sess.run([tf.argmax(test_softmax_,1), correct_prediction, accuracy], feed_dict={test_images: [[1 ,1, .9, 0]]}))