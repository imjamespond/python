import torch
from d2l import torch as d2l
import matplotlib
import matplotlib.pyplot as plt
""" 激活函数 """
""" ReLU函数 
通俗地说，ReLU函数通过将相应的活性值设为0，仅保留正元素并丢弃所有负元素。 为了直观感受一下，我们可以画出函数的曲线图。 正如从图中所看到，激活函数是分段线性的。
"""
x = torch.arange(-8.0, 8.0, 0.1, requires_grad=True)
y = torch.relu(x)
d2l.plot(x.detach(), y.detach(), "x", "relu(x)", figsize=(5, 2.5))
d2l.plt.figure() 
""" 当输入为负时，ReLU函数的导数为0，而当输入为正时，ReLU函数的导数为1。 注意，当输入值精确等于0时，ReLU函数不可导。 
在此时，我们默认使用左侧的导数，即当输入为0时导数为0。 我们可以忽略这种情况，因为输入可能永远都不会是0。 
这里引用一句古老的谚语，“如果微妙的边界条件很重要，我们很可能是在研究数学而非工程”， 这个观点正好适用于这里。 下面我们绘制ReLU函数的导数。 
"""
y.backward(torch.ones_like(x), retain_graph=True)
d2l.plot(x.detach(), x.grad, "x", "grad of relu", figsize=(5, 2.5))
d2l.plt.figure()

""" sigmoid函数 
当我们想要将输出视作二元分类问题的概率时， sigmoid仍然被广泛用作输出单元上的激活函数 （sigmoid可以视为softmax的特例）。 
然而，sigmoid在隐藏层中已经较少使用， 它在大部分时候被更简单、更容易训练的ReLU所取代。
"""
y = torch.sigmoid(x)
d2l.plot(x.detach(), y.detach(), "x", "sigmoid(x)", figsize=(5, 2.5))
d2l.plt.figure() 

# 清除以前的梯度
x.grad.data.zero_()
y.backward(torch.ones_like(x), retain_graph=True)
d2l.plot(x.detach(), x.grad, "x", "grad of sigmoid", figsize=(5, 2.5))
d2l.plt.figure() 

""" tanh函数 
tanh(双曲正切)函数也能将其输入压缩转换到区间(-1, 1)上
"""
y = torch.tanh(x)
d2l.plot(x.detach(), y.detach(), "x", "tanh(x)", figsize=(5, 2.5))
d2l.plt.figure() 
""" tanh函数的导数图像如下所示。 当输入接近0时，tanh函数的导数接近最大值1。 与我们在sigmoid函数图像中看到的类似， 输入在任一方向上越远离0点，导数越接近0。 """
# 清除以前的梯度
x.grad.data.zero_()
y.backward(torch.ones_like(x), retain_graph=True)
d2l.plot(x.detach(), x.grad, "x", "grad of tanh", figsize=(5, 2.5))
d2l.plt.show()

