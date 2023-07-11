'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-05-10 22:15:53
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-05-10 22:46:04
FilePath: \.vscode\py\Learning_Test\5.10.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
m=10
y_pred=[1,-1,-1,1,1,1,1,-1,-1,1] 
y     =[1,1,1,-1,-1,-1,1,-1,1,1]

w = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,.10]   
err = w[(y_pred != y)]
#errw=err.sum()
print(err)  
#print(errw)
