from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

data_dim = 16
timesteps = 8
num_classes = 10
batch_size = 32

# Expected input batch shape: (batch_size, timesteps, data_dim)
# Note that we have to provide the full batch_input_shape since the network is stateful. 
# 注意到 我们提供 完整的 batch-input-shape 参数是因为 些网络是有状态的
# the sample of index i in batch k is the follow-up for the sample i in batch k-1.
# 样本i 在批量k中 将是 前一批?
# stateful=True, 在进行一批样本处理后 获得内部状态 并重新用作 下一批的初始状态
# 这样可以有效控制复杂度 从而 可以处理较长的序列
model = Sequential()
model.add(LSTM(32, 
               return_sequences=True, 
               stateful=True,
               batch_input_shape=(batch_size, timesteps, data_dim)))
model.add(LSTM(32, 
               return_sequences=True, 
               stateful=True))
model.add(LSTM(32, stateful=True))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Generate dummy training data
# 生成 10批数据 份维度 timesteps*data_dim 的数据
x_train = np.random.random((batch_size * 10, timesteps, data_dim))
y_train = np.random.random((batch_size * 10, num_classes))

# Generate dummy validation data
x_val = np.random.random((batch_size * 3, timesteps, data_dim))
y_val = np.random.random((batch_size * 3, num_classes))

model.fit(x_train, y_train,
          batch_size=batch_size, epochs=5, shuffle=False,
          validation_data=(x_val, y_val))