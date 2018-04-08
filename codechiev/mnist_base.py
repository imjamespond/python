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
    
    def __init__(self, width):
        '''
        Constructor
        '''
        print(tf.VERSION)
      
        self.W = tf.Variable(tf.zeros([784, self.classNum]))
        self.b = tf.Variable(tf.zeros([self.classNum]))
        
        '''
        None indicates that the first dimension, 
          corresponding to the batch size, can be of any size
        y_ will also consist of a 2d tensor,
          where each row is a one-hot 10-dimensional vector indicating (一组bits)
          which digit class (zero through nine) the corresponding MNIST image belongs to
        '''
        self.x = tf.placeholder(tf.float32, shape=[None, 784])#The input images
        self.y_ = tf.placeholder(tf.float32, shape=[None, self.classNum])#The target output classes 
        
        #Predicted Class and Loss Function
        self.y = tf.matmul(self.x , self.W) + self.b
        self.cross_entropy = tf.reduce_mean(
          tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=self.y))
        
        #Train the Model
        self.train_step = tf.train.GradientDescentOptimizer(0.5).minimize(self.cross_entropy)
        
        #Evaluate the Model
        self.correct_prediction = tf.equal(tf.argmax(self.y,1), tf.argmax(self.y_,1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))
        
        self.saver = tf.train.Saver()
        
    def learn(self, image, label): 
      with tf.Session() as sess:  
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        
        self.restoreSession(sess)
    
        x = np.array([image])
        y_ = np.zeros( (self.batchSize, 10) )
        y_[0][label]=1
        #Train the Model
        for _ in range(100):
          self.train_step.run(feed_dict={self.x: x, self.y_: y_})
        
        print(self.accuracy.eval(feed_dict={self.x: x, self.y_: y_}))
       
        self.saver.save(sess, os.path.join(FLAGS.checkpoint_dir, 'model.ckpt') )
        
    def identify(self, image, label):
      with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        x = np.array([image])
        y_ = np.zeros( (self.batchSize, 10) )
        y_[0][label]=1
        #Evaluate the Model
        if self.restoreSession(sess):
          print(self.accuracy.eval(feed_dict={self.x: x, self.y_: y_}))
    
    def restoreSession(self, sess):
      ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
      if ckpt and ckpt.model_checkpoint_path:
        self.saver.restore(sess, ckpt.model_checkpoint_path)
        return True
      return False
    