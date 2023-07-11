#include <stdio.h>
#include<string.h>
#define N 30;


int Hash(char * cp);
void find(char** p,char *s);
int main()
{
char* s[5]={"wujiahong","huge","jack","Jay","gehu"};

char* p[30]={NULL};
for(int i=0;i<5;i++)
{
    int j=Hash(s[i]);
    while(p[j]!=NULL)
    {
        j++;
    }
    p[j]=s[i];
}
for(int i=0;i<30;i++)
printf("%s ",p[i]);
printf("\n");
find(p,"huge");
find(p,"gehu");
find(p,"gheu");
   // printf("%s",p[Hash("huge")]);
    //printf("%s",p[Hash("gehu")+1]);
    return 0;
}

int Hash(char * cp)
{int sum = 0;
int n = strlen(cp);
for(int i = 0 ; i < n; i++)
{sum += (int)*cp;cp ++;} 
sum=sum%N;
return sum;
}

void find(char** p,char *s)
{
int n=Hash(s);
if(!p[n])printf("%s no in!\n",s);
while(strcmp(p[n],s))
{
n++;
if(!p[n])break;
}
if(!p[n]) printf("'%s' is no in!\n",s);
else if(!strcmp(p[n],s))
printf("this '%s' is in position %d \n",s,n);
}