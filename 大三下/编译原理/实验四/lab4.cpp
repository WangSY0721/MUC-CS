#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

char *cp;            /*指向给定的要分析
的表达式语言 */
int i = 1;           //从第一步开始执行

struct sta_stack
{   int stas[50];
    int top1;

};          //状态栈的数据结构
sta_stack stack1;    //定义一个状态栈
struct str_stack
{   string strs[50];
    int top2;
};          //符号栈的数据结构
str_stack stack2;    //定义一个符号栈


/*终结符用相应的整数代替*/
string symbol1[6] =
{"#", "ID", "+", "*", "(", ")"};

/*非终结符也用相应的整数代替*/
string symbol2[4] =
{"S", "E", "T", "F"};

/* Yy_action表 */
int Yya000[] = {2, 4, 2, 1, 1};

int Yya001[] = {4, 5, -6, 3, -6, 2, -6, 0, -6};

int Yya003[] = {2, 0, 0, 2, 7};

int Yya004[] = {4, 5, -2, 2, -2, 0, -2, 3, 8};

int Yya005[] = {4, 5, -4, 3, -4, 2, -4, 0, -4};

int Yya006[] = {2, 5, 9, 2, 7};

int Yya009[] = {4, 5, -5, 3, -5, 2, -5, 0, -5};

int Yya010[] = {4, 5, -1, 2, -1, 0, -1, 3, 8};

int Yya011[] = {4, 5, -3, 3, -3, 2, -3, 0, -3};

int *Yy_action[] =
{   Yya000, Yya001, Yya000, Yya003, Yya004, Yya005,
    Yya006, Yya000, Yya000, Yya009, Yya010, Yya011
};

/*Yy_goto表*/
int Yyg000[] = {3, 3, 5, 2, 4, 1, 3};

int Yyg002[] = {3, 3, 5, 2, 4, 1, 6};

int Yyg007[] = {2, 3, 5, 2, 10};

int Yyg008[] = {1, 3, 11};

int *Yy_goto[] =
{   Yyg000, NULL, Yyg002, NULL, NULL, NULL,
    NULL, Yyg007, Yyg008, NULL, NULL, NULL
};

/* 为了进行归约，使用一个Yy_lhs[]数组，其值为代表
产生式左部符号的整数，数组的下标为产生式号  */
int Yy_lhs[7] = {0, 1, 1, 2, 2, 3, 3};

/*Yy_reduce[]数组元素的值为产生式右部符号的个数，
以产生式号为数组的下标索引 */
int Yy_reduce[7] = {1, 3, 1, 3, 1, 3, 1};

/*根据以上数组结构，构造函数Yy_next()，其功能是在给
定状态和输入符号下，求出应采取的动作或转向的下一状态。*/
int Yy_next(int **table, int cur_state, int symbol)
{   int *p = table[cur_state];
    int i;
    if (p)
       for (i = (int) * p++; i-- > 0; p += 2)
          if (symbol == p[0])
             return (p[1]);
    return 8000;                             /*出错指示*/
}

/*将相应的状态和符号进行压栈*/
void push(int sta, string str)
{   stack1.top1++;
    stack1.stas[stack1.top1] = sta;
    stack2.top2++;
    stack2.strs[stack2.top2] = str;
}

/* 从输入流读下一单词到  sym*/
string advance()
{   string sym;
    if (*cp == 'I' && *(cp + 1) == 'D')
    {  sym = "ID";
       /*cp=cp+2;*/
    }
    else
    {  sym = *cp;
       /*cp=cp+1;*/
    }
    return sym;
}

/*进行归约动作*/
int act(int YN)
{   int tYN = -YN;
    return Yy_lhs[tYN];
}

/*弹栈*/
void pop(int n)
{   stack1.top1 -= n;
    stack2.top2 -= n;
}


void output()   //输出状态栈、符号栈以及未分析输入串
{   int sumstrlen = 0, i6;
    int stasum = 0, i7;
    cout << setw(3) << setiosflags(ios::right) << i << "     ";
    for (int i2 = 0; i2 <= stack1.top1; i2++)
    {  cout <</*setw(8)<<setiosflags(ios::left)<<*/stack1.stas[i2];
       if (stack1.stas[i2] == 10 || stack1.stas[i2] == 11)
          i7 = 2;
       else
          i7 = 1;
       stasum = stasum + i7;
    }
    cout << setw(12 - stasum) << setiosflags(ios::left) << " ";
    for (int i3 = 0; i3 <= stack2.top2; i3++)
    {  cout << stack2.strs[i3];
       if (stack2.strs[i3] == "ID")
          i6 = 2;
       else
          i6 = 1;
       sumstrlen = sumstrlen + i6;
    }
    cout << setw(12 - sumstrlen) << setiosflags(ios::left) << " ";
//cout<<"    ";
    cout << setw(8) << setiosflags(ios::right) << cp << "    ";
}

int main()
{   stack1.top1 = stack2.top2 = -1;
    char as[50];
    cp = as;
    int YN = 0;
    cout << "请输入要分析的语句：";
    cin >> as;
    cout << "               " << "对输入串" << as << "的分析过程如下" << endl;
    cout << "步骤    " << "状态栈      ";
    cout << "符号栈      " << "输入串      ";
    cout << "ACTION    " << "GOTO" << endl;
    push(0, "#");
    output();
    string sym;
    while (1)
    {  sym = advance();
       int i1 = 0;
       while (sym != symbol1[i1])
          i1++;
       YN = Yy_next(Yy_action, YN, i1);
       if (YN > 0 && YN < 8000)
       {  cout << "  " << "S" << YN << "      " << endl; //进行移进动作
          push(YN, sym);
          i++;
          if (sym == "ID")
             cp += 2;
          else
             cp += 1;
          //cp++;
          output();
       }
       else if (YN < 0)
       {  cout << "  " << "r" << -YN << "      "; //进行归约动作
          int sym2 = act(YN);     //执行利用产生式N的归约的动作
          pop(Yy_reduce[-YN]);     //从栈顶弹出N个符号（状态）；

          /*根据归约后的产生式的左部符号利用goto表将栈顶状态更新*/
          int *p1 = Yy_goto[stack1.stas[stack1.top1]];
          for (int i4 = (int) * p1++; i4-- > 0; p1 += 2)
             if (sym2 == p1[0])
             {  YN = p1[1];
                break;
             }
          cout << " " << YN << "  " << endl;
          push(YN, symbol2[sym2]);
          i++;
          //cp++;
          output();
       }
       else if (YN == 0)
       {  //accept();
          cout << "  " << "acc" << "     " << endl; //返回成功状态，LR分析停止工作
          cout << "分析结束，该句子是文法定义的一个句子。" << endl;
          break;
       }
       else
       {  //error();
          cout << " " << "出错" << "     " << endl; //提示出错信息，LR分析器停止工作
          cout << "分析结束，该句子不是文法定义的合法句子。" << endl;
          break;
       }
    }
    return 0;
}