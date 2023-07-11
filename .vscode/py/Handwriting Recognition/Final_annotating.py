import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

# 定义数据预处理
train_transform = transforms.Compose([
    transforms.RandomRotation(10),  # 随机旋转
    transforms.RandomAffine(degrees=10, translate=(0.1, 0.1), scale=(0.9, 1.1), shear=10),  # 随机仿射变换
    transforms.ToTensor(),  # 转换为张量
    transforms.Normalize((0.1307,), (0.3081,))  # 标准化
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# 加载数据集
train_dataset = datasets.MNIST('data', train=True, download=True, transform=train_transform)
test_dataset = datasets.MNIST('data', train=False, download=True, transform=test_transform)

# 定义数据加载器
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 第一个卷积层，输入通道为1，输出通道为16，卷积核大小为5，步长为1，填充为2
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1, padding=2)
        
        # 第二个卷积层，输入通道为16，输出通道为32，卷积核大小为5，步长为1，填充为2
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2)
        
        # 第三个卷积层，输入通道为32，输出通道为64，卷积核大小为5，步长为1，填充为2
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, stride=1, padding=2)
        
        # 全连接层1，输入尺寸为64 * 7 * 7，输出尺寸为128
        self.fc1 = nn.Linear(in_features=64 * 7 * 7, out_features=128)
        
        # 全连接层2，输入尺寸为128，输出尺寸为10
        self.fc2 = nn.Linear(in_features=128, out_features=10)

    def forward(self, x):
        # 输入：[batch_size, 1, 28, 28]
        x = self.conv1(x)  # [batch_size, 16, 28, 28]
        x = nn.functional.relu(x)  # ReLU激活函数
        x = nn.functional.max_pool2d(x, kernel_size=2, stride=2)  # 最大池化层，缩小图像尺寸为[batch_size, 16, 14, 14]
        
        x = self.conv2(x)  # [batch_size, 32, 14, 14]
        x = nn.functional.relu(x)
        x = nn.functional.max_pool2d(x, kernel_size=2, stride=2)  # 最大池化层，缩小图像尺寸为[batch_size, 32, 7, 7]
        
        x = self.conv3(x)  # [batch_size, 64, 7, 7]
        x = nn.functional.relu(x)
        
        x = x.view(-1, 64 * 7 * 7)  # 展平张量
        
        x = self.fc1(x)  # [batch_size, 128]
        x = nn.functional.relu(x)
        x = nn.functional.dropout(x, p=0.5, training=self.training)  # dropout防止过拟合
        
        x = self.fc2(x)  # [batch_size, 10]
        
        return nn.functional.log_softmax(x, dim=1)  # log_softmax作为输出激活函数

# 初始化模型和优化器
model = Net()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练函数
def train(epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()  # 清除梯度
        output = model(data)  # 前向传播
        loss = nn.functional.nll_loss(output, target)  # 计算损失
        loss.backward()  # 反向传播
        optimizer.step()  # 更新参数
        
        if batch_idx % 100 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))

# 测试函数
def test():
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            test_loss += nn.functional.nll_loss(output, target, reduction='sum').item()
            pred = output.argmax(dim=1, keepdim=True)  # 获取预测值
            correct += pred.eq(target.view_as(pred)).sum().item()  # 计算正确分类的数量
    
    test_loss /= len(test_loader.dataset)
    print('Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

# 训练和测试模型
for epoch in range(1, 11):
    train(epoch)
    test()