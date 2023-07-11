#include<stdio.h>
#include<stdbool.h>
#include<stdlib.h>
#include<assert.h>

typedef struct Tree{
 
 int data;					//	存放数据域
 struct Tree *lchild;			//	遍历左子树指针
 struct Tree *rchild;			//	遍历右子树指针
 int flag;
}Tree,*BitTree;

typedef struct node
{
	BitTree data;
	struct node* next;
}stack;
//后序遍历

 int MAX_NODE=9;
int CreatBSTree(BitTree *t,int data);
int CreatBSTree1(BitTree *t,int data);
void ShowXianXu(BitTree T);
void ShowZhongXu(BitTree T);
void ShowHouXu(BitTree T);
void PreOrder(BitTree T);
void MidOrder(BitTree T);
void Postorder(BitTree T );
int depth(BitTree T);
int nodenums(BitTree T);
int leafnums(BitTree T);

void Push(stack **s,BitTree data);
BitTree Pop(stack** s);
void Destroy(stack** s);
int  Empty(stack** s);

int main()
{
	BitTree S=NULL;
	int data[9]={71,65,40,88,67,90,60,70,77};
	for(int i=0;i<9;i++)
	{
	CreatBSTree(&S,data[i]);		
	}
    printf("-----------递归---------\n");
    printf("先序：");
	ShowXianXu(S);
    // printf("\n");				
    // printf("中序：");
	// ShowZhongXu(S);
    // printf("\n");
    // printf("后序：");
	// ShowHouXu(S);
    // printf("\n");
	// printf("----------非递归--------\n");
    // printf("先序：");
    // PreOrder(S);
    // printf("\n");
    // printf("中序：");
	// MidOrder(S);
    // printf("\n");
    // printf("后序：");
    // Postorder(S);
    // printf("\n");
	// printf("%d",depth(S));
    // printf("\n");
	// printf("nodenums:%d",nodenums(S));
    // printf("\n");
	// printf("leafnums:%d",leafnums(S));
	return 0;	
} 

int CreatBSTree(BitTree *t,int data){
	if(!(*t)){
		(*t)=(BitTree)malloc(sizeof(Tree));
		(*t)->data=data;
		(*t)->rchild=NULL;
		(*t)->lchild=NULL;
	}
	else if(data>(*t)->data){
		CreatBSTree(&((*t)->rchild),data);
	}
	else{
		CreatBSTree(&((*t)->lchild),data);
	}
	return 1;
}

///////////////递归遍历
void ShowXianXu(BitTree T)			//		先序遍历二叉树
{
	if(T==NULL)
	{
		return;
	}
	printf("%d ",T->data);
	ShowXianXu(T->lchild);			//	递归遍历左子树
	ShowXianXu(T->rchild);			//	递归遍历右子树
}

void ShowZhongXu(BitTree T)
{
	if(NULL==T){
		return;
	}
	
	ShowZhongXu(T->lchild);
	printf("%d ", T->data);
	ShowZhongXu(T->rchild);
}


void ShowHouXu(BitTree T)
{
	if(NULL == T){
		return;
	}
	
	ShowHouXu(T->lchild);
	ShowHouXu(T->rchild);
	printf("%d ", T->data);
}
///////////////非递归遍历
void PreOrder(BitTree T) { //树的前序遍历
	stack* s=NULL;
	BitTree p =T;
	while (p||!Empty(&s)) { //当p为空，栈也为空时退出循环
		while (p) {
			printf("%d ",p->data);//访问根结点
			Push(&s, p); //将指针p的节点压入栈中
			p = p->lchild; //遍历左子树
		}
		if (!Empty(&s)) { //栈不为空
			p = Pop(&s); //根结点出栈,相当于回退
			p = p->rchild; //遍历右子树
		}
	}
	Destroy(&s);
}

void MidOrder(BitTree T) { //树的中序遍历
	stack* s=NULL;
	BitTree p =T;
	while (p||!Empty(&s)) { //当p为空，栈也为空时退出循环
		while (p) {
			//printf("%d ",p->data);//访问根结点
			Push(&s, p); //将指针p的节点压入栈中
			p = p->lchild; //遍历左子树
		}
		if (!Empty(&s)) { //栈不为空
			p = Pop(&s); //根结点出栈,相当于回退
			printf("%d ",p->data);
			p = p->rchild; //遍历右子树
		}
	}
	Destroy(&s);
}

void Postorder( BitTree T)
{
	BitTree p;stack* s=NULL;
	if(!T) 
		return;
	p = T;
	while( 1 )
	{
		if(p)//p非空，则入栈，之后p向左走 
		{
			Push(&s,p);
			p = p->lchild;
		}
		else//p为空，则出栈 
		{
			p =Pop(&s);
			//右为空，且flag为真，则访问，之后p置空 
			if( p->rchild==NULL|| p->flag == 1 )
			{
				printf("%d ",p->data );
				p = NULL;
			} 
			else//右非空，则p重新入栈，重复入栈标志flag置为真，之后p向右走
			{
				Push(&s,p);
				p->flag = 1;
				p = p->rchild;
			}
		} 
		if(Empty(&s))//栈为空，则结束遍历
			break;
	}
}




int depth(BitTree T)
{
	int l,r;
if(!T){
		return 0;//初始：叶子结点下的深度为0
	}
else{
	l=depth(T->lchild);
	r=depth(T->rchild);//证明：假定，l和r表示该节点下的深度
	//每次返回时，由该节点下的深度加上本层（1），即为上一层深度
	return l>r?(l+1):(r+1); //回溯时，返回层深
}
}

int nodenums(BitTree T)			//		先序遍历二叉树
{int l,r;
	if(!T)
		return 0;
	else{
	l=nodenums(T->lchild);			
	r=nodenums(T->rchild);
	return l+r+1;
	}
}
int leafnums(BitTree T)			
{int l,r,num;
	if(T==NULL)
		return 0;
	else if(!T->lchild&&!T->rchild)
	return 1;
	else{
		l=leafnums(T->lchild);			
		r=leafnums(T->rchild);
	}
	return l+r;
}







//////////////栈
void Push(stack **s,BitTree data)//传入栈地址和入栈的数据
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
BitTree Pop(stack** s)//函数传参，传的是拷贝//出栈后，将值弹出
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

