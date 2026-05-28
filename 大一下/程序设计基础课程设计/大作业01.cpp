#include <stdio.h>
#include <math.h>
void Judge7(int m,int n){  //（1）求出m和n两个数之间所有“明7暗7”数
	int i,j,k;
	printf("\n明7暗7：");
	for(i=m;i<=n;i++){
		k=i;
		if(i%7==0){
			printf("%d ",i);
		}
		else{
			for(j=0;k!=0;j++){
				if(k%10==7){
					printf("%d ",i);
					break;
				}
				k/=10;
			}	
		}
	}
	printf("\n\n");
}

void Factorial(int p){  //（2）分别求出m! 和 n!
	long double product=1.0;
	for(int i=1;i<=p;i++){
		product*=i;
	}
	printf("%.6Lf\n",product);
}

void GcdLcm(int m,int n)  //（3）求m和n的最大公约数和最小公倍数
{
	int p,i;
	p=n*m;
	while(m!=0){
		i=n%m;
		n=m;
		m=i;
	}
	printf("输入的这两个数的最大公约数为:%d\n",n);
	printf("输入的这两个数的最小公倍数为:%d\n\n",p/n);
}

void RevertedNumber(int m,int n)  //（4）求出m和n两个数之间的所有回文数
{	
	int t,j;
	printf("输入的两个数之间的回文数有：");
	for(int i=m;i<=n;i++){
		j=0;
		t=i;
		while(t!=0){       
        	j=j*10+t%10;        
        	t/=10;    
    	}    
    	if(j==i){
    		printf("%d ",i);
		}  
	}
	printf("\n\n");
}

void Prime(int m,int n)  //（5）求出m和n两个数之间的所有素数
{
	int x,i,isPrime;
	double k;
	printf("输入的两个数之间的素数有：");
	for(x=m;x<=n;x++){
		k=sqrt(x);
		isPrime=1;
		if(x==1){
			isPrime=0;
		}
		for(i=2;i<=k;i++){
			if(x%i==0){
				isPrime=0;
				break;
			}
		}
		if(isPrime==1){
			printf("%d ",x);
		}
	}
	printf("\n\n");
}

void Perfectnumber(int m,int n)  //（6）求出m和n两个数之间的所有完数
{
	int k,i,sum;
	printf("输入的两个数之间的完数有：");
	for(k=m;k<=n;k++){
		sum=0;
		for(i=1;i<k;i++){
			if(k%i==0){
				sum+=i;
			}
		}
		if(sum==k){
			printf("%d ",k);
		}	
	}
	printf("\n\n");
}

int main()
{
	int m,n,temp;
	printf("输入两个正整数(按回车键结束):\n");
	printf("请输入第一个数：");
	scanf("%d",&m);
	printf("请输入第二个数：");
	scanf("%d",&n);
	
	if(m>n){
		temp=m;m=n;n=temp;
	}  //交换
	
	Judge7(m,n);
	
	printf("第一个输入的数阶乘为：");
	Factorial(m);
	printf("第二个输入的数阶乘为：");
	Factorial(n);
	printf("\n");
	
	GcdLcm(m,n);
	
	RevertedNumber(m,n);
	
	Prime(m,n);
	
	Perfectnumber(m,n);
	return 0; 
}