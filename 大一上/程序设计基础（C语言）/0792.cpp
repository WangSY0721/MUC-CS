#include <stdio.h>
int Day(int year,int month)
{
	if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12){	
		return 31;
	}
	else if (month==4 || month==6 || month==9 || month==11) {	
		return 30;
	}
	else if(month==2){	
		if((year%4==0) && (year%100!=0) || (year%400==0)){	
			return 29;
		}
		else{	
			return 28;
		}
	}
	else{
		return 0;
	}
}

int main()
{	int year, month, day;

	printf("Which year,month?");
	scanf("%d %d", &year, &month);
	while ((month > 12) || (month < 1))
	{	
		printf ("error");
		scanf("%d %d", &year, &month);
	}
	day=Day(year,month);
	printf("There are %d days in the month.",day);
	return 0 ;
}