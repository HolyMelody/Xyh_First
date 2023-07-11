#include<bits/stdc++.h>
using namespace std;
#define MAX 9
void mergearray(int a[],int first,int mid,int last,int temp[]);
bool MergeSort(int a[], int n) ;
void Show(int *num);
int main()
{
	// int a[1005];
	// int n;
	// scanf("%d",&n);
	// for(int i=0;i<n;i++)
	// 	scanf("%d",&a[i]);
	int num[MAX]={14,17,53,35,9,37,68,21,46};
	MergeSort(num,MAX);
} 

void mergearray(int a[],int first,int mid,int last,int temp[])	//将两个有序数组合并排序 
{
	int i=first,j=mid+1;
	int m=mid,n=last;
	int k=0;
	while(i<=m&&j<=n)
	{
		if(a[i]<a[j])
			temp[k++]=a[i++];
		else
			temp[k++]=a[j++];
	}
	while(i<=m)//防止一边放置完，另一边没有
		temp[k++]=a[i++];
	while(j<=n)
		temp[k++]=a[j++];
	for(i=0;i<k;i++)
		a[first+i]=temp[i];
}
 
void mergesort(int a[],int first,int last,int temp[])	//将两个任意数组合并排序 
{
	if(first<last)
	{
		int mid=(first+last)/2;
		mergesort(a,first,mid,temp);	//左边有序 
		mergesort(a,mid+1,last,temp);	//右边有序 
		mergearray(a,first,mid,last,temp);	//再将两个有序数组合并 
		Show(a);
	}
}
 
bool MergeSort(int a[], int n)  
{  
    int *p = new int[n];  //分配一个有n个int型元素的数组所占空间，并将该数组的第一个元素的地址赋给int *型指针p。
    if (p == NULL)  
        return false;  
    mergesort(a, 0, n - 1, p);  
    delete[] p;  
    return true;  
} 
void Show(int *num)
{
for(int i=0;i<MAX;i++)
    printf("%d ",num[i]);
printf("\n");
}