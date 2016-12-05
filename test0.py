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
  
  def fill_feed_dict(feed1,feed2, input1, input2):
    feed_dict = {
        input1: feed1,
        input2: feed2,
    }
    return feed_dict
  with tf.Session() as sess:
    print sess.run([mulop,divop], feed_dict=fill_feed_dict([7.],[2.],input1_value,input2_value))
