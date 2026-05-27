#include <stdio.h>
#include <string.h>
#define N 100
char str[N];
void f(char *p)
{
	int i;
	for(i=strlen(p);i>0;i--){
		*(p+2*i)=*(p+i);
		*(p+2*i-1)=' ';
	}
	printf("The new string is:%s\n",p);
}

int main()
{
	char *p;
	p=str;
	printf("Please input a integer:");
	scanf("%s",&str);
	f(p);
	return 0;
}