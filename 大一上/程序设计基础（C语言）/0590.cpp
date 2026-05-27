#include <stdio.h>
int main()
{
	int m,n,sum=0;
	printf("Please input two integers(m<n):");
	scanf("%d,%d",&m,&n);
	while(m<=n){
		sum+=m;
		m++;
	}
	printf("The sum from m to n is:%d\n",sum);
	return 0;
}