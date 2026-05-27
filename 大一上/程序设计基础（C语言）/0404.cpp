#include <stdio.h>

int main()
{
	int a,b,c,t,max;
	printf("Please input three integers a,b,c:");
	scanf("%d,%d,%d",&a,&b,&c);
	t=(a>b)?a:b;
	max=(t>max)?t:max;
	printf("The largest of the three integers is:%d",max);
	return 0;
}