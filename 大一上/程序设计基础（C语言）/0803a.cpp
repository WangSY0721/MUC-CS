#include <stdio.h>
#define N 10
int main()
{
	int number[N];
	printf("Please input %d numbers:",N);
	for(int i=0;i<N;i++){
		scanf("%d",&number[i]);
	}
	int *max,*min,*p;
	int temp;
	max=min=number;
	for(p=number+1;p<number+N;p++){
		if(*p<*min){
			min=p;	
		}
	}
	temp=number[0];
	number[0]=*min;
	*min=temp;
	
	for(p=number+1;p<number+N;p++){
		if(*p>*max){
			max=p;	
		}
	}
	temp=number[N-1];
	number[N-1]=*max;
	*max=temp;
	
	printf("The new array is:");
	for(p=number;p<number+N;p++){
		printf("%d ",*p);
	}
	printf("\n");
	return 0;
}