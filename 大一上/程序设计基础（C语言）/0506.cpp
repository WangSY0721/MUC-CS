#include <stdio.h>
int main()
{
	double s=0,k=1;
	for(int n=1;n<=20;n++){
		k*=n;
		s+=k;
	}
	printf("1!+2!+3!+4!......+20!=%f\n",s);
	return 0;
}