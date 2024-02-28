import math
import numpy as np
import torch
from torch import nn
from d2l import torch as d2l
from utils.d2l.commons import Animator


max_degree = 20  # 多项式的最大阶数
n_train, n_test = 100, 100  # 训练和测试数据集大小
true_w = np.zeros(max_degree)  # 分配大量的空间
true_w[0:4] = np.array([5, 1.2, -3.4, 5.6])
""" 使用以下三阶多项式来生成训练和测试数据的标签： """
features = np.random.normal(size=(n_train + n_test, 1)) # 200行，1列
print(features.shape)
np.random.shuffle(features)
poly_features = np.power(features, np.arange(max_degree).reshape(1, -1)) # x^0 + x^1, x^2, x^3, x^4,... x^19
print(poly_features.shape) # 扩展为 200行，20列
for i in range(max_degree): # 分母
    poly_features[:, i] /= math.gamma(i + 1)  # gamma(n)=(n-1)!
# labels的维度:(n_train+n_test,)
labels = np.dot(poly_features, true_w) # 系数 , 0*x^4,... 0*x^19
labels += np.random.normal(scale=0.01, size=labels.shape)


# NumPy ndarray转换为tensor
true_w, features, poly_features, labels = [
    torch.tensor(x, dtype=torch.float32)
    for x in [true_w, features, poly_features, labels]
]


print(features[:2], poly_features[:2, :], labels[:2])


def evaluate_loss(net, data_iter, loss):  # @save
    """评估给定数据集上模型的损失"""
    metric = d2l.Accumulator(2)  # 损失的总和,样本数量
    for X, y in data_iter:
        out = net(X)
        y = y.reshape(out.shape)
        l = loss(out, y)
        metric.add(l.sum(), l.numel())
    return metric[0] / metric[1]


def train(train_features, test_features, train_labels, test_labels, num_epochs=400):
    loss = nn.MSELoss(reduction="none")
    input_shape = train_features.shape[-1]
    # 不设置偏置，因为我们已经在多项式中实现了它
    net = nn.Sequential(nn.Linear(input_shape, 1, bias=False))
    batch_size = min(10, train_labels.shape[0]) # 100 中取10
    train_iter = d2l.load_array(# 构造 X， y迭代， 10行， 列依次为 4，2，20
        (train_features, train_labels.reshape(-1, 1)), batch_size
    )
    test_iter = d2l.load_array(
        (test_features, test_labels.reshape(-1, 1)), batch_size, is_train=False
    )
    trainer = torch.optim.SGD(net.parameters(), lr=0.01)
    animator = Animator(
        xlabel="epoch",
        ylabel="loss",
        yscale="log",
        xlim=[1, num_epochs],
        ylim=[1e-3, 1e2],
        legend=["train", "test"],
    )
    for epoch in range(num_epochs):
        d2l.train_epoch_ch3(net, train_iter, loss, trainer)# 输入计算出y_hat后，和y计算出损失，再计算w梯度，最后更新w
        if epoch == 0 or (epoch + 1) % 20 == 0:
            animator.add(
                epoch + 1,
                (
                    evaluate_loss(net, train_iter, loss),
                    evaluate_loss(net, test_iter, loss),
                ),
            )
    print("weight:", net[0].weight.data.numpy())

""" 三阶多项式函数拟合(正常) """
# 从多项式特征中选择前4个维度，即1,x,x^2/2!,x^3/3!
train(poly_features[:n_train, :4], poly_features[n_train:, :4],
      labels[:n_train], labels[n_train:])


""" 线性函数拟合(欠拟合) """
# 从多项式特征中选择前2个维度，即1和x
train(poly_features[:n_train, :2], poly_features[n_train:, :2],
      labels[:n_train], labels[n_train:])


""" 高阶多项式函数拟合(过拟合) """
# 从多项式特征中选取所有维度
train(poly_features[:n_train, :], poly_features[n_train:, :],
      labels[:n_train], labels[n_train:], num_epochs=1500)

