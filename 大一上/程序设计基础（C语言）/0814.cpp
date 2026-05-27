#include <stdio.h>
int main()
{
	void sort(char *p,int m);
	int n;
	printf("Please input the number you want to sort:");
	scanf("%d",&n);
	char number[n];
	printf("Please input %d number:",n);
	for(int i=0;i<n;i++){
		scanf("%d",&number[i]);
	}
	char *p=number;
	sort(p,n);
	printf("The new sequence is:");
	for(int i=0;i<n;i++){
		printf("%d ",number[i]);
	}
	printf("\n");
	return 0;
}

void sort(char *p,int n)
{
	char temp,*p1,*p2;
	for(int i=0;i<n/2;i++){
		p1=p+i;
		p2=p+(n-1-i);
		temp=*p1;
		*p1=*p2;
		*p2=temp;
	}
}