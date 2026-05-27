#include <stdio.h>
#define N 10
int main()
{
	float a[N+1],number,end;
	int temp1,temp2;
	printf("please input %d numbers:\n",N);
	for(int i=0;i<N;i++){
		scanf("%3f",&a[i]);
	}
	printf("Please input the insert data:");
	scanf("%f",&number);
	end=a[N-1];
	if(number>end){
		a[N]=number;
	}
	else{
		for(int i=0;i<N;i++){
			if(a[i]>number){
				temp1=a[i];
				a[i]=number;
				for(int j=i+1;j<N+1;j++){
					temp2=a[j];
					a[j]=temp1;
					temp1=temp2;
				}
				break;
			}
		}
	}
	printf("The new array:\n");
	for(int i=0;i<N+1;i++){
		printf("%.3f  ",a[i]);
	}
	printf("\n");
	return 0;
}