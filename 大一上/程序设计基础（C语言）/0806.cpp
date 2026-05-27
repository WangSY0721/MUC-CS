#include <stdio.h>
int main()
{
	int length(char *p);
	int len;
	char str[20];
	printf("Please input a string:");
	scanf("%s",str);
	len=length(str);
	printf("The length of the string is %d.\n",len);
	return 0;
}

int length(char *p)
{
	int n=0;
	while(*p!='\0'){
		n++;
		p++;
	}
	return n;
}