#include <stdio.h>
int main()
{
	int hcf(int,int);
	int lcd(int,int,int);
	int u,v,HCF,LCD;
	printf("Please input two integers:");
	scanf("%d,%d",&u,&v);
	HCF=hcf(u,v);
	printf("HCF=%d\n",HCF);
	LCD=lcd(u,v,HCF);
	printf("LCD=%d\n",LCD);
	return 0;
}

int hcf(int u,int v)
{
	int m,n;
	if(v>u){
		m=u;
		u=v;
		v=m;
	}
	while(u%v!=0){
		n=u%v;
		u=v;
		v=n;
	}
	return(v);
}

int lcd(int u,int v,int HCF)
{
	return(u*v/HCF);
}