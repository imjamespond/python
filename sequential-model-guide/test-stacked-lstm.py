from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

data_dim = 16
timesteps = 8
num_classes = 10

# expected input data shape: (batch_size, timesteps, data_dim)
model = Sequential()
model.add(LSTM(32,  # returns a sequence of vectors of dimension 32
               return_sequences=True,
               input_shape=(timesteps, data_dim))) 
model.add(LSTM(32,  # returns a sequence of vectors of dimension 32, 返回维度为32
               return_sequences=True))
model.add(LSTM(32)) # return a single vector of dimension 32, 返回单一数组维度为32
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Generate dummy training data
# 生成1000份维度 timesteps*data_dim 的数据
x_train = np.random.random((1000, timesteps, data_dim))
# 生成1000份标签每分对应10个类之一
y_train = np.random.random((1000, num_classes))

# Generate dummy validation data
x_val = np.random.random((100, timesteps, data_dim))
y_val = np.random.random((100, num_classes))

model.fit(x_train, y_train,
          batch_size=64, # 每次梯度 更新的样本数
          epochs=25, # 训练样本的次数, 和initial_epoch放一起可认为是最后一次的次数
          validation_data=(x_val, y_val))

classes = model.predict(x_train, batch_size=128)
from numpy import argmax
for clz in classes:
  print(argmax(clz))
