#include <stdio.h>
#define N 5
int main()
{
	int a[N],i,k;
	printf("please input %d numbers:",N);
	for(i=0;i<N;i++){
		scanf("%d",&a[i]);
	}
	
	for(i=0;i<N/2;i++){
		k=a[i];
		a[i]=a[N-i-1];
		a[N-i-1]=k;
	}
	
	for(i=0;i<N;i++){
		printf("%d ",a[i]);
	}
	printf("\n");
	return 0;
}