#include <stdio.h>
#include <string.h>
#define N 100
void f(char str[])
{
	int i;
	for(i=strlen(str);i>0;i--){
		str[2*i]=str[i];
		str[2*i-1]=' ';
	}
	printf("The new string is:%s\n",str);
}

int main()
{
	char str[N];
	printf("Please input a integer:");
	scanf("%s",&str);
	f(str);
	return 0;
}