#include <stdio.h>
int main()
{
	int a;
	float x,y,total;
	x=2.5;
	a=7;
	y=4.7;
	total=x+a%3*(int)(x+y)%2/4.0;  //The number in your question should be 4.0?
	printf("total=%.2f\n",total);
	return 0;
}