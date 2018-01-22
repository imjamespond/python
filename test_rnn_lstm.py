import tensorflow as tf
import collections

# https://www.tensorflow.org/tutorials/recurrent
# https://github.com/tensorflow/models/tree/master/tutorials/rnn/ptb

flags = tf.flags
flags.DEFINE_bool("use_fp16", False,
                  "Train using 16-bit floats instead of 32bit floats")
FLAGS = flags.FLAGS
logging = tf.logging

def data_type():
  return tf.float16 if FLAGS.use_fp16 else tf.float32

words = ['The', 'brown', 'fox', 'is','quick','The', 'red',   'fox', 'jumped', 'high']
vocab_size = 10
batch_size = 2
embedding_size = 15
num_steps = 2
num_features = embedding_size
hidden_size = embedding_size

'''
For example:
 t=0  t=1    t=2  t=3     t=4
[The, brown, fox, is,     quick]
[The, red,   fox, jumped, high]

words_in_dataset[0] = [The, The]
words_in_dataset[1] = [brown, red]
words_in_dataset[2] = [fox, fox]
words_in_dataset[3] = [is, jumped]
words_in_dataset[4] = [quick, high]
batch_size = 2, num_steps = 5
'''
# batch_size is 2

def _build_vocab(data):
  counter = collections.Counter(data)
  count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

  words, _ = list(zip(*count_pairs))
  word_to_id = dict(zip(words, range(len(words))))

  return word_to_id

word_to_id = _build_vocab(words)
# print(word_to_id)
# {'The': 0, 'fox': 1, 'brown': 2, 'high': 3, 'is': 4, 'jumped': 5, 'quick': 6, 'red': 7}

def _to_word_ids(data, word_to_id): 
  return [word_to_id[word] for word in data if word in word_to_id]

word_ids = _to_word_ids(words, word_to_id)
# print(word_ids)
# [0, 2, 1, 4, 6, 0, 7, 1, 5, 3]

def _build_data(word_ids, batch_size, num_steps, name=None):
  with tf.name_scope(name, "build_data", [word_ids, batch_size, num_steps]):
    word_ids = tf.convert_to_tensor(word_ids, name="raw_data", dtype=tf.int32)

    data_len = tf.size(word_ids)
    batch_len = data_len // batch_size
    data = tf.reshape(word_ids[0 : batch_size * batch_len],
                      [batch_size, batch_len])

    epoch_size = (batch_len - 1) // num_steps
    assertion = tf.assert_positive(
        epoch_size,
        message="epoch_size == 0, decrease batch_size or num_steps")
    with tf.control_dependencies([assertion]):
      epoch_size = tf.identity(epoch_size, name="epoch_size")

    i = tf.train.range_input_producer(epoch_size, shuffle=False).dequeue()
    x = tf.strided_slice(data, [0, i * num_steps], [batch_size, (i + 1) * num_steps])
    x.set_shape([batch_size, num_steps])
    y = tf.strided_slice(data, [0, i * num_steps + 1], [batch_size, (i + 1) * num_steps + 1])
    y.set_shape([batch_size, num_steps])
    return x,y

inputX, inputY = _build_data(word_ids, batch_size, num_steps) 

#data = tf.reshape(raw_data[0 : batch_size * batch_len], [batch_size, batch_len])


# word_embeddings = tf.get_variable("word_embeddings", [vocab_size, embedding_size])
# embedded_word_ids = tf.nn.embedding_lookup(word_embeddings, word_ids) 
# embedded_word_ids_list = tf.unstack(embedded_word_ids, num=num_steps, axis=1)



# words_in_dataset = tf.placeholder(tf.float32, [num_steps, batch_size, num_features])

# # Placeholder for the inputs in a given iteration.
# words = tf.placeholder(tf.int32, [batch_size, num_steps])

# lstmCell = tf.contrib.rnn.BasicLSTMCell(hidden_size)
# # Initial state of the LSTM memory.
# initial_state = state = tf.zeros([batch_size, lstmCell.state_size])

# #output, state = self._build_rnn_graph(inputs, config, is_training) 
# inputs = embedded_word_ids_list
# outputs, state = tf.contrib.rnn.static_rnn(lstmCell, inputs,
#                             initial_state=initial_state)
# output = tf.reshape(tf.concat(outputs, 1), [-1, hidden_size])

# softmax_w = tf.get_variable(
#     "softmax_w", [embedding_size, vocab_size], dtype=data_type())
# softmax_b = tf.get_variable(
#     "softmax_b", [vocab_size], dtype=data_type())
# logits = tf.nn.xw_plus_b(output, softmax_w, softmax_b)
#     # Reshape logits to be a 3-D tensor for sequence loss
# logits = tf.reshape(logits, [batch_size, num_steps, vocab_size])

# # Use the contrib sequence loss and average over the batches
# loss = tf.contrib.seq2seq.sequence_loss(
#     logits,
#     input_.targets,
#     tf.ones([batch_size, num_steps], dtype=data_type()),
#     average_across_timesteps=False,
#     average_across_batch=True)

# # Update the cost
# _cost = tf.reduce_sum(loss)
# _final_state = state

class LSTM_Test(tf.test.TestCase):
  def testPtbProducer(self):  
    inputX, inputY = _build_data(word_ids, batch_size, num_steps)
    with self.test_session() as session: 
      coord = tf.train.Coordinator()
      tf.train.start_queue_runners(session, coord=coord)
      try:
        print( session.run([inputX, inputY]) )
      finally:
        coord.request_stop()
        coord.join()

if __name__ == "__main__":
  #tf.test.main()
  pass