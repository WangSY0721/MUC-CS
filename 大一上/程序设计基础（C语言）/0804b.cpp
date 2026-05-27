#include <stdio.h>
#define N 100
void move(int a[],int n,int m)
{
	int *p,end;
	end=*(a+n-1);
	for(p=a+n-1;p>a;p--){
		*p=*(p-1);
	}
	*a=end;
	m--;
	if(m>0){
		move(a,n,m);
	}
}

int main()
{
	int number[N],n,m,i;
	int *p=number;
	printf("PLease input the number:");
	scanf("%d",&n);
	printf("Please input %d integers:\n",n);
	for(i=0;i<n;i++){
		scanf("%d",&number[i]);
	}
	printf("Please input how much place you want to move:");
	scanf("%d",&m);
	move(number,n,m);
	printf("The new sequence is:\n");
	for(i=0;i<n;i++){
		printf("%d ",*(p+i));
	}
	printf("\n");
	return 0;
}