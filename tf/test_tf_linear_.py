from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from six.moves import xrange 

import numpy as np
import tensorflow as tf

def my_input_fn():

    # Preprocess your data here...

    # ...then return 1) a mapping of feature columns to Tensors with
    # the corresponding feature data, and 2) a Tensor containing labels
    x = np.fromiter( (i for i in xrange(100)), dtype="int" )
    y = np.fromiter( (i*i/100 for i in xrange(100)), dtype=np.float32 )
    feature_cols = {"y": tf.constant(y) }
    label = tf.constant(x)
    return feature_cols, label
  
def samples():
  return {"y": np.array([10, 100], dtype=np.float32)}

def main():
  y = tf.contrib.layers.real_valued_column("y")
  
  feature_cols = [ y ]
  # Build 3 layer DNN with 10, 20, 10 units respectively.
  regressor = tf.contrib.learn.DNNRegressor(feature_columns=feature_cols,
                                          hidden_units=[10, 10],
                                          model_dir="/tmp/linear_")
  
  #Train
  regressor.fit(input_fn=my_input_fn, steps=2000)

  # Evaluate accuracy.
  #eval = regressor.evaluate(input_fn=my_input_fn, steps=1)
  #print("\neval: {}\n".format(eval))

  predictions = list(regressor.predict(input_fn=samples))
  print("\npredictions: {}\n".format(predictions))

if __name__ == "__main__":
    main()