import tensorflow as tf

words = ['red', 'blue', 'yellow', 'pink', 'voilet', 'green']
word_ids = [0,0,1,1,2,2]
vocabulary_size = len(words)
embedding_size = 10
word_embeddings = tf.get_variable("word_embeddings",
    [vocabulary_size, embedding_size])
'''
  Let us assume that this has already been done, 
and that word_ids is a vector of these integers. 
  For example, the sentence “I have a cat.” 
could be split into [“I”, “have”, “a”, “cat”, “.”] 
and then the corresponding word_ids tensor would have shape [5] 
and consist of 5 integers. 
  To map these word ids to vectors, we need to create the embedding variable 
and use the tf.nn.embedding_lookup
'''
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
batch_size = 2, time_steps = 5
'''
# batch_size is 2
ids = [word_ids,[0,1,2,3,4,5]]
batch_size = len(ids)
embedded_word_ids = tf.nn.embedding_lookup(word_embeddings, ids) 
embedded_word_ids_list = tf.unstack(embedded_word_ids, axis=1)

#Use static RNN way
WORDS_FEATURE="foobar"
x_features={WORDS_FEATURE: ids}
# Convert indexes of words into embeddings.
# This creates embeddings matrix of [n_words, EMBEDDING_SIZE] and then
# maps word indexes of the sequence into [batch_size, sequence_length,
# EMBEDDING_SIZE].
word_vectors = tf.contrib.layers.embed_sequence(
x_features[WORDS_FEATURE], vocab_size=vocabulary_size, embed_dim=embedding_size)
# Split into list of embedding per word, while removing doc length dim.
# word_list results to be a list of tensors [batch_size, EMBEDDING_SIZE].
word_list = tf.unstack(word_vectors, axis=1)
# Create a Gated Recurrent Unit cell with hidden size of EMBEDDING_SIZE.
mGRUCell = tf.nn.rnn_cell.GRUCell(embedding_size)
# Create an unrolled Recurrent Neural Networks to length of
# MAX_DOCUMENT_LENGTH and passes word_list as inputs for each unit.
_, encoding = tf.nn.static_rnn(mGRUCell, word_list, dtype=tf.float32)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

print('embedding_lookup', sess.run(embedded_word_ids_list))
print('embed_sequence', sess.run(word_list))

# Use native RNN build way
initial_state = mGRUCell.zero_state(batch_size, tf.float32)
state = initial_state#sess.run(initial_state)
num_steps=6
outputs = []
for i in range(num_steps) :
  output, state = mGRUCell(embedded_word_ids_list[i], state)
  outputs.append(output)
 