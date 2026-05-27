#include <stdio.h>
#define N 3
int main()
{
	int a[N][N],sum=0;
	int i,j;
	printf("Please enter a matrix:\n");
	for(i=0;i<N;i++){
		for(j=0;j<N;j++){
			scanf("%3d",&a[i][j]);
		}
	}
	for(i=0;i<N;i++){
		sum+=a[i][i];
	}
	printf("sum=%3d\n",sum);
	return 0;
}