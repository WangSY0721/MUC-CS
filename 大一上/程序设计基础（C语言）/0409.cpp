#include <stdio.h>
int main()
{
	int number,digits,bits,ten,hundred,thousand,tenthousand;
	printf("Please input a integer(0-99999):");
	scanf("%d",&number);
	while(number>99999||number<0){
		printf("\nthe input is incorrect,please try again");
		scanf("%d",&number);
	}
	if(number>9999){
		digits=5;
	}
	else if(number>999){
		digits=4;
	}
	else if(number>99){
		digits=3;
	}
	else if(number>9){
		digits=2;
	}
	else{
		digits=1;
	}
	printf("The digit is %d.\n",digits);
	tenthousand=number/10000;
	thousand=(number-10000*tenthousand)/1000;
	hundred=(number-10000*tenthousand-1000*thousand)/100;
	bits=number%10;
	ten=(number%100-bits)/10;
	printf("The numbers for each are:%d,%d,%d,%d,%d\n",tenthousand,thousand,hundred,ten,bits);
	switch(digits){
		case 5:printf("The number in reverse order is:%d%d%d%d%d",bits,ten,hundred,thousand,tenthousand);break;
		case 4:printf("The number in reverse order is:%d%d%d%d",bits,ten,hundred,thousand);break;
		case 3:printf("The number in reverse order is:%d%d%d",bits,ten,hundred);break;
		case 2:printf("The number in reverse order is:%d%d",bits,ten);break;
		case 1:printf("The number in reverse order is:%d",bits);break;
	}
	return 0;
}