#include <stdio.h>
#define N 100
int main()
{
	char s1[N],s2[N];
	int i=0,j=0;
	printf("Please input string1:");
	scanf("%s",s1);
	printf("Please input string2:");
	scanf("%s",s2);
	while(s1[i]!='\0'){
		i++;
	}
	while(s2[j]!='\0'){
		s1[i++]=s2[j++];
	}
	s1[i]='\0';
	printf("The new string is:%s\n",s1);
	return 0;
}