# -*- coding: utf-8 -*- 
'''
Created on 2016年11月28日

@author: metasoft
'''
import tensorflow as tf
import numpy
import math
if __name__ == '__main__':
  with tf.name_scope('foo'):
    var = tf.constant('foo')
    foo = tf.add("this is ",var)
  with tf.name_scope('bar'):
    var = tf.constant('bar')
    bar = tf.add("this is ",var)
    
  a = tf.constant(10)
  b = tf.constant(32)
  
  
  state = tf.Variable(0, name="counter")
  one = tf.constant(1)
  new_value = tf.add(state, one)
  update = tf.assign(state, new_value)
  
  input1_value = tf.placeholder(tf.float32)
  input2_value = tf.placeholder(tf.float32)
  mulop = tf.mul(input1_value, input2_value)
  divop = tf.div(input1_value, input2_value, "divop_")
  
  weights_ = tf.placeholder(tf.float32)
  weights1_ = tf.Variable(tf.truncated_normal([3, 32], stddev=1.0 / math.sqrt(float(3))))
  images_ = tf.placeholder(tf.float32)
  labels_ = tf.placeholder(tf.float32)
  
  matmul_ = tf.matmul(images_, weights_)
  softmax_matmul_ = tf.nn.softmax(matmul_)
  
  reducesum_x = [[1, 1, 1], [1, 1, 2]]
  reducesum_ = tf.reduce_sum(reducesum_x, reduction_indices=[1])  
  argmax_ = tf.argmax(reducesum_,0)
  
  matmul1_ = tf.nn.relu(tf.matmul(images_, weights1_))
  labels_ = tf.to_int64(labels_)
  softmax_cross_entropy_with_logits_matmul_ = tf.nn.sparse_softmax_cross_entropy_with_logits(matmul1_, labels_, name='xentropy')
  reduce_mean_ = tf.reduce_mean(softmax_cross_entropy_with_logits_matmul_, name='xentropy_mean')
  tf.summary.scalar('loss', reduce_mean_)
  #An Operation that updates the variables in `var_list`.  If `global_step`
  #was not `None`, that operation also increments `global_step`.
  train_step = tf.train.GradientDescentOptimizer(0.01).minimize(softmax_cross_entropy_with_logits_matmul_)
  argmax1_ = tf.argmax(matmul1_,0)
  
  def fill_feed_dict(feed1,feed2, input1, input2):
    feed_dict = {
        input1: feed1,
        input2: feed2,
    }
    return feed_dict
  
  init_op = tf.initialize_all_variables()
  with tf.Session() as sess:
    print(sess.run(foo))
    print(sess.run(bar))
    print(sess.run(a + b))
    
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
    print "softmax_matmul"
    #4 evidences
    print sess.run(softmax_matmul_,feed_dict={weights_:weights, images_:images})
    print sess.run(reducesum_)
    print sess.run(argmax_)
    
    print "softmax_cross_entropy_with_logits_matmul"
    print sess.run(softmax_cross_entropy_with_logits_matmul_,feed_dict={images_:images, labels_:labels})
    print sess.run(argmax1_,feed_dict={images_:images, labels_:labels})
    for step in xrange(100):
      _,loss = sess.run([train_step,reduce_mean_],feed_dict={images_:images, labels_:labels})
      if step % 10 == 0:
        print loss
    