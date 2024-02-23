import time
import torch
from matplotlib import pyplot as plt
from d2l import torch as d2l
from _5 import Accumulator, Animator
from _5_1 import load_data_fashion_mnist
from _5_2 import accuracy, softmax, evaluate_accuracy as _evaluate_accuracy


def cross_entropy(y_hat, y):
    return -torch.log(y_hat[range(len(y_hat)), y])


def evaluate_accuracy(net, data_iter):  # @save
    metric = _evaluate_accuracy(net, test_iter)
    return metric[0] / metric[1]


def train_epoch_ch3(net, train_iter, loss, updater):  # @save
    """训练模型一个迭代周期（定义见第3章）"""
    begin = time.time()
    # 将模型设置为训练模式
    if isinstance(net, torch.nn.Module):
        net.train()
    # 训练损失总和、训练准确度总和、样本数
    metric = Accumulator(3)
    for X, y in train_iter:
        # 计算梯度并更新参数
        y_hat = net(X)
        l = loss(y_hat, y)
        if isinstance(updater, torch.optim.Optimizer):
            # 使用PyTorch内置的优化器和损失函数
            updater.zero_grad()
            l.mean().backward()
            updater.step()
        else:
            # 使用定制的优化器和损失函数
            l.sum().backward()
            updater(X.shape[0])
        metric.add(float(l.sum()), accuracy(y_hat, y), y.numel())

    print("epoch cost", time.time() - begin)
    # 返回训练损失和训练精度
    return metric[0] / metric[2], metric[1] / metric[2]


def train_ch3(net, train_iter, test_iter, loss, num_epochs, updater):  # @save
    """训练模型（定义见第3章）"""
    animator = Animator(
        xlabel="epoch",
        xlim=[1, num_epochs],
        ylim=[0.3, 0.9],
        legend=["train loss", "train acc", "test acc"],
    )
    for epoch in range(num_epochs):
        train_metrics = train_epoch_ch3(net, train_iter, loss, updater)
        test_acc = evaluate_accuracy(net, test_iter)
        animator.add(epoch + 1, train_metrics + (test_acc,))
    train_loss, train_acc = train_metrics
    assert train_loss < 0.5, train_loss
    assert train_acc <= 1 and train_acc > 0.7, train_acc
    assert test_acc <= 1 and test_acc > 0.7, test_acc


if __name__ == "__main__":

    # Check that MPS is available
    if not torch.backends.mps.is_available():
        if not torch.backends.mps.is_built():
            print(
                "MPS not available because the current PyTorch install was not "
                "built with MPS enabled."
            )
        else:
            print(
                "MPS not available because the current MacOS version is not 12.3+ "
                "and/or you do not have an MPS-enabled device on this machine."
            )

    device = torch.device("mps")

    batch_size = 256
    _train_iter, _test_iter = load_data_fashion_mnist(batch_size, device=device)
    train_iter = [[X.to(device=device), y.to(device=device)] for X, y in _train_iter]
    test_iter = [[X.to(device=device), y.to(device=device)] for X, y in _test_iter]

    num_inputs = 784
    num_outputs = 10

    # 768行，10列 随机权重
    W = torch.normal(
        0, 0.01, size=(num_inputs, num_outputs), requires_grad=True, device=device
    )
    b = torch.zeros(num_outputs, requires_grad=True, device=device)

    def net(X: torch.Tensor):
        # print(X.shape, W.shape)  # torch.Size([256, 1, 28, 28]), torch.Size([784, 10])
        return softmax(
            torch.matmul(X.reshape((-1, W.shape[0])), W) + b
        )  # 行自动为256，列为784， [256,784] * [784,10] = [256,10]

    lr = 0.1

    def updater(batch_size):
        return d2l.sgd([W, b], lr, batch_size)

    num_epochs = 10
    train_ch3(net, train_iter, test_iter, cross_entropy, num_epochs, updater)

    plt.show()
