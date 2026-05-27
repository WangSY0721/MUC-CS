#include <stdio.h>
int main ()
{
	int i,j,capitalletters=0,lowercaseletters=0,digital=0,blankspace=0,other=0;
	char str[10];
	gets(str);
	for(i=0;i<10&&str[i]!='\0';i++){
		if (str[i]>='A'&&str[i]<='Z'){
			capitalletters++;
		}
		else if (str[i]>='a'&&str[i]<='z'){
			lowercaseletters++;
		}
		else if (str[i]>='0'&&str[i]<='9'){
			digital++;
		}
		else if (str[i]==' '){
			blankspace++;
		}
		else{
			other++;
		}
	}
	printf("\ncapital letters  :%d\n",capitalletters);
	printf("lowercase letters:%d\n",lowercaseletters);
	printf("digital          :%d\n",digital);
	printf("blank space      :%d\n",blankspace);
	printf("other            :%d\n",other);
	return 0;
}