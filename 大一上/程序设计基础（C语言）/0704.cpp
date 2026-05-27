#include <stdio.h>
#define N 3
void move (int a[N][N])
{
	int i,j,k;
	for(i=0;i<N;i++){
		for(j=i+1;j<N;j++){
			k=a[i][j];
			a[i][j]=a[j][i];
			a[j][i]=k;
		}
	}
}

int main()
{
	int a[N][N],i,j;
	printf("please input a matrix:\n");
	for(i=0;i<N;i++){
		for(j=0;j<N;j++){
			scanf("%d",&a[i][j]);
		}
	}
	move (a);
	printf("Now the matrix is:\n");
	for(i=0;i<N;i++){
		for(j=0;j<N;j++){
			printf("%4d",a[i][j]);
		}
		printf("\n");
	}
    return 0;
}