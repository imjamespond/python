from keras.models import Sequential
from keras.layers import Dense

# For a single-input model with 2 classes (binary classification):
# 单独模型 分两类
model = Sequential()
# units: dimensionality of the output space输出维度, input_dim: 输入维度, 
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dense(1, activation='sigmoid')) # 最后输出维度为1, 可表示两个分类
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Generate dummy data
import numpy as np
# 生成1000份维度100的数据
data = np.random.random((1000, 100))
# 生成1000份标签(长度为1000的1维数组)(0或1, 2 is exclusive)
labels = np.random.randint(2, size=(1000, 1))

# Train the model, iterating on the data in batches of 32 samples
# 批量32?, epoch为训练10次
model.fit(data, labels, epochs=10, batch_size=32)

import os 
h5path = os.path.dirname(os.path.realpath(__file__))+'/sm.h5'
model.save(h5path)

from keras.models import load_model 
model = load_model(h5path) 

# def keys(f):
#     return [key for key in f.keys()]

# import h5py
# with h5py.File(h5path, 'r') as f:
#   fkeys = keys(f)
#   print(fkeys)
#   print(keys(f['model_weights']))
#   print(keys(f['optimizer_weights']))

