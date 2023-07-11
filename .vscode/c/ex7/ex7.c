#include <stdio.h>
#define true 1;
#define false 0;
#define MAX 10

void Simple_Sort(int *num);
void Insert_Sort(int *num);
void Bubble_Sort(int *num);
void Show(int *num);
void Swap(int *num,int i,int j);
int main()
{
//513,87,512,61,908,170,897,275,653,462
int num1[MAX]={513,87,512,61,908,170,897,275,653,462};
printf("this is Simple_Sort:\n");
printf("----------------------------\n");
Simple_Sort(num1);
printf("----------------------------\n");
printf("end!\n\n\n");

//Show(num1);
printf("this is Insert_Sort:\n");
printf("----------------------------\n");
int num2[MAX]={513,87,512,61,908,170,897,275,653,462};
Insert_Sort(num2);
printf("----------------------------\n");
printf("end!\n\n\n");

// Show(num2);
printf("this is Bubble_Sort:\n");
printf("----------------------------\n");
int num3[MAX]={513,87,512,61,908,170,897,275,653,462};
Bubble_Sort(num3);
printf("----------------------------\n");
printf("end!\n\n\n");
//Show(num3);
    return 0;
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
void Simple_Sort(int *num)
{
for(int i=0;i<MAX;i++)
{
    int MIN=i;
    for(int j=i+1;j<MAX;j++)
        {
        if(num[j]<num[MIN])
        MIN=j;
        }
    if(MIN!=i)
    {
    Swap(num,MIN,i);
    }
    printf("The %d the time:\n",i+1);
    Show(num);
}
}

void Insert_Sort(int *num)
{
for(int i=0;i<MAX;i++)
{ 
int key=num[i];
int j=i-1;
while(j>=0&&num[j]>key)
    {
    num[j+1]=num[j];
    j--;
    }
num[j+1]=key;
printf("The %d the time:\n",i+1);
Show(num);
}
}
void Bubble_Sort(int *num)
{
for(int i=0;i<MAX-1;i++)
{int flag=0;
    for(int j=0;j<MAX-i-1;j++)
    {
        if(num[j]>num[j+1])
           { Swap(num,j+1,j);
           flag=1;
           }
    }
    if(!flag)
        break;
    printf("The %d the time:\n",i+1);
    Show(num);
}
}