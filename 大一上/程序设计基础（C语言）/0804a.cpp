#include <stdio.h>
void move(int array[],int n,int m)
{
	int *p,end;
	end=*(array+n-1);
	for(p=array+n-1;p>array;p--){
		*p=*(p-1);
	}
	*array=end;
	m--;
	if(m>0){
		move(array,n,m);
	}
}

int main()
{
	int number[100],n,m,i;
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
		printf("%d ",number[i]);
	}
	printf("\n");
	return 0;
}