import tensorflow as tf

words = ['red', 'blue', 'yellow', 'pink', 'voilet', 'green']
word_ids = [0,0,1,1,2,2]
vocabulary_size = len(words)
embedding_size = 10
word_embeddings = tf.get_variable("word_embeddings", [vocabulary_size, embedding_size])

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


init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

time_steps=6
num_features=embedding_size
lstm_size=embedding_size

words_in_dataset = tf.placeholder(tf.float32, [time_steps, batch_size, num_features])

# Placeholder for the inputs in a given iteration.
words = tf.placeholder(tf.int32, [batch_size, time_steps])

lstmCell = tf.contrib.rnn.BasicLSTMCell(lstm_size)
# Initial state of the LSTM memory.
initial_state = state = tf.zeros([batch_size, lstmCell.state_size])

for i in range(time_steps):
    # The value of state is updated after processing each batch of words.
    output, state = lstmCell(words[:, i], state)

    # The rest of the code.
    # ...

final_state = state


# Initial state of the LSTM memory.
hidden_state = tf.zeros([batch_size, lstmCell.state_size])
current_state = tf.zeros([batch_size, lstmCell.state_size])
state = hidden_state, current_state
probabilities = []
loss = 0.0
for current_batch_of_words in words_in_dataset:
    # The value of state is updated after processing each batch of words.
    output, state = lstmCell(current_batch_of_words, state)
        
    # The LSTM output can be used to make next word predictions
    #logits = tf.matmul(output, softmax_w) + softmax_b
    #probabilities.append(tf.nn.softmax(logits))
 