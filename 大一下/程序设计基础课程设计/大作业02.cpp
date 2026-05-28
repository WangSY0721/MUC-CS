#include <stdio.h>
#include <stdlib.h>
#include <time.h>
void Average(int a[],int n)  //求出所有高于平均数的数据
{
	int sum=0,i;
	float avg;
	for(i=0;i<n;i++){
		sum+=a[i];
	}
	avg=sum*1.0/n;
	//printf("%d个数的平均数为：%f\n",n,avg);
	
	printf("高于该组数据平均数的数据有:");
	for(i=0;i<n;i++){
		if(a[i]>avg){
			printf("%d ",a[i]);
		}
	}
	printf("\n");
}

void Swap(int *x,int *y)  //交换两数大小
{
	int temp;
	temp=*x;
	*x=*y;
	*y=temp;
}

void MaxMin(int a[],int n)  
{
	int i,temp;
	int max,maxi=0;
	max=a[0];
	for(i=1;i<n;i++){  //求出n个数的最大数的下标
		if(a[i]>max){
			max=a[i];
			maxi=i;
		}
	}
	
	int min,mini=0;
	min=a[0];
	for(i=1;i<n;i++){  //求出n个数的最小数的下标
		if(a[i]<min){
			min=a[i];
			mini=i;
		}
	}
	
	Swap(&a[maxi],&a[mini]);  //交换最大数和最小数的位置
	printf("交换该组数据中最大和最小数据的位置后该组数据变成：");
	for(i=0;i<n;i++){
		printf("%d ",a[i]);
	}
	printf("\n");
}

void Invertedsequence(int a[],int n)  //对这组数据进行逆置
{
	int i;
	printf("将该数组逆置后为：");
	for(i=n-1;i>=0;i--){
		printf("%d ",a[i]);
	}
	printf("\n");
}

void Bubble(int a[],int n)  //起泡排序对这组数据进行排序（递增）并显示
{
	int i,j,temp;
	for(j=0;j<n-1;j++){
		for(i=0;i<n-1-j;i++){
			if(a[i]>=a[i+1]){
				temp=a[i];
				a[i]=a[i+1];
				a[i+1]=temp;
			}
		}
	}
	
	printf("将该组数据递增排序后为：");
	for(i=0;i<n;i++){
		printf("%d ",a[i]);
	}
	printf("\n\n");
}

void Sequence(int a[],int n,int num)  //对n个数的进行顺序查找
{
	int i,x,flag=1,t=0;
	printf("将该组数据进行顺序查找：\n");
	printf("比较的数据有：");
	for(i=0;i<n;i++){
		if(num!=a[i]){
			printf("%d ",a[i]);
			t++;
		}
		if(num==a[i]){
			printf("%d ",a[i]);
			flag=0;
			x=i;
			t++;
			break;
		}
	}
	printf("\n");
	if(flag==0){
		printf("比较的次数为：%d次\n",t);
		printf("该数的下标为：%d\n",x+1);
		printf("        结果：该数组中有%d\n",num);
	}
	else{
		printf("\n该组数据中没有%d！",num);
	}
	printf("\n\n");
}

void Binary(int a[],int n,int num)  //对n个数的进行二分查找
{
	int i,x,t=0,flag=1;
	int min=0,max=n-1,avg;
	printf("将该数组进行二分查找：\n");
	printf("比较的数据有：");
	while(min<=max){
		avg=(min+max)/2;
		if(a[avg]==num){
			printf("%d ",a[avg]);
			flag=0;
			x=avg;
			t++;
			break;
		}
		else if(a[avg]<num){
			printf("%d ",a[avg]);
			min=avg+1;
			t++;
		}
		else{
			printf("%d ",a[avg]);
			max=avg-1;
			t++;
		}
	}
	printf("\n");
	if(flag==0){
		printf("比较的次数为：%d次\n",t);
		printf("该数的下标为：%d\n",x+1);
		printf("        结果：该数组中有%d\n",num);
	}
	else{
		printf("\n该组数据中没有%d！",num);
	}
	printf("\n");
}

int main()
{
	int a[40],b[40],c[40],n,i,num;
	int maxi,mini;
	printf("请输入要处理元素的个数：");
	scanf("%d",&n);
	srand((unsigned)time(NULL));
	printf("给出的数据分别是：");
	for(i=0;i<n;i++){
		a[i]=rand()%100;
		printf("%d ",a[i]);
	}
	printf("\n");
	
	for(i=0;i<n;i++){
		b[i]=a[i];
	}
	for(i=0;i<n;i++){
		c[i]=a[i];
	}
	
	Average(a,n);
	
	MaxMin(a,n);
	
	Invertedsequence(b,n);
	
	Bubble(b,n);
	
	printf("请输入一个需要查找的数:");
	scanf("%d",&num);
	Sequence(c,n,num);
	
	Binary(b,n,num);
	
	return 0;
}