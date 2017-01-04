# -*- coding: utf-8 -*- 
'''
Created on Nov 29, 2016

@author: james
'''
import os
import time
import tensorflow as tf
import numpy as np
from PIL import Image
#import com.tf.mnist as mnist
from com.tf import mnist

TRAINNING_IMAGE_FILES = ['img/2-1.png', 'img/2-2.png', 'img/2-7.png', 'img/1-1.png']
TESTING_IMAGE_FILES = ['img/2-4.png']

# Basic model parameters as external flags.
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_float('learning_rate', 0.01, 'Initial learning rate.')
flags.DEFINE_integer('max_steps', 200, 'Number of steps to run trainer.')
flags.DEFINE_integer('hidden1', 128, 'Number of units in hidden layer 1.')
flags.DEFINE_integer('hidden2', 32, 'Number of units in hidden layer 2.')
flags.DEFINE_integer('batch_size', 1, 'Batch size. 分批处理尺寸,必须是数据量能除尽, Must divide evenly into the dataset sizes.')
flags.DEFINE_string('train_dir', 'data', 'Directory to put the training data.')
flags.DEFINE_boolean('fake_data', False, 'If true, uses fake data for unit testing.')

def get_image_data(image_files,labels):
  train_images = []
  for filename in image_files:
    image = Image.open(filename)#读取image数据
    image = image.resize((mnist.IMAGE_SIZE,mnist.IMAGE_SIZE))#resize图像
    image = np.array(image)#通过numpy得到数组
    train_images.append(image)
    #print(image)
    
  train_images = np.array(train_images)#展开
  train_images = train_images.reshape(len(image_files), mnist.IMAGE_PIXELS)#重塑

  train_labels = np.array(labels)
  
  return train_images,train_labels

train_images,train_labels = get_image_data(TRAINNING_IMAGE_FILES,[2,2,2,1])
test_images,test_labels = get_image_data(TESTING_IMAGE_FILES,[2])

def placeholder_inputs(batch_size):
  images_placeholder = tf.placeholder(tf.float32, shape=(batch_size, mnist.IMAGE_PIXELS))
  labels_placeholder = tf.placeholder(tf.int32, shape=(batch_size))
  return images_placeholder, labels_placeholder

def fill_feed_dict(images_feed,labels_feed, images_pl, labels_pl):  
  """Fills the feed_dict for training the given step.为训练特定步数填充
  A feed_dict takes the form of:
  feed_dict = {
      <placeholder>: <tensor of values to be passed for placeholder>,
      ....
  }
  Args:
    data_set: The set of images and labels, from input_data.read_data_sets()
    images_pl: The images placeholder, from placeholder_inputs().
    labels_pl: The labels placeholder, from placeholder_inputs().
  Returns:
    feed_dict: The feed dictionary mapping from placeholders to values.
  """
  feed_dict = {
      images_pl: images_feed,
      labels_pl: labels_feed,
  }
  return feed_dict

def do_eval(sess,
            eval_correct,
            images_placeholder,
            labels_placeholder,
            images, labels):
  # And run one epoch of eval.
  true_count = 0  # Counts the number of correct predictions.
  steps_per_epoch = len(images) // FLAGS.batch_size
  num_examples = steps_per_epoch * FLAGS.batch_size
  for step in xrange(steps_per_epoch):
    images_batch = images[step:step+FLAGS.batch_size]
    labels_batch = labels[step:step+FLAGS.batch_size]
    feed_dict = fill_feed_dict(images_batch, labels_batch, images_placeholder, labels_placeholder)
    accuracy = sess.run(eval_correct, feed_dict=feed_dict)
    print("accuracy:%.3f" % (accuracy))
    true_count+=accuracy
  precision = true_count / num_examples
  print('  Num examples: %d  Num correct: %d  Precision @ 1: %0.04f' %
        (num_examples, true_count, precision))

def run_training():
  with tf.Graph().as_default():
    #持有image,label数据
    images_placeholder, labels_placeholder = placeholder_inputs(FLAGS.batch_size)
    #推测模型
    logits = mnist.inference(images_placeholder, FLAGS.hidden1, FLAGS.hidden2)
    #输出丢失计算
    loss = mnist.loss(logits, labels_placeholder)
    #输出应用梯度
    train_op = mnist.training(loss, FLAGS.learning_rate)
    #输出对比罗杰斯和label(在评估中)
    eval_correct = mnist.evaluation(logits, labels_placeholder)
    #保存训练的checkpoint
    saver = tf.train.Saver()
    
    sess = tf.Session()
    init = tf.initialize_all_variables()
    sess.run(init)
    
    for step in xrange(FLAGS.max_steps):
      start_time = time.time()
      batch = step % len(train_images)
      train_images_batch = train_images[batch:batch+FLAGS.batch_size]
      train_labels_batch = train_labels[batch:batch+FLAGS.batch_size]
      feed_dict = fill_feed_dict(train_images_batch, train_labels_batch, images_placeholder, labels_placeholder)
      # Run one step of the model.  The return values are the activations
      # from the `train_op` (which is discarded) and the `loss` Op.  To
      # inspect the values of your Ops or variables, you may include them
      # in the list passed to sess.run() and the value tensors will be
      # returned in the tuple from the call.运行模型一步,返回值是训练输出的激活,损失.
      #要窥视输出值和变量,你要包在run的list中括包它们,tensors将返回一个tuple
      _, loss_value = sess.run([train_op, loss], feed_dict=feed_dict)
      duration = time.time() - start_time
      
      if step % 3 == 0:
        # Print status to stdout.
        print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
      if (step + 1) % 10 == 0 or (step + 1) == FLAGS.max_steps:
        checkpoint_file = os.path.join(FLAGS.train_dir, 'model.ckpt')
        saver.save(sess, checkpoint_file, global_step=step)
        print('Training Data Eval:')
        do_eval(sess, eval_correct, images_placeholder, labels_placeholder, test_images, test_labels)

def main(_):
  run_training()
if __name__ == '__main__':
  tf.app.run()