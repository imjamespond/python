# -*- coding: utf-8 -*- 
'''
Created on 2016年11月28日

@author: metasoft
'''
import tensorflow as tf
import numpy
import math
if __name__ == '__main__':
  hello = tf.constant('Hello, TensorFlow!')
  sess = tf.Session()
  print(sess.run(hello))
  a = tf.constant(10)
  b = tf.constant(32)
  print(sess.run(a + b))
  
  state = tf.Variable(0, name="counter")
  one = tf.constant(1)
  new_value = tf.add(state, one)
  update = tf.assign(state, new_value)
  
  input1_value = tf.placeholder(tf.float32)
  input2_value = tf.placeholder(tf.float32)
  mulop = tf.mul(input1_value, input2_value)
  divop = tf.div(input1_value, input2_value, "divop_")
  
  weights_ = tf.placeholder(tf.float32)
  weights1_ = tf.truncated_normal([3, 32], stddev=1.0 / math.sqrt(float(3)))
  images_ = tf.placeholder(tf.float32)
  labels_ = tf.placeholder(tf.float32)
  
  matmul_ = tf.matmul(images_, weights_)
  softmax_matmul_ = tf.nn.softmax(matmul_)
  matmul1_ = tf.matmul(images_, weights1_)
  labels_ = tf.to_int64(labels_)
  softmax_cross_entropy_with_logits_matmul_ = tf.nn.sparse_softmax_cross_entropy_with_logits(matmul1_, labels_, name='xentropy')
  
  reducesum_x = [[1, 1, 1], [1, 1, 1]]
  reducesum_ = tf.reduce_sum(reducesum_x, reduction_indices=[1])
  
  def fill_feed_dict(feed1,feed2, input1, input2):
    feed_dict = {
        input1: feed1,
        input2: feed2,
    }
    return feed_dict
  
  init_op = tf.initialize_all_variables()
  with tf.Session() as sess:
    # 运行 'init' op
    sess.run(init_op)
    # 打印 'state' 的初始值
    print sess.run(state)
    # 运行 op, 更新 'state', 并打印 'state'
    for _ in range(3):
      sess.run(update)
      print sess.run(state)
        
    images = [[1,2,3],[1,2,3.5]]
    labels = numpy.array([1,1])
    weights = [[0,0,0,1],[0,0,0,1],[0,0,0,1]]

    #同时运行乘,除
    print sess.run([mulop,divop], feed_dict=fill_feed_dict([7.],[2.],input1_value,input2_value))
    print sess.run(matmul_, feed_dict=fill_feed_dict([[1,2,3]],[[4],[5],[6]], images_,weights_))
    print sess.run(weights1_)

    #3个像素两张图, 4个label3个像素权重
    print sess.run(matmul_, feed_dict={weights_:weights, images_:images})
    #4 evidences
    print sess.run(softmax_matmul_,feed_dict={weights_:weights, images_:images})
    print sess.run(softmax_cross_entropy_with_logits_matmul_,feed_dict={images_:images, labels_:labels})
   
    print sess.run(reducesum_)