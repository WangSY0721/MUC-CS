#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_SIZE 1000
#define MAX_WORD 100

int freq[26];  //存储字母数量的数组
int numInts;  //统计整数的个数

int CountWords(char* str){
    int cnt=0;
    int len=strlen(str);
    for(int i=0;i<len;i++){
        if(i==0||isspace(str[i-1])){  //判断空格
            //isspace()函数用于判断是否为空白字符
			while(i<len&&isalnum(str[i])){  //向后扫描直到空格或标点符号
                //isalnum()函数判断一个字符是否是字母或数字
				i++;
            }
            cnt++;
        }
    }
    return cnt;
}

void FindLongestWord(char* str,char* LongestWord){
    int maxLen=0;
    int len=strlen(str);
    char word[MAX_WORD]="";
    int idx=0;
    for(int i=0;i<len;i++){
        if(isalnum(str[i])){  //如果当前字符是字母或数字，加入
            word[idx++]=tolower(str[i]);  //转换成小写字母
        } 
		else{  //如果当前字符是空格或标点符号，结束
            if(idx>maxLen){
                maxLen=idx;
                strcpy(LongestWord,word);
            }
            idx=0;  //重置当前单词
            memset(word,0,sizeof(word));  //清空当前单词的缓存
        }
    }
    if(idx>maxLen){
        maxLen=idx;
        strcpy(LongestWord,word);
    }
}

void CountInts(char* str,int ints[]){
    int len=strlen(str);
    char numStr[MAX_WORD]="";
    int idx=0;
    for(int i=0;i<len;i++){
        if(isdigit(str[i])){  //如果当前字符是数字，加入
            numStr[idx++]=str[i];
        } 
		else{  //如果当前字符不是数字，结束
            if(idx>0){
                numInts++;
                ints[numInts-1]=atoi(numStr);  //将当前整数字符串转换为整数并存储
            }
            idx=0;  //重置当前整数
            memset(numStr,0,sizeof(numStr));  //清空当前整数的缓存
            //memset(s,c,n);将s所指向的前n字节的内存单元用c替换
        }
    }
    if(idx>0){  //处理最后一个整数
        numInts++;
        ints[numInts-1]=atoi(numStr);
    }
}

int main() 
{
    FILE* fp=fopen("1.txt","r");
    if(fp==NULL){
        printf("无法打开输入文件！");
    }
    
    char text[MAX_SIZE]="";
    char line[MAX_SIZE];
    while(fgets(line,MAX_SIZE,fp)!=NULL){  //逐行读取文本
        strcat(text,line);  //将每行文本连接成完整的文本
    }
    fclose(fp);
    
    int NumWords=CountWords(text);
    printf("共有%d个单词在文件中\n",NumWords);
    
    char LongestWord[MAX_WORD]="";
    FindLongestWord(text,LongestWord);
    printf("最长的单词的长度为%d\n这个单词是：%s\n\n",(int)strlen(LongestWord),LongestWord);
    
    int len=strlen(text);
    for(int i=0;i<len;i++){
        if(isalpha(text[i])){ // 如果当前字符是字母，则统计数量
            freq[tolower(text[i])-'a']++;
        }
    }
    printf("字母的数量统计：\n\n");
	int amount1=0;
    for(int i=0;i<26;i++){
        printf("%c： %-5d",'a'+i,freq[i]);
        amount1+=1;
        if(amount1==7){
        	printf("\n");
        	amount1=0;
		}
    }
    printf("\n\n");
    
    int ints[MAX_SIZE];
    CountInts(text,ints);
    printf("文件中的整数出现%d次：\n",numInts);
    int amount2=0;
    for(int i=0;i<numInts;i++){
        printf("%d ",ints[i]);
        amount2+=1;
        if(amount2==5){
        	printf("\n");
        	amount2=0;
		}
    }
    printf("\n");
    
    return 0;
}