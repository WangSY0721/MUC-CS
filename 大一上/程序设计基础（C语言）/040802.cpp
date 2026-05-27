#include <stdio.h>
int main ()
{
	int score;
	char grade;
	printf("please input the score of the student:");
	scanf("%d",&score);
	while(score>100||score<0){
		printf("\nthe input is incorrect,please try again");
		scanf("%d",&score);
	}
	switch(score/10){
		case 10:
		case 9:grade='A';break;
		case 8:grade='B';break;
		case 7:grade='C';break;
		case 6:grade='D';break;
		default:grade='E';break;
	}
	printf("The corresponding grade is %c\n",grade);
	return 0;
}