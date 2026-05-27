#include <stdio.h>
int main ()
{
	int a,b,c,n;
	printf("parcissus numbers are:");
	for(n=100;n<1000;n++){
		a=n/100;
		b=n/10-a*10;
		c=n%10;
		if(n==a*a*a+b*b*b+c*c*c){
			printf("%d ",n);
		}
	}
	printf("\n");
	return 0;
}