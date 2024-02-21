import torch

# 创建向量x
x = torch.arange(4.0)
# print(x)

# 需要保存梯度
x.requires_grad_(True)
# print(x,x.grad)

# x点积 0 1 2 3 逐个代入求和
y = 2 * torch.dot(x, x)
print(y)

# 通过调用反向传播函数来自动计算y关于x每个分量的梯度
y.backward()
print(x.grad,x.grad == 4 * x) # 0 + 2 + 8 + 18 = 28 , 2 * 2 * x

# 现在计算x的另一个函数
x.grad.zero_()
y = x.sum() # 0 + 1 + 2 + 3
y.backward()
print(y,x.grad == 1)

# 非标量变量的反向传播。深度学习中，我们的目的不是计算微分矩阵，而是单独计算批量中每个样本的偏导数之和
x.grad.zero_()
y = x * x
# 等价于y.backward(torch.ones(len(x)))
y.sum().backward() # 转成标量才能求导
print(y.sum(),x.grad,x.grad == 2 * x) # 0 + 1 + 4 + 9

# 分离计算
x.grad.zero_()
y = x * x
# 希望将y视为一个常数, u: 0 1 4 9
u = y.detach() 
z = u * x
# print(y,u,z)
z.sum().backward()
print(x.grad,z.sum(),x.grad == u)

def f(a):
    b = a * 2
    while b.norm() < 1000:
        b = b * 2
    if b.sum() > 0:
        c = b
    else:
        c = 100 * b
    return c

a = torch.randn(size=(), requires_grad=True)
d = f(a)
d.backward()

a.grad == d / a
