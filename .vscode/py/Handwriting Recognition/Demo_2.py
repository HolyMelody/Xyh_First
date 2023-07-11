import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
 # 定义数据预处理：数据标准化
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
 # 加载数据集：下载MNIST数据集，进行数据预处理
train_dataset = datasets.MNIST('data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST('data', train=False, download=True, transform=transform)
 # 定义数据加载器：加载训练集和测试集
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)
 # 定义模型：三层卷积神经网络
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 第一层卷积层：输入通道为1，输出通道为10，卷积核大小为5x5
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        # 第二层卷积层：输入通道为10，输出通道为20，卷积核大小为5x5
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        # 全连接层1：输入节点数为320，输出节点数为50
        self.fc1 = nn.Linear(320, 50)
        # 全连接层2：输入节点数为50，输出节点数为10
        self.fc2 = nn.Linear(50, 10)
     # 前向传播函数
    def forward(self, x):
        # 第一层卷积层：卷积+池化
        x = nn.functional.relu(nn.functional.max_pool2d(self.conv1(x), 2))
        # 第二层卷积层：卷积+池化
        x = nn.functional.relu(nn.functional.max_pool2d(self.conv2(x), 2))
        # 将多维的输入张量视为一维，以便送到全连接层
        x = x.view(-1, 320)
        # 全连接层1：ReLU激活函数
        x = nn.functional.relu(self.fc1(x))
        # 全连接层2：softmax激活函数，输出10个类别的概率值
        x = self.fc2(x)
        return nn.functional.log_softmax(x, dim=1)
 # 初始化模型和优化器
# 模型初始化
model = Net()
# 优化器初始化
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
 # 训练函数
def train(epoch):
    # 训练模式
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        # 清零梯度缓存
        optimizer.zero_grad()
        # 前向传播
        output = model(data)
        # 计算损失
        loss = nn.functional.nll_loss(output, target)
        # 反向传播
        loss.backward()
        # 更新参数
        optimizer.step()
        # 每100次迭代输出一次信息
        if batch_idx % 100 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
 # 测试函数
def test():
    # 测试模式
    model.eval()
    # 初始化测试集损失和正确分类样本计数
    test_loss = 0
    correct = 0
    with torch.no_grad():
        # 对测试集进行测试
        for data, target in test_loader:
            # 前向传播
            output = model(data)
            # 计算测试损失
            test_loss += nn.functional.nll_loss(output, target, reduction='sum').item()
            # 判断分类是否正确
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
    # 计算平均测试损失和测试准确率
    test_loss /= len(test_loader.dataset)
    print('Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
 # 训练和测试模型：训练10个epochs
for epoch in range(1, 11):
    train(epoch)
    test()