#include <stdio.h>
#define true 1;
#define false 0;
int orderfind(int *a,int length,int data);
int twofind(int *a,int length,int data);
int main()
{
int a[8]={3,10,13,17,40,43,50,70};
int data[2]={43,5};
int length=sizeof(a)/sizeof(a[0]);

for(int i=0;i<2;i++)
{
twofind(a,length,data[i]);
orderfind(a,length,data[i]);
}
return 0;
}

int orderfind(int *a,int length,int data)
{
printf("this is orderfind:\n");
int n=length;
    for(int i=0;i<n;i++)
    {
        if(a[i]==data)
        {
        printf("'%d' is in  position '%d'\n",data,i+1);
         return true;
        }
    }
    printf("%d is not in\n",data);
    return false;
}
int twofind(int *a,int length,int data)
{
printf("this is twofind:\n");
int n=length;
int l=0;int r=n-1;
while(l<=r)
{
   int mid=(l+r)/2;
    if(data==a[mid])
        {   printf("'%d' is in position '%d'\n",data,mid+1);
            return true;}
    else if(data>a[mid])
       { 
        l=mid+1;}
    else if(data<a[mid])
        { 
            r=mid-1;}
}   printf("%d is not in\n",data);
    return false;
}
