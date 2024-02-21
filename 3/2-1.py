import torch

w = torch.tensor([2, -3.4])
b = 4.2
X = torch.normal(mean=0, std=1, size=(10, 2))
y = torch.matmul(X, w) + b

from d2l import torch as d2l

d2l.plot(X.detach().numpy())
d2l.plt.show()
