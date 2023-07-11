from collections import defaultdict




# n=int(input())#最大邻居数
# e=int(input())#边数
# s=int(input())#源点
# t=int(input())#目标
# Graph=[[0]*50 for i in range(50)]#边权图




I=99999    #  1  2  3  4  5  6 7 8 9 10 11 12 13
Matrix =    [[I, 4, I, I, I, I,I,I,I, I, I, I,I],
             [4, I, 5, 1, 2, I,I,I,I, I, I, I,I],
             [I, 5, I, 4, I, I,I,I,I, 2, I, I,2],
             [I, 1, 4, I, I, I,I,I,I, I, I, I,I],
             [I, 2, I, I, I, 4,2,2,2, I, I, I,I],
             [I, I, I, I, 4, I,I,I,I, I, I, I,I],
             [I, I, I, I, 2, I,I,I,I, I, I, I,I],
             [I, I, I, I, 2, I,I,I,2, I, I, I,I],
             [I, I, I, I, 2, I,I,2,I, 2, 2, I,I],
             [I, I, 2, I, I, I,I,I,I, 2, 2, I,2],
             [I, I, I, I, I, I,I,I,I, I, I, 2,I],
             [I, I, I, I, I, I,I,I,I, I, I, I,2],
             [I, I, I, I, I, I,I,I,I, I, I, I,I]]


edges=[]
for i in range(len(Matrix)):
   for j in range(len(Matrix[0])):
        if(Matrix[i][j]!=I and i!=j):
            edges.append([i+1,j+1,Matrix[i][j]])
 
print(edges)