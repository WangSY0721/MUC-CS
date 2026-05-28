#include <stdio.h>
#include <string.h>
#define N 100
void Extract(char *expression,int &n,int *num){  //提取数字
	int i=0,j=0,temp=0;
	int flag=0;
	while(i<strlen(expression)){
		while(expression[i]==' '){
			i++;
		}
		while(i<strlen(expression) && expression[i]>='0' && expression[i]<='9'){
			temp=temp*10+expression[i]-'0';
			flag=1;
			i++;
		}
		if(flag==1){
			*num=temp;
			num++;
			j++;
			flag=0;
		}
		i++;
		temp=0;
	}
	n=j;
}

void Getoperator(char *expression,char *opera){  //获取运算符
	int i,j=0;
	for(i=0;i<strlen(expression);i++){
		while(expression[i]==' '){
			i++;
		}
		if(expression[i]=='+'||expression[i]=='-'||expression[i]=='*'||expression[i]=='/'){
			opera[j]=expression[i];
			j++;
		}
	}
}

float Calculate(char *opera,int *num,int n){  //计算结果
	int i=0,j;
	float calume[n];
	for(j=0;j<n;j++){
		calume[j]=num[j];
	}
	while(i<n){
		if(opera[i]=='+'){  //加法
			i++;
		}
		else if(opera[i]=='-'){  //减法
			calume[i+1]=-calume[i+1];
			opera[i]='+';
			i++;
		}
		else if(opera[i]=='*'){
			calume[i+1]=calume[i]*calume[i+1];
			opera[i]='+';
			calume[i]=0;
			i++;
		}
		else if(opera[i]=='/'){
			calume[i+1]=calume[i]/calume[i+1];
			opera[i]='+';
			calume[i]=0;
			i++;
		}
		else{
			i++;
		}
	}
	float result=0.0;
	for(j=0;j<n;j++){
		result+=calume[j];
	}
	return result;
}

int main()
{
	printf("请输入你想计算的式子(用等号结尾):\n");
	printf("例1:\n1 + 20 * 3 / 8 - 5 + 16 / 2 / 1 * 5 =\n\n\n");
	printf("例2:\n1+20*3/8-5+16/2/1*5=\n");
	printf("====================================\n\n");
	char expression[N];  //表达式
	char opera[N];  //运算符
	int num[N];
	int n=0;
	gets(expression);  //获取表达式
	Getoperator(expression,opera);  //获取运算符
	Extract(expression,n,num);
	float result;
	result=Calculate(opera,num,n);
	printf("结果=%.2f\n",result);
	return 0;
}