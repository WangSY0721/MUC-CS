#include <stdio.h>
#define N 100
int main()
{
	void input(int *p,int n);
	void minimum(int *p,int *q,int *min,int n);
	void maximum(int *p,int *q,int *max,int n);
	int number[N];
	int *p=number;
	printf("Please input 10 numbers:");
 	input(p,10);
	int *max,*min,*q;
	int temp;
	max=min=p;
	minimum(p,q,min,10);
	maximum(p,q,max,10);
	printf("The new array is:");
	for(q=p;q<p+10;q++){
		printf("%d ",*q);
	}
	printf("\n");
	return 0;
}

void input(int *p1,int n)
{
	for(int i=0;i<n;i++){
		scanf("%d",p1+i);
	}
}

void minimum(int *p,int *q,int *min,int n)
{
	int temp;
	for(q=p+1;q<p+n;q++){
		if(*q<*min){
			min=q;	
		}
	}
	temp=*p;
	*p=*min;
	*min=temp;
}

void maximum(int *p,int *q,int *max,int n)
{
	int temp;
	for(q=p+1;q<p+n;q++){
		if(*q>*max){
			max=q;	
		}
	}
	temp=*(p+n-1);
	*(p+n-1)=*max;
	*max=temp;
}
