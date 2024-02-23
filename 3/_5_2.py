import torch
from matplotlib import pyplot as plt
from typing import Callable
from _5 import Accumulator
from _5_1 import load_data_fashion_mnist, show_images, get_fashion_mnist_labels


def softmax(X):
    X_exp = torch.exp(X)  # [batch_size, 10] 幂
    partition = X_exp.sum(1, keepdim=True)  # [batch_size] 每行幂之和 作为 分母
    return X_exp / partition  # 这里应用了广播机制, [batch_size, 10] 每行和为1


def accuracy(y_hat, y):  # @save
    """计算预测正确的数量"""
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:  # 2维 且 列数大于1
        # print("y_hat.shape", y_hat.dtype, y.dtype, y_hat.shape, y_hat[0])
        y_hat = y_hat.argmax(axis=1)  # 2维变成1维 每行取最大一列, 即取得分类label
        # print("y_hat.shape.", y_hat.shape, y_hat[0], y[0])
    cmp = y_hat.type(y.dtype) == y  # torch.float32 转 torch.int64 对比 true_labels
    # print("cmp", cmp)
    return float(
        cmp.type(y.dtype).sum()
    )  # torch.bool转成torch.int64, 累计batch size中true数目


def evaluate_accuracy(net: Callable[[torch.Tensor], torch.Tensor], data_iter):  # @save
    """计算在指定数据集上模型的精度"""
    if isinstance(net, torch.nn.Module):
        net.eval()  # 将模型设置为评估模式
    metric = Accumulator(2)  # 正确预测数、预测总数
    with torch.no_grad():
        for X, y in data_iter:
            true_num = accuracy(net(X), y)  # 输入X 通过net得到 输出y
            print(true_num)
            metric.add(true_num, y.numel())  # 单次batch size的 true num 和 总数
    return metric


def predict_ch3(test_iter, net: Callable[[torch.Tensor], torch.Tensor], n=6):  # @save
    """预测标签（定义见第3章）"""
    for X, y in test_iter:
        # print(X.shape, y.shape) # [256, 1, 28, 28] [batch_size, 通道数(灰度图为1), w, h]
        break  # 第一批
    trues = get_fashion_mnist_labels(y)
    preds = get_fashion_mnist_labels(net(X).argmax(axis=1))
    titles = [true + "\n" + pred for true, pred in zip(trues, preds)]
    show_images(X[0:n].reshape((n, 28, 28)), 1, n, titles=titles[0:n])  # 显示已=6个


if __name__ == "__main__":

    batch_size = 256
    train_iter, test_iter = load_data_fashion_mnist(batch_size)

    num_inputs = 784
    num_outputs = 10

    # 768行，10列 随机权重
    W = torch.normal(0, 0.01, size=(num_inputs, num_outputs), requires_grad=True)
    b = torch.zeros(num_outputs, requires_grad=True)

    def net(X: torch.Tensor):
        # print(X.shape, W.shape)  # torch.Size([256, 1, 28, 28]), torch.Size([784, 10])
        return softmax(
            torch.matmul(X.reshape((-1, W.shape[0])), W) + b
        )  # 行自动为256，列为784， [256,784] * [784,10] = [256,10]

    predict_ch3(test_iter, net=net)

    metric = evaluate_accuracy(net, test_iter)
    print("evaluate_accuracy", metric[0], metric[1])

    plt.show()
