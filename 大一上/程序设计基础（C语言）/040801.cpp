#include <stdio.h>
int main ()
{
	int score,s;
	char grade;
	printf("please input the score of the student:");
	scanf("%d",&score);
	while(score>100||score<0){
		printf("\nthe input is incorrect,please try again");
		scanf("%d",&score);
	}
	s=score/10;
	if(s==10||s==9){
		printf("The corresponding grade is A.\n");
	}
	else if(s==8){
		printf("The corresponding grade is B.\n");
	}
	else if(s==7){
		printf("The corresponding grade is C.\n");
	}
	else if(s==6){
		printf("The corresponding grade is D.\n");
	}
	else{
		printf("The corresponding grade is E.\n");
	}
	return 0;
}