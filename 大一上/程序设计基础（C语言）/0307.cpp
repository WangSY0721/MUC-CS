#include <stdio.h>
#define PI 3.14
int main()
{
	float r,h;
	float C,S,Sq,Vq,V;
	printf("please input the radius:");
	scanf("%f",&r);
	printf("please input the height:");
	scanf("%f",&h);
	C=2*PI*r;
	S=PI*r*r;
	Sq=4*PI*r*r;
	Vq=(4*PI*r*r*r)/3;
	V=S*h;
	printf("Circumference is:%.2f\n",C);
	printf("Circular area is:%.2f\n",S);
	printf("Sphere surface area is:%.2f\n",Sq);
	printf("Sphere volume is:%.2f\n",Vq);
	printf("Cylindrical volume is:%.2f\n",V);
	return 0;
}