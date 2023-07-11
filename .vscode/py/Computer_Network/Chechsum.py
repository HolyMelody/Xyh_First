# author: zhujie 
# time: 2020/4/2
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button

def btn_clicked(e):
    number1 = int(textbox_1.text, 2)
    number2 = int(textbox_2.text, 2)
    number3 = int(textbox_3.text, 2)
    sum = bin(number1 + number2)
    # 检查溢出
    if len(sum) > 18:
        sum = sum[3:19]
        sum = int(sum, 2)
        sum += 1
    else:
        sum = sum[2: 18]
        sum = int(sum, 2)
    print(bin(sum))
    sum = bin(sum + number3)
    # 检查溢出
    if len(sum) > 18:
        sum = sum[3:19]
        sum = int(sum, 2)
        sum += 1
    else:
        sum = sum[2: 18]
        sum = int(sum, 2)
    sum ^= 0xffff
    sum = bin(sum)
    print(sum)
    sum = sum[2:18]
    textbox_4 = TextBox(plt.axes([0.3,0.1,0.5,0.075]),"checksum:",initial=sum)

# 初始化GUI
axbox_1 = plt.axes([0.3, 0.9, 0.5, 0.075])
axbox_2 = plt.axes([0.3, 0.7, 0.5, 0.075])
axbox_3 = plt.axes([0.3, 0.5, 0.5, 0.075])
axbtn = plt.axes([0.3, 0.3, 0.3, 0.1])
textbox_1 = TextBox(axbox_1, 'input1:')
textbox_2 = TextBox(axbox_2, "input2:")
textbox_3 = TextBox(axbox_3, "input3:")
button = Button(axbtn, "Calculate Checksum")
# 绑定点击事件
button.on_clicked(btn_clicked)
plt.show()