from keras.models import Sequential
from keras.layers import Dense, Activation

model = Sequential([
    # Pass an input_shape argument to the first layer. 
    # (and only the first, because following layers can do automatic shape inference)
    # specify a fixed batch size by batch_size=32, it will then expect every batch of inputs to have the same batch shape 
    Dense(32, input_shape=(784,)),
    Activation('relu'),
    Dense(10),
    Activation('softmax'),
])

# # You can also simply add layers via the .add() method:
# model = Sequential()
# model.add(Dense(32, input_dim=784))
# model.add(Activation('relu'))


# Compilation

# For a multi-class classification problem
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# # For a binary classification problem
# model.compile(optimizer='rmsprop',
#               loss='binary_crossentropy',
#               metrics=['accuracy'])

# # For a mean squared error regression problem
# model.compile(optimizer='rmsprop',
#               loss='mse')

# # For custom metrics
# import keras.backend as K

# def mean_pred(y_true, y_pred):
#     return K.mean(y_pred)

# model.compile(optimizer='rmsprop',
#               loss='binary_crossentropy',
#               metrics=['accuracy', mean_pred])


# Training
# Keras models are trained on Numpy arrays of input data and labels. 
# For training a model, you will typically use the  fit function. Read its documentation here.

# # For a single-input model with 2 classes (binary classification):

# model = Sequential()
# model.add(Dense(32, activation='relu', input_dim=100))
# model.add(Dense(1, activation='sigmoid'))
# model.compile(optimizer='rmsprop',
#               loss='binary_crossentropy',
#               metrics=['accuracy'])

# # Generate dummy data
# import numpy as np
# data = np.random.random((1000, 100))
# labels = np.random.randint(2, size=(1000, 1))

# # Train the model, iterating on the data in batches of 32 samples
# model.fit(data, labels, epochs=10, batch_size=32)

import keras

# For a single-input model with 10 classes (categorical classification):

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Generate dummy data
import numpy as np
data = np.random.random((1000, 100))
labels = np.random.randint(10, size=(1000, 1))

# Convert labels to categorical one-hot encoding
one_hot_labels = keras.utils.to_categorical(labels, num_classes=10)

# Train the model, iterating on the data in batches of 32 samples
model.fit(data, one_hot_labels, epochs=10, batch_size=32)

# Examples
# https://keras.io/getting-started/sequential-model-guide/