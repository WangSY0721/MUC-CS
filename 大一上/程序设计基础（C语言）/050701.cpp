#include <stdio.h>
int main()
{
	int a=100,b=50,c=10;
	float k,s1=0,s2=0,s3=0,sum;
	for(k=1;k<=a;k++){
		s1+=k;
	}
	for(k=1;k<=b;k++){
		s2+=k*k;
	}
	for(k=1;k<=c;k++){
		s3+=1/k;
	}
	sum=s1+s2+s3;
	printf("sum=%.3f\n",sum);
	return 0;
}