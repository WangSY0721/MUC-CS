#include <stdio.h>
int main ()
{
	int m,n,p,i,t;
	printf("please input two numbers:");
	scanf("%d,%d",&m,&n);
	if(n<m){
		t=n;
		n=m;
		m=t;
	}
	p=n*m;
	while(m!=0){
		i=n%m;
		n=m;
		m=i;
	}
	printf("the greatest common divisor is:%d\n",n);
	printf("least common multiple is:%d\n",p/n);
	return 0;
}