#include <stdio.h>
#define N 5
struct Student{
	char number[10];
	char name[10];
	int score[3];
};

int main()
{
	struct Student stu[N];
	void print(struct Student s[]);
	for(int i=0;i<N;i++){
		printf("Please input the information of student %d:\n",i+1);
		printf("NO.");
		scanf("%s",stu[i].number);
		printf("name:");
		scanf("%s",stu[i].name);
		for(int j=0;j<3;j++){
			printf("score %d:",j+1);
			scanf("%d",&stu[i].score[j]);
		}
		printf("\n");
	}
	print(stu);
	return 0;
}

void print(struct Student s[])
{
	printf("\nNO.  name  score1  score2  score3\n");
	for(int i=0;i<N;i++){
		printf("%-5s%-6s",s[i].number,s[i].name);
		for(int j=0;j<3;j++){
			printf("%-8d",s[i].score[j]);
		}
		printf("\n");
	}
}