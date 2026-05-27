#include <stdio.h>
#define N 10
int main()
{
	float a[N],sum,aver;
	printf("please input %d numbers:\n",N);
	for(int i=0;i<N;i++){
		scanf("%f",&a[i]);
	}
	for(int i=0;i<N;i++){
		sum+=a[i];
	}
	aver=sum/N;
	printf("The average is %f\n",aver);
	int maxi,mini;
	float max=a[0],min=a[0];
	for(int i=0;i<N;i++){
		if(a[i]>=max){
			maxi=i;
			max=a[i];
		}
	}
	printf("The maximum is %f,the subscript is %d\n",max,maxi);
	for(int i=0;i<N;i++){
		if(a[i]<=min){
			mini=i;
			min=a[i];
		}
	}
	printf("The minimum is %f,the subscript is %d\n",min,mini);
	return 0;
}