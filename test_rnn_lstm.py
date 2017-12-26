import tensorflow as tf

words = ['red', 'blue', 'yellow', 'pink', 'voilet', 'green']
word_ids = [0,0,1,1,2,2]
vocabulary_size = len(words)
embedding_size = 10
word_embeddings = tf.get_variable("word_embeddings",
    [vocabulary_size, embedding_size])
embedded_word_ids = tf.nn.embedding_lookup(word_embeddings, word_ids)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

print( sess.run(embedded_word_ids))