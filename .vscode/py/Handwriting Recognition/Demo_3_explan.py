"""
该程序使用PyTorch框架实现一个三层卷积神经网络（CNN）模型，用于训练和测试MNIST手写数字数据集。
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
 # 将数据转换为张量并对其进行归一化处理
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
 # 加载训练和测试数据集
train_dataset = datasets.MNIST('data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST('data', train=False, download=True, transform=transform)
 # 创建数据加载器
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)
 # 定义一个卷积神经网络
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 定义一个卷积层，输入通道数为1，输出通道数为32，卷积核大小为3，padding为1
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        # 定义一个批量归一化层
        self.bn1 = nn.BatchNorm2d(32)
        # 定义一个卷积层，输入通道数为32，输出通道数为64，卷积核大小为3，padding为1
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # 定义一个批量归一化层
        self.bn2 = nn.BatchNorm2d(64)
        # 定义一个卷积层，输入通道数为64，输出通道数为128，卷积核大小为3，padding为1
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        # 定义一个批量归一化层
        self.bn3 = nn.BatchNorm2d(128)
        # 定义一个全连接层，输入特征数为2048，输出特征数为512
        self.fc1 = nn.Linear(2048, 512)
        # 定义一个全连接层，输入特征数为512，输出特征数为10（类别数）
        self.fc2 = nn.Linear(512, 10)
    def forward(self, x):
        # 在第一层卷积后应用ReLU激活函数
        x = nn.functional.relu(self.bn1(self.conv1(x)))
        # 对结果进行2x2的最大池化
        x = nn.functional.max_pool2d(x, 2)
        # 在第二层卷积后应用ReLU激活函数
        x = nn.functional.relu(self.bn2(self.conv2(x)))
        # 对结果进行2x2的最大池化
        x = nn.functional.max_pool2d(x, 2)
        # 在第三层卷积后应用ReLU激活函数
        x = nn.functional.relu(self.bn3(self.conv3(x)))
        # 对结果进行2x2的最大池化
        x = nn.functional.max_pool2d(x, 2)
        # 重新整形数据以适应全连接层输入
        x = x.view(x.size(0), -1)
        # 在第一层全连接层后应用ReLU激活函数
        x = nn.functional.relu(self.fc1(x))
        # 输出层
        x = self.fc2(x)
        # 应用log softmax激活函数
        return nn.functional.log_softmax(x, dim=1)
 # 初始化模型
model = Net()
# 定义一个优化器
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
 # 训练模型
def train(epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = nn.functional.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 100 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
 # 测试模型
def test():
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            test_loss += nn.functional.nll_loss(output, target, reduction='sum').item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
    test_loss /= len(test_loader.dataset)
    print('Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
 # 训练并测试模型，共20个周期
for epoch in range(1, 21):
    train(epoch)
    test()