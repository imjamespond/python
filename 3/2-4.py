import numpy as np
import torch
from torch import Tensor

batch_size = 12
num_examples = 1000


def data_iter():
    for i in range(0, features.shape[0], batch_size):
        end = min(i + batch_size, num_examples)
        yield features[i:end], labels[i:end]


def net(X: Tensor, w: Tensor, b: Tensor):
    return torch.matmul(X, w) + b


def loss(y_hat: Tensor, y: Tensor):
    return (y_hat - y.reshape(y_hat.shape)) ** 2 / 2


true_w = Tensor([2, -3.4]).reshape(2, 1)
true_b = 4.2

w = torch.normal(0, 0.1, size=(true_w.shape), requires_grad=True)
b = torch.zeros(1, requires_grad=True)


X = torch.normal(0, 1, size=(num_examples, len(true_w)))
y = net(X, true_w, true_b)
y += torch.normal(0, 0.01, y.shape)

features = X
labels = y


lr = 0.03
num_epochs = 3


def updater(
    *params: Tensor,
):
    with torch.no_grad():
        for param in params:
            param -= lr * param.grad / batch_size
            param.grad.zero_()


def evaluate(ep):
    with torch.no_grad():
        train_l = loss(net(features, w, b), labels)
        print(f"epoch {ep}, loss {float(train_l.mean()):f}")  # 1000行均值, :f打印浮点
        print(w.detach().numpy(), b.detach().numpy())


evaluate(0)

for ep in range(num_epochs):
    tain_data = data_iter()
    for X, y in tain_data:
        y_hat = net(X, w, b)
        l = loss(y_hat, y)
        l.sum().backward()
        params = (w, b)
        updater(*params)
    evaluate(ep + 1)

from d2l import torch as d2l

predicted_labels = net(features, w, b)

d2l.set_figsize()
d2l.plt.scatter(np.arange(100), (labels - predicted_labels)[:100, (0)].detach().numpy(), 1)
d2l.plt.show()
