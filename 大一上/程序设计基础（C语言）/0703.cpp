#include <stdio.h>
#include <math.h>
int prime(int n)
{
	int flag=0;
	for(int i=2;i<sqrt(n);i++){
		if(n%i==0){
			flag=1;
		}
	}
	return flag;
}

int main()
{
	int n;
	printf("Please input an n:");
	scanf("%d",&n);
	if(prime(n)){
		printf("%d is not a prime.\n",n);
	}
	else{
		printf("%d is a prime.\n",n);
	}
	return 0;
}