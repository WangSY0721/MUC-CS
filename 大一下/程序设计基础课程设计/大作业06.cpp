#include <stdio.h>
#define N 10

float credits;  //表示总积分

struct stru_goods{
 	char name[40];  //商品名称
 	float price;  //商品单价
 	int num_now=0;  //当前买数
 	int num_max=0;  //能买的最大数
};

struct stru_goods goods[N]={
 	{"李宁双肩包",8200},
 	{"新款毛巾",678},
 	{"金吉星软包抽纸",1040},
 	{"2018洗车大毛巾",1250},
 	{"小米 移动电源2",7900},
 	{"不锈钢保温杯",8690},
 	{"滋润型护肤脂",710},
 	{"真好芦荟胶",1900},
 	{"维达 手帕纸",2090},
 	{"佳洁士巨人专用",395}
};

struct stru_choice{
 	struct stru_goods goods_[N]={
  		{"李宁双肩包",8200},
  		{"新款毛巾",678},
  		{"金吉星软包抽纸",1040},
  		{"2018洗车大毛巾",1250},
  		{"小米 移动电源2",7900},
  		{"不锈钢保温杯",8690},
  		{"滋润型护肤脂",710},
  		{"真好芦荟胶",1900},
  		{"维达 手帕纸",2090},
  		{"佳洁士巨人专用",395}
 	};
 	float consum_credits=0.0;
};

struct stru_choice choices[5];

void sum_goods(){  //计算各搭配所用的积分
 	float sum_credits=0.0;
 	struct stru_goods *p;
 	p=goods;
 	struct stru_choice *tp;
 	struct stru_choice *fp;
 	struct stru_choice c[1];
 	fp=c;
 	struct stru_choice *sp;
 	int k=0;
 	while(p<goods+N){
  		sum_credits=sum_credits+p->num_now*p->price;  //累计消耗的积分
      	fp->goods_[k].num_now=p->num_now;
  		k++;
  		p++;
 	}
 	if(sum_credits<=credits){  //每次都找出最小值
  		float min = choices[0].consum_credits;
  		for(tp=choices;tp<choices+5;tp++){
     		if(tp->consum_credits<=min){
    			min=tp->consum_credits;
    			sp=tp;
   			}
  		}

  		if(sum_credits>min){
   			sp->consum_credits=sum_credits;
   			for(int k=0;k<N;k++){
    			sp->goods_[k].num_now=fp->goods_[k].num_now;  //商品购买数替换
   			}
  		}
 	}
}

void Deal_goods(int i){  //递归
 	struct stru_goods *p;
 	p=&goods[i];  //每次所指的元素不同

 	if(i<N){
  		for(p->num_now=0;p->num_now<=p->num_max;p->num_now++){
   		Deal_goods(i+1);
  		}
 	} 
	else{
		sum_goods();  //递归调用
	}
  
}

void print(){  //输出
 	struct stru_choice *tp;
 	int n=1;
 	
 	struct stru_choice s[1];
	struct stru_choice *sp;
 	sp=s;
 	for(int i=0;i<5;i++){  //冒泡排序
  		for(int j=0;j<5-i;j++){
   			for(tp=choices;tp<choices+5;tp++){
    			if(tp->consum_credits<=(tp+1)->consum_credits){
     				*sp=*tp;
     				*tp=*(tp+1);
     				*(tp+1)=*sp;
    			}
   			}
  		}
 	}
 	printf("积分损失最小的5种换购方案如下:\n\n");
 	for(tp=choices;tp<choices+5;tp++){
 		printf("———————第%d选择—————————\n以下商品消耗积分:%0.0f\n商品名称      需积分   换购数量\n————————————————————\n",n,tp->consum_credits);
  		for(int k=0;k<N;k++){
   			printf("%-15s   %-10.0f    %-2d\n",tp->goods_[k].name,tp->goods_[k].price,tp->goods_[k].num_now);
  		}
  		n++;
  		printf("========================================\n\n");
 	}
}

int main() 
{
 	int i;  //商品序号
 	printf("请输入您所有的积分:");
 	scanf("%f",&credits);
 	printf("\n===================================\n       您的总积分有:%0.0f\n===================================\n\n",credits);
 	struct stru_goods *p;
 	for(p=goods;p<goods+N;p++){
  		p->num_max=credits/p->price;  //计算可购买的最大数
 	}
 	Deal_goods(0);
 	print();  //显示前五种方案
 	return 0;
}