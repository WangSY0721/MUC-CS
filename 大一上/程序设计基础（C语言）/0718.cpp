#include <stdio.h>
int main()
{
	int leap(int year);
	int sum_day(int month,int year);
	int judge(int month ,int day); 
	int year,month,day,days;
	printf("please input date(year month day):");
	scanf("%d %d %d",&year,&month,&day);
	if(judge(month,day)){
		days=judge(month,day);
			if(leap(year)&&month>=3){
			days+=1;
		}
	}
	else{
		printf("Error!\nPlease input a new date(year month day):");
		scanf("%d %d %d",&year,&month,&day);
	}
	printf("This is the %dth day in this year.\n",days);
  	return 0;
}

int judge(int month ,int day){
	int sum_day(int month,int year);
	int days;
	if((month<1||month>12)||(day<1)||(month==1||month==3||month==5||month==7||month==8||month==10||month==12)&&(day>31)||(month==4||month==6||month==9||month==11)&&(day>30)){
		return 0;
	}
	else{
		days=sum_day(month,day);
		return days;
	}
}

int sum_day(int month,int day)
{
	int day_tab[13]={0,31,28,31,30,31,30,31,31,30,31,30,31};
	int i;
	for(i=0;i<month;i++){
		day+=day_tab[i];
		}
	return day;
}

int leap (int year){
	int leap;
	if(year%4!=0)  
		leap=0;
	else if (year%100!=0)  
		leap=1;
	else if(year%400!=0)   
		leap=0;
	else
		leap=1;
	//leap=year%4==0&&year%100!=0||year%400==0;
	return(leap);
}