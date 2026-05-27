#include <stdio.h>
#define N 100
int main()
{
	int str[N];
	int *p=str;
	int n,i,k,m;
	printf("Please input the nunber of the people:");
	scanf("%d",&n);
	for(i=0;i<n;i++){
		*(p+i)=i+1;
	}
	i=0;k=0;m=0;
	while(m<n-1){
		if(*(p+i)!=0){
			k++;
		}
		if(k==3){
			*(p+i)=0;
			k=0;
			m++;
		}
		i++;
		if(i==n){
			i=0;
		}
	}
	while(*p==0){
		p++;
	}
	printf("The number left is:%d",*p);
	return 0;
}