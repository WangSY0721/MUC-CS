#include <stdio.h>
int main()
{
	float a=2,b=1,t;
	double s=0;
	for(int i=1;i<=20;i++){
		s+=a/b;
		t=a;
		a=a+b;
		b=t;
	}
	printf("sum=%f\n",s);
	return 0;
}