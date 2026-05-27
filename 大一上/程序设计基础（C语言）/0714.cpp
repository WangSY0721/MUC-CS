#include <stdio.h>
#define N 10
#define M 5
float score[N][M];
void student_score()
{
	int i,j;
	for(i=0;i<N;i++){
		printf("Please input the score of student %2d:\n",i+1);
		for(j=0;j<M;j++){
			scanf("%f",&score[i][j]);
		}
		printf("\n");
	}
}

void student_aver()
{
	int i,j;
	float s;
	for(i=0;i<N;i++){
		s=0;
		for(j=0;j<M;j++){
			s+=score[i][j];
		}
		printf("The %d student average grade is:%f\n",i+1,s/M);
	}
}

void course_aver()
{
	int i,j;
	float s;
	for(j=0;j<M;j++){
		s=0;
		for(i=0;i<N;i++){
			s+=score[i][j];
		}
		printf("The %d course average grade is:%f\n",j+1,s/N);
	}
}

void highest()
{
	int i,j,i1,j1;
	float high=score[0][0];
	for(i=0;i<N;i++){
		for(j=0;j<M;j++){
			if(score[i][j]>high){
				high=score[i][j];
				i1=i+1;
				j1=j+1;
			}
		}
	}
	printf("Highest:%7.2f   NO. %2d   course:%2d\n",high,i1,j1);
}

int main()
{
	student_score();
	student_aver();
	printf("\n");
	course_aver();
	printf("\n");
	highest();
	return 0;
}