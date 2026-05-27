#include <stdio.h>
void exchange(int *p1,int *p2,int *p3)
{
	void swap(int *q1,int *q2);
	if(*p1>*p2){
		swap(p1,p2);
	}
	if(*p1>*p3){
		swap(p1,p3);
	}
	if(*p2>*p3){
		swap(p2,p3);
	}
}

void swap(int *q1,int *q2)
{
	int q;
	q=*q1;
	*q1=*q2;
	*q2=q;
}

int main()
{
	int n1,n2,n3;
	int *p1,*p2,*p3;
	printf("Please input three integers n1,n2,n3:");
	scanf("%d,%d,%d",&n1,&n2,&n3);
	p1=&n1;
	p2=&n2;
	p3=&n3;
	exchange(p1,p2,p3);
	printf("The new order id:%d %d %d\n",n1,n2,n3);
	return 0;
}