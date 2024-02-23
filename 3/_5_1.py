import numpy as np
import torch
import torchvision
from torch.utils import data
from torchvision import transforms

# from d2l import torch as d2l
from matplotlib import pyplot as plt


def get_dataloader_workers():
    """Use 4 processes to read the data."""
    return 2


def load_data_fashion_mnist(batch_size: int, resize=None):
    """Download the Fashion-MNIST dataset and then load it into memory."""
    trans = [transforms.ToTensor()]
    if resize:
        trans.insert(0, transforms.Resize(resize))
    trans = transforms.Compose(trans)
    mnist_train = torchvision.datasets.FashionMNIST(  # fashion集 数据
        root="../data", train=True, transform=trans, download=False
    )
    mnist_test = torchvision.datasets.FashionMNIST(
        root="../data", train=False, transform=trans, download=False
    ) 

    return (
        data.DataLoader(
            mnist_train, batch_size, shuffle=True, num_workers=get_dataloader_workers()
        ),
        data.DataLoader(
            mnist_test, batch_size, shuffle=False, num_workers=get_dataloader_workers()
        ),
    )


def get_fashion_mnist_labels(labels):
    """Return text labels for the Fashion-MNIST dataset."""
    text_labels = [
        "t-shirt",
        "trouser",
        "pullover",
        "dress",
        "coat",
        "sandal",
        "shirt",
        "sneaker",
        "bag",
        "ankle boot",
    ]
    return [text_labels[int(i)] for i in labels]


def show_images(imgs, num_rows, num_cols, titles=None, scale=1.5):
    """Plot a list of images."""
    figsize = (num_cols * scale, num_rows * scale + 1)  # width height
    _, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    print(axes.shape)
    axes = axes.flatten()
    for i, (ax, img) in enumerate(zip(axes, imgs)):
        if torch.is_tensor(img):
            # Tensor Image
            ax.imshow(img.numpy())
        else:
            # PIL Image
            ax.imshow(img)
        # ax.axes.get_xaxis().set_visible(False)
        # ax.axes.get_yaxis().set_visible(False)
        if titles:
            ax.set_title(titles[i])
    return axes


# 多进程，只在主进程执行
if __name__ == "__main__":

    batch_size = 256
    train_iter, test_iter = load_data_fashion_mnist(batch_size)

    def predict_ch3(test_iter, n=6):  # @save
        """预测标签（定义见第3章）"""
        for X, y in test_iter:
            # print(X.shape, y.shape) # [256, 1, 28, 28] [batch_size, 通道数(灰度图为1), w, h]
            break  # 第一批
        trues = get_fashion_mnist_labels(y)
        # preds = d2l.get_fashion_mnist_labels(net(X).argmax(axis=1))
        # titles = [true + "\n" + pred for true, pred in zip(trues, preds)]
        titles = [true + "\n" for true in trues]
        show_images(X[0:n].reshape((n, 28, 28)), 1, n, titles=titles[0:n])  # 显示已=6个

    predict_ch3(test_iter)

    plt.show()
