#include <stdio.h>
int main()
{
	int i,j,m,n;
	printf("please input an n:");
	scanf("%d",&n);
	while(n%2==0){
		printf("please add another one.\n");
		scanf("%d",&n);	
	}

	for(i=1;i<=(n-1)/2+1;i++){
		for(m=1;m<=(n-1)/2+1-i;m++){
			printf ("%c",' ');
		}
		for(j=1;j<=2*i-1;j++){
			printf ("%c",'*');
		}
		printf("\n");
	}
	for(i=1;i<=(n-1)/2;i++){
		for(m=1;m<=i;m++){
			printf ("%c",' ');
		}
		for(j=1;j<=n-2*i;j++){
			printf ("%c",'*');
		}
		printf("\n");
	}
	return 0;
}