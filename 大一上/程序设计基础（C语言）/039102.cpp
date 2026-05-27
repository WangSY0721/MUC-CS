#include <stdio.h>
int main()
{
	int a,b;
	float x,y,total;
	a=2;
	b=3;
	x=3.5;
	y=2.5;
	total=(float)(a+b)/2+(int)x%(int)y;
	printf("total=%.1f\n",total);
	return 0;
}