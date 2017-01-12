# -*- coding: utf-8 -*- 
'''
Created on 2016/11/28

@author: metasoft
'''
import tensorflow as tf
if __name__ == '__main__':
  sess = tf.Session()
  '''
  new_saver = tf.train.import_meta_graph('data/sess_save.meta')
  new_saver.restore(sess, tf.train.latest_checkpoint('./data'))
  all_vars = tf.trainable_variables()
  for v in all_vars:
      print(v.name)
  '''
  state = tf.Variable(0, name="counter")
  saver = tf.train.Saver() 
  with tf.Session() as sess:
    
    ckpt = tf.train.get_checkpoint_state('data')
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
        print sess.run(state)