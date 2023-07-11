import matplotlib.pyplot as plt
import numpy as np



plt.ion()
plt.imshow(image)
plt.title(f'Class:{class_name} Probability:{probability:.3f}')
# 保存
plt.axis('off')
 
# saveDir+os.path.basename(filepath)：d:/test.jpg
plt.savefig(saveDir+os.path.basename(filepath))
    
plt.show(block=False)
plt.pause(1) # 显示1s
plt.close()