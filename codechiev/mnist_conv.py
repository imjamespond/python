# -*- coding: utf-8 -*- 
'''
Created on 2017年2月17日

@author: metasoft
'''
import tensorflow as tf
import numpy as np
import math
import os
from six.moves import xrange
from tensorflow.examples.tutorials.mnist import input_data

tutorials_mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('checkpoint_dir', 'data', 'Directory to put the training data.')

class Mnist(object):
  '''
  classdocs
  '''

  batchSize = 1
  pixelNum = 0
  classNum = 10
  
  def __init__(self, device='/cpu:0'):
    '''
    Constructor
    '''
    print(tf.VERSION)
    tf.logging.set_verbosity(tf.logging.INFO)

    self.graph = tf.Graph()
    with self.graph.as_default():
      with tf.device(device):
        '''
        None indicates that the first dimension, 
          corresponding to the batch size, can be of any size
        y_ will also consist of a 2d tensor,
          where each row is a one-hot 10-dimensional vector indicating (一组bits)
          which digit class (zero through nine) the corresponding MNIST image belongs to
        '''
        self.x = tf.placeholder(tf.float32, shape=[None, 784])#The input images
        #The target output classes
        #one-hot标签
        self.y_ = tf.placeholder(tf.float32, shape=[None, self.classNum])
        x_image = tf.reshape(self.x, [-1,28,28,1])#batch_size待定,宽,高,channels:1为黑白 
        
        #First Convolutional Layer         
        W_conv1 = self.weight_variable([5, 5, 1, 32])#[filter_height, filter_width, in_channels, out_channels]
        b_conv1 = self.bias_variable([32])
        # Applies 32 5x5 filters (extracting 5x5-pixel subregions), 1 channel
        h_conv1 = tf.nn.relu(self.conv2d(x_image, W_conv1) + b_conv1)#[batch_size, 28, 28, 32]
        # max pooling with a 2x2 filter and stride of 2
        h_pool1 = self.max_pool_2x2(h_conv1)#pool1 has a shape of [batch_size, 14, 14, 1(错了?32)]: the 2x2 filter reduces width and height by 50%.
        
        #Second Convolutional Layer
        W_conv2 = self.weight_variable([5, 5, 32, 64])
        b_conv2 = self.bias_variable([64])
        #Applies 64 5x5 filters
        h_conv2 = tf.nn.relu(self.conv2d(h_pool1, W_conv2) + b_conv2)#conv2 has a shape of [batch_size, 14, 14, 64]
        h_pool2 = self.max_pool_2x2(h_conv2)#pool2 has shape [batch_size, 7, 7, 64] (50% reduction of width and height from conv2).
        
        #Densely Connected Layer
        W_fc1 = self.weight_variable([7 * 7 * 64, 1024])
        b_fc1 = self.bias_variable([1024])
        
        h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        
        #Dropout
        #  1,024 neurons, with dropout regularization rate of 0.4 
        #  (probability of 0.4 that any given element will be dropped during training)
        self.keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)
        
        #Readout Layer
        W_fc2 = self.weight_variable([1024, 10])
        b_fc2 = self.bias_variable([10])
        # 10 neurons, one for each digit target class (0–9)
        # 最后得到10维的特征向量
        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
        
        #Train and Evaluate the Model
        #最后softmax分类得到各类概率, 交差熵计算误差
        with tf.name_scope('cross_entropy'):
          #internally computes the softmax activation内部计算softmax激活
          diff = tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=y_conv)
          with tf.name_scope('total'):
            #误差平均值
            cross_entropy = tf.reduce_mean( diff )       
        #优化
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

        #正确率, argmax给出最大值, y_conv是否还要加上softmax?
        correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(self.y_,1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        #预测值
        '''tf.argmax is an extremely useful function 
          which gives you the index of the highest entry in a tensor along some axis'''
        self.highest_entry = tf.argmax(y_conv,1)

      tf.summary.scalar('cross_entropy', cross_entropy)
      self.saver = tf.train.Saver()

  ''' initialize weights with a small amount of noise for symmetry breaking,
      and to prevent 0 gradients'''
  def weight_variable(self, shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)
  
  def bias_variable(self, shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)
  
  #Convolution and Pooling
  def conv2d(self, x, W):
    # strides: A list of ints. 1-D tensor of length 4. 
    # The stride of the sliding window for each dimension of input. 
    # The dimension order is determined by the value of data_format
    # data_format: An optional string from: "NHWC", "NCHW". Defaults to "NHWC"
    # the data is stored in the order of: [batch, height, width, channels]
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
    """
    For the 'SAME' padding, the output height and width are computed as:
    out_height = ceil(float(in_height) / float(strides[1]))
    out_width  = ceil(float(in_width) / float(strides[2]))

    The filter is applied to image patches of the same size 
    as the filter and strided according to the strides argument. 
    strides = [1, 1, 1, 1] applies the filter to a patch at every offset, 
    strides = [1, 2, 2, 1] applies the filter to every other image patch 
      in each dimension, etc.
    """
  
  def max_pool_2x2(self, x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
      strides=[1, 2, 2, 1], padding='SAME')

def restoreSession( sess, saver):
  ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
  if ckpt and ckpt.model_checkpoint_path:
    saver.restore(sess, ckpt.model_checkpoint_path)
    return True
  return False

def learn( image, label): 
  mnist = Mnist('/gpu:0')
  with tf.Session(graph=mnist.graph) as sess: 
    
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    
    restoreSession(sess, mnist.saver)

    x = np.array([image])
    #one-hot label
    y_ = np.zeros( (mnist.batchSize, 10) )
    y_[0][label]=1
    #Train the Model
    for _ in range(100):
      mnist.train_step.run( feed_dict={mnist.x: x, mnist.y_: y_, mnist.keep_prob: 1.0})
    
    print(mnist.accuracy.eval(feed_dict={mnist.x: x, mnist.y_: y_, mnist.keep_prob: 0.5}))
    
    mnist.saver.save(sess, os.path.join(FLAGS.checkpoint_dir, 'model.ckpt') )
    
def identify( image):
  mnist = Mnist(device='/gpu:0')
  with tf.Session(graph=mnist.graph) as sess: 
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    x = np.array([image])
    #Evaluate the Model
    if restoreSession(sess,mnist.saver):
      print(mnist.highest_entry.eval(feed_dict={mnist.x: x, mnist.keep_prob: 0.5}))

def trainExample():
  mnist = Mnist(device='/gpu:0')
  with tf.Session(graph=mnist.graph) as sess: 
    # Merge all the summaries and write them out to ./summary (by default)
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter('summary', sess.graph)
    
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    
    restoreSession(sess,mnist.saver)
    
    for i in range(20000):
      batch = tutorials_mnist.train.next_batch(50)
      if i%100 == 0:
        summary,train_accuracy = sess.run([merged, mnist.accuracy], feed_dict={
            mnist.x:batch[0], mnist.y_: batch[1], mnist.keep_prob: 1.0})
        train_writer.add_summary(summary, i)
        print("step %d, training accuracy %g"%(i, train_accuracy))
      mnist.train_step.run(feed_dict={mnist.x: batch[0], mnist.y_: batch[1], mnist.keep_prob: 0.5})
    
    train_writer.flush()
    mnist.saver.save(sess, os.path.join(FLAGS.checkpoint_dir, 'model.ckpt') )

  mnist_cpu = Mnist()
  with tf.Session(graph=mnist_cpu.graph) as sess: 
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    restoreSession(sess,mnist.saver)

    #mnist test requir more than 2GB mem that may cause gpu memalloc error
    print("test accuracy %g"%mnist_cpu.accuracy.eval(feed_dict={
        mnist_cpu.x: tutorials_mnist.test.images, mnist_cpu.y_: tutorials_mnist.test.labels, 
        mnist_cpu.keep_prob: 1.0}))
