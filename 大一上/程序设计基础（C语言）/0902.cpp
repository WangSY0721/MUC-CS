#include <stdio.h>
struct Date{
	int year;
	int month;
	int day;
}date;

int main()
{
	int days(int year,int month,int day);
	int Days;
	printf("Please input year,month,day:");
	scanf("%d,%d,%d",&date.year,&date.month,&date.day);
	Days=days(date.year,date.month,date.day);
	printf("It is the %d day of the year.\n",Days);
	return 0;
}

int days(int year,int month,int day)
{
	int sum=day;
	int day_tab[13]={0,31,28,31,30,31,30,31,31,30,31,30,31};
	for(int i=1;i<month;i++){
		sum+=day_tab[i];
	}
	if(((year%4==0&&year%100!=0)||year%400==0)&&month>=3){
		sum+=1;
	}
	return sum;
}