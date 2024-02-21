import threading
import time
import torch
x = torch.rand(5, 3)
print(x)

A = torch.arange(20).reshape(5, 4)
# print(A)
# print(A.T)

x = torch.arange(4, dtype=torch.float32)
x, x.sum()

A.shape, A.sum()

from torch.distributions import multinomial
fair_probs = torch.ones([6]) / 6
sample = multinomial.Multinomial(1, fair_probs).sample()

counts = multinomial.Multinomial(1000, fair_probs).sample()
counts / 1000  # 相对频率作为估计值

counts = multinomial.Multinomial(10, fair_probs).sample((500,))
cum_counts = counts.cumsum(dim=0)
estimates = cum_counts / cum_counts.sum(dim=1, keepdims=True)

from d2l import torch as d2l

d2l.set_figsize((6, 4.5))
for i in range(6):
    d2l.plt.plot(estimates[:, i].numpy(),
                label=("P(die=" + str(i + 1) + ")"))
d2l.plt.axhline(y=0.167, color='black', linestyle='dashed')
d2l.plt.gca().set_xlabel('Groups of experiments')
d2l.plt.gca().set_ylabel('Estimated probability')
d2l.plt.legend()
# d2l.plt.pause(100)
d2l.plt.show()

# help(torch.cumsum)