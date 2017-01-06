# -*- coding: utf-8 -*- 
'''
Created on 2016年11月28日

@author: metasoft
'''
import tensorflow as tf
if __name__ == '__main__':
  hello = tf.constant('Hello, TensorFlow!')
  sess = tf.Session()
  print(sess.run(hello))
  a = tf.constant(10)
  b = tf.constant(32)
  print(sess.run(a + b))
  
  input1_value = tf.placeholder(tf.float32)
  input2_value = tf.placeholder(tf.float32)
  mulop = tf.mul(input1_value, input2_value)
  divop = tf.div(input1_value, input2_value, "divop_")
  
  matmul1 = tf.matmul(input1_value, input2_value)
  softmax1 = tf.nn.softmax(matmul1)
  
  def fill_feed_dict(feed1,feed2, input1, input2):
    feed_dict = {
        input1: feed1,
        input2: feed2,
    }
    return feed_dict
  
  with tf.Session() as sess:
    #同时运行乘,除
    print sess.run([mulop,divop], feed_dict=fill_feed_dict([7.],[2.],input1_value,input2_value))
    print sess.run(matmul1, feed_dict=fill_feed_dict([[1,2,3]],[[4],[5],[6]], input1_value,input2_value))
    print sess.run(matmul1, feed_dict=fill_feed_dict([[1,2,3],[4,5,6]],[[0,0,0,0],[0,0,0,0],[0,0,0,0]], input1_value,input2_value))
    #4 even evidences
    print sess.run(softmax1,feed_dict=fill_feed_dict([[1,2,3],[4,5,6]],[[0,0,0,0],[0,0,0,0],[0,0,0,0]], input1_value,input2_value))
   