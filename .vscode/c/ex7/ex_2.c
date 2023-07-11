#include <stdio.h>
#define MAX 9
void Quick_sort(int *num,int low,int high);
void Show(int *num);
void Swap(int *num,int i,int j);
int main()
{
int num[MAX]={14,17,53,35,9,37,68,21,46};
Quick_sort(num,0,MAX);
Show(num);
return 0;
}
void Quick_sort(int *num,int low,int high)
{
if(low>high)
return;
int i=low,j=high;
int base=num[low];
while(i!=j)
{
   while(num[j]>=base&&i<j)
        j--;
   while(num[i]<=base&&i<j)
        i++;
    if(i<j)
        Swap(num,i,j);//low_i指针和high_j指针数据交换
}
    printf("g:%d\n",num[i]);
    num[low]=num[i];//low_i指针所指的数与base交换
    num[i]=base;
    Show(num);
Quick_sort(num,low,i-1);
Quick_sort(num,i+1,high);
}

void Show(int *num)
{
for(int i=0;i<MAX;i++)
    printf("%d ",num[i]);
printf("\n");
}

void Swap(int *num,int i,int j)
{
        int temp=0;
        temp=num[j];
        num[j]=num[i];
        num[i]=temp;
}

