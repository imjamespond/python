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
    classNum = 3
    
    def __init__(self, width):
        '''
        Constructor
        '''
        print(tf.__version__)
      
        self.pixelNum = width*width
        self.weights = tf.Variable(tf.truncated_normal([self.pixelNum, self.classNum], stddev=1.0 / math.sqrt(float(self.pixelNum))), name='weights')
        self.biases = tf.Variable(tf.zeros([self.classNum]), name='biases')
        
        self.images = tf.placeholder(tf.float32, shape=(self.batchSize, self.pixelNum))
        self.lables = tf.placeholder(tf.int32, shape=(self.batchSize))
  
        logits = tf.nn.relu(tf.matmul(self.images, self.weights)+self.biases)
        softmax = tf.nn.softmax(logits)
        
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits, self.lables, name='xentropy')
        self.loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
        optimizer = tf.train.GradientDescentOptimizer(0.5)
        self.train = optimizer.minimize(self.loss)
        
        self.test_softmax = tf.nn.softmax(tf.nn.relu(tf.matmul(self.images, self.weights)))
        self.correct_prediction = tf.equal(tf.argmax(softmax,1), tf.argmax(self.test_softmax,1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))
            
        self.saver = tf.train.Saver()
        
    def learn(self, image, label): 
      with tf.Session() as sess:  
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        
        self.restoreSession(sess)
        
        for step in xrange(100):
          _,loss_rs = sess.run([self.train,self.loss], feed_dict={self.images: [image], self.lables: [label]})
          if step % 20 == 0:
            print(step, loss_rs)
        print (sess.run([tf.argmax(self.test_softmax,1), self.correct_prediction,self.accuracy], feed_dict={self.images: [image]}))
 
        self.saver.save(sess, os.path.join(FLAGS.checkpoint_dir, 'model.ckpt') )
        
    def identify(self, image):
      with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        
        if self.restoreSession(sess):
          print(sess.run(self.weights))
          print(sess.run([tf.argmax(self.test_softmax,1), self.correct_prediction,self.accuracy], feed_dict={self.images: [image]}))
    
    def restoreSession(self, sess):
      ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
      if ckpt and ckpt.model_checkpoint_path:
        self.saver.restore(sess, ckpt.model_checkpoint_path)
        return True
      return False
    