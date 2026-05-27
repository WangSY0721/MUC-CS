#include <stdio.h>
int main()
{
	int leap(int year),sum_day(int month,int year);
	int year,month,day,days;
	printf("please input date(year,month,day):");
	scanf("%d,%d,%d",&year,&month,&day);
	days=sum_day(month,day);
	if(leap(year)&&month>=3){
		days+=1;
	}
	printf("This is the %dth day in this year.\n",days);
  	return 0;
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

int sum_day(int month,int day)
{
	int day_tab[13]={0,31,28,31,30,31,30,31,31,30,31,30,31};
	int i;
	for(i=0;i<month;i++){
		day+=day_tab[i];
		}
	return day;
}