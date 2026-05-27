#include <stdio.h>
int main()
{
	int a,n,Sn=0,k=0,i=1;
	printf("Please input a,n:");
	scanf("%d,%d",&a,&n);
	while(i<=n){
		k+=a;
		Sn+=k;
		a*=10;
		i++;
	}
	printf("a+aa+aaa+......=%d\n",Sn);
	return 0;
}