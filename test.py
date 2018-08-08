# 序列模型
from keras.models import Sequential

model = Sequential()

# 堆叠层
from keras.layers import Dense

model.add(Dense(units=64, activation="relu", input_dim=100))
model.add(Dense(units=10, activation="softmax"))

# 模型好了 就可以compile了
model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])

# 如有需要 也可以自定 调节器
# model.compile(
#     loss=keras.losses.categorical_crossentropy,
#     optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True),
# )

