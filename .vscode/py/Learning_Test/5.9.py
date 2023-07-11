import copy


a=[1,2,3]
b=a

c=copy.copy(a)  # 浅拷贝
d=copy.deepcopy(a)   # 深拷贝
# print(id(d))
# pr