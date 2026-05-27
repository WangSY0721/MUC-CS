#include <stdio.h>
#include <math.h>

int main()
{
	int i;
	float t;
	printf("please input a integer (1-999):");
	scanf("%d",&i);
	if(i>0 && i<1000){
		t=sqrt(i);
		printf("The square root of this integer is:%.0f",t);
	}
	else{
		printf("Sorry, the number you entered does not meet the requirements, please re-enter!");
	}
	return 0;
}