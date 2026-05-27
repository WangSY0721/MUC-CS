#include <stdio.h>
int main()
{
	int m,n,sum=0;
	printf("Please input two integers(m<n):");
	scanf("%d,%d",&m,&n);
	do{
		if(m%2==0){
			sum+=m;	
		}
		m++;
	}while(m<=n);
	printf("The sum of even number from m to n is:%d\n",sum);
	return 0;
}