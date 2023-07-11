#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#define type int

typedef struct node
{
	int data;
	struct node* next;
}stack;

void Push(stack **s,int data);
int Pop(stack** s);
void Destroy(stack** s);
int  Empty(stack** s);
//////////////栈

void Push(stack **s,type data)//传入栈地址和入栈的数据
{
	stack* p = (stack*)malloc(sizeof(stack));
	if (!(*s))
	{
		(*s) = p; (*s)->data = data;
		(*s)->next = NULL;
	}
	else {
		p->next = (*s); (*s) = p;(*s)->data = data;
	}
}
type Pop(stack** s)//函数传参，传的是拷贝//出栈后，将值弹出
{
	stack* p = *s;
    if (!p)return 0;
	*s= (*s)->next;
    p->next=NULL;
	return p->data;
}

void Destroy(stack** s)
{  
    stack *p=*s;
    assert(p);
    while(p)
    {p=(*s)->next;
        free(*s);
        *s=p;
    }
    p=NULL;
}

int  Empty(stack** s)
{
return (*s)==NULL;
}




//test main
int main()
{
stack* u=NULL;//很重要
for(int i=0;i<10;i++)
Push(&u,i);
while(u)
printf("%d,",Pop(&u));

//Destroy(&u);
printf("\n%d",Empty(&u));
    return 0;
}