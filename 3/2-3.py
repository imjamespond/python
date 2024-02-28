import numpy as np
import torch

w_len = 10
num_examples = 1000

X = torch.normal(10, 5, (num_examples, w_len)) #
y = X * X

# features = torch.arange(100)
# labels = torch.sin(2 * np.pi / 100 * features)

from d2l import torch as d2l

d2l.set_figsize()
d2l.plt.scatter(X[:, (1)].detach().numpy(), y[:, (1)].detach().numpy(), 1)
# d2l.plt.scatter(features.detach().numpy(),labels.numpy(), 1)
d2l.plt.show()