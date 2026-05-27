#include <stdio.h>
#define N 8
int main()
{
	int i,j,k;
	float a[N];
	printf("please input %d numbers:\n",N);
	for(i=0;i<N;i++){
		scanf("%f",&a[i]);
	}
	for(j=0;j<N-1;j++){
		for(i=0;i<N-1-j;i++){
			
			if(a[i]<=a[i+1]){
				k=a[i];
				a[i]=a[i+1];
				a[i+1]=k;
			}
		}
	}
	
	for(i=0;i<N;i++){
		printf("%f ",a[i]);
	}
	printf("\n");
	return 0;
}