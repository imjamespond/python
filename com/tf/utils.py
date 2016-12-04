'''
Created on Nov 29, 2016

@author: james
'''
import tensorflow as tf
def placeholder_inputs(batch_size, pixel_num):
  images_placeholder = tf.placeholder(tf.float32, shape=(batch_size, pixel_num))
  labels_placeholder = tf.placeholder(tf.int32, shape=(batch_size))
  return images_placeholder, labels_placeholder

def inference(images, hidden1_units, hidden2_units):
  pass