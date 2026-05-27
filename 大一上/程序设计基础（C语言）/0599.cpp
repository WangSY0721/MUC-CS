#include <stdio.h>
int main()
{
	int m,n,sum=0;
	printf("Please input two integers(m<n):");
	scanf("%d,%d",&m,&n);
	printf("The numbers from m to n that are divisible by 3 or 4 are:");
	while(m<=n){
		if(m%3==0||m%4==0){
			printf("%d ",m);	
		}
		m++;
	}
	return 0;
}