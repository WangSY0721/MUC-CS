#include <stdio.h>
int f(int a,int n)
{
	int Sn=0,k=0,i=1;
	while(i<=n){
		k+=a;
		Sn+=k;
		a*=10;
		i++;
	}
	return Sn;
}

int main()
{
	int a,n,sum;
	printf("Please input a,n:");
	scanf("%d,%d",&a,&n);
	sum=f(a,n);
	printf("a+aa+aaa+......=%d\n",sum);
	return 0;
}