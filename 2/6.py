import torch

x = torch.arange(12)
print(x,x.shape,x.numel())

X = x.reshape(3, 4)
print(X)

X = torch.arange(12, dtype=torch.float32).reshape((3,4))
print(X[1:2])
