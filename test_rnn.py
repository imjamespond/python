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
# [word_ids] batch_size is 1
ids = [word_ids]
batch_size = len(ids)
embedded_word_ids = tf.nn.embedding_lookup(word_embeddings, ids) 

WORDS_FEATURE="foobar"
x_features={WORDS_FEATURE: word_ids}
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

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

print('embedding_lookup', sess.run(embedded_word_ids))
print('embed_sequence', sess.run(word_vectors))

initial_state = mGRUCell.zero_state(batch_size, tf.float32)
state = sess.run(initial_state)
print(state)
# num_steps=6
# for i in range(num_steps) :
#   output, state = mGRUCell(embedded_word_ids[:, i, :], state)
#   print (output, state)
 