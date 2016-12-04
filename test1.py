'''
Created on Nov 29, 2016

@author: james
'''
import tensorflow as tf
import com.tf.utils as utils

# Basic model parameters as external flags.
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_float('learning_rate', 0.01, 'Initial learning rate.')
flags.DEFINE_integer('max_steps', 2000, 'Number of steps to run trainer.')
flags.DEFINE_integer('hidden1', 128, 'Number of units in hidden layer 1.')
flags.DEFINE_integer('hidden2', 32, 'Number of units in hidden layer 2.')
flags.DEFINE_integer('batch_size', 4, 'Batch size. Must divide evenly into the dataset sizes.')
flags.DEFINE_string('train_dir', 'data', 'Directory to put the training data.')
flags.DEFINE_boolean('fake_data', False, 'If true, uses fake data for unit testing.')
NUM_CLASSES = 2 
IMAGE_SIZE = 28 
CHANNELS = 3
IMAGE_PIXELS = IMAGE_SIZE * IMAGE_SIZE * CHANNELS

def run_training():
  with tf.Graph().as_default():
    images_placeholder, labels_placeholder = utils.placeholder_inputs(4, IMAGE_PIXELS)
    logits = utils.inference(images_placeholder, FLAGS.hidden1, FLAGS.hidden2)

def main(_):
  run_training()
if __name__ == '__main__':
  tf.app.run()