import numpy as np
import torch

# 创建向量x
x = torch.arange(100.)
# print(x)

# 需要保存梯度
x.requires_grad_(True)
# print(x,x.grad)

x_ = 2*np.pi / len(x) * x
y = torch.sin(x_)

# y.sum().backward()
y.backward(torch.ones(len(x)))

from d2l import torch as d2l
d2l.plot(x_.detach().numpy(), x.grad, xlabel="x", ylabel="y")
d2l.plt.show()