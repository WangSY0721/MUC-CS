#include <stdio.h>
#include <string.h>
#define N 100
int main()
{
	char s1[N],s2[N];
	int i;
	printf("Please input s1:");
	scanf("%s",s1);
	printf("please input s2:");
	scanf("%s",s2);
	for(i=0;i<=strlen(s2);i++){
		s1[i]=s2[i];
	}
	s1[i]='\0';
	printf("The new string is:%s\n",s1);
	return 0;
}