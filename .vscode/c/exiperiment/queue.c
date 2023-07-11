#include <stdio.h>
#include <malloc.h>
#define ture 1
#define false 0
#define N 5
int flag = 0;
typedef struct
{
	int data[N];
	int front, rear;
}queue_type;


int Enqueue(queue_type* q, int m);
int Dequeue(queue_type* q);
int show(queue_type q);
int empty(queue_type *q);
int main()
{

queue_type q={{0},0,0};
printf("please input 6 nums:\n");
int m=0;
while(1)
{ 
scanf_s("%d",&m);
if(!Enqueue(&q,m))
break ;
}show(q);
 printf("3 nums out:\n");
Dequeue(&q);Dequeue(&q);Dequeue(&q);
show(q);
printf("please input 4 num:\n");
while(1)
{ 
 scanf_s("%d",&m);
if(!Enqueue(&q,m))
break ;
}show(q);
printf("5 nums out:\n");
for(int i=0;i<6;i++)
 { 
 if(!Dequeue(&q))
break ;
}show(q);
printf("2 nums in:\n");
Enqueue(&q,88);Enqueue(&q,88);
show(q);
    return 0;
}
int Enqueue(queue_type* q, int m)//进队
{
	if (flag) {
		printf_s("full!error!!"); return false;
	}
    if (q->front == (q->rear + 1) % N)
		flag = 1;
		q->data[q->rear] = m;
        q->rear = (q->rear + 1) % N;
		return ture;
}
int Dequeue(queue_type* q)//出队
{
	if (empty(q)) { printf_s("error!"); 
	return false; }
	flag = 0;
    int value = q->data[q->front];
	q->front = (q->front + 1) %N;
	return value;
}
int empty(queue_type *q)
{if((q->rear)%N== q->front&&!flag)
return ture;
return false;
}
int show(queue_type q)
{
	if(empty(&q))
		return false;
	else {int i=q.front;
        if(flag)
        {
            int n=N;
        while(n--)
        {  
      printf_s("%d,", q.data[i]);
        i=(i+1)%N;
        }
        }
        else{
		while(i!=q.rear)
        { 
			printf_s("%d,", q.data[i]);
            i=(i+1)%N;
        }
	}
	printf_s("\n");
	return ture;
}
}