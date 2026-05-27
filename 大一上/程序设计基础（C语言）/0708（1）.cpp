#include <stdio.h>
int main()
{
	void f(int a);
	int a;
	printf("Please input a four digit number:");
	scanf("%d",&a);
	f(a);
	return 0;
}

void f(int a)
{
	int b,c,d,e;
	b=a/1000;
	c=a/100%10;
	d=a/10%10;
	e=a%10;
	printf("%c %c %c %c\n",b+'0',c+'0',d+'0',e+'0');
	printf("%d %d %d %d\n",b,c,d,e);
}