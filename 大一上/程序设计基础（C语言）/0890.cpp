#include <stdio.h>
#define N 10
void calculate(int *p)
{
	int sum=0,num=0;
	float avg;
	for(int i=0;i<N;i++){
		sum+=*(p+i);
	}
	avg=sum*1.0/N;
	for(int i=0;i<N;i++){
		if(*(p+i)%2==0){
			num++;
		}
	}
	printf("sum=%d\n",sum);
	printf("avg=%f\n",avg);
	printf("Number of even numbers is %d",num);
}

int main()
{
	int a[N],*p;
	p=a;//p=&a[0];
	printf("Please input 10 integers:");
	for(int i=0;i<N;i++){
		scanf("%d",&a[i]);
	}
	calculate(p);
	return 0;
}