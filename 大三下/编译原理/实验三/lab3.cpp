#include<iostream>
#include<fstream>
#include<iomanip>
#include "string"
#include<set>
#include<stack>
#define MAX 20
#define MAXSTACKSIZE 100
#define OFFSET 256
using namespace std;

typedef struct analysisStack //定义分析栈
{
    int data[MAXSTACKSIZE];
    int top;//栈顶指针
}sqstack;


string VN[]={"prgm","prgm'","expr","term","expr'","factor","term'","system_goal"};
string VT[]={"#",";","+","*","(",")","NUM"};
const int lenVN = 8, lenVT = 7;  //非终结符、终结符数量
int formsNum,lenForm = 0;//产生式数量,最大产生式长度
int formulas[MAX][MAX];//文法表达式，以符号编码代替具体内容
set<pair<int, int>> firstSet[lenVN];//first集合,第一个为终结符编号，第二个为产生式编号
bool visited[lenVN] = {false};  // 标记非终结符的FIRST集合是否已经计算过
int flag[lenVN];  // 标记非终结符的FOLLOW集合是否已经计算过
set<int> followSet[lenVN];//follow集合
int LLTable[lenVN][lenVT]; //LL(1)预测表
sqstack st;//递归分析栈


//函数声明
void initFormula(); //初始化文法表达式
bool isVT(int idx);  //是否是终结符
void getFirst(int target);   //求取指定非终结符的first集合
//这两个都可以实现，第一个需要借助辅助数组flag
void getFollow(int target);   //求取指定非终结符的follow集合
void getFollow();           //求取所有非终结符的follow集合

void getAllFirstAndFollow(int startFormula);  //求取所有的first和follow集合
void createLLTable();
void printTable();
void analyseProc(string str,int strCode[]);
void printAnalysisContent(int stTop, string str, int p); //p-活动指针
void strToNum(string str,int res[],int& len);   //将输入的字符串转成相应的编码

int main(){
    //1.初始化相关数据结构
    initFormula();
    getAllFirstAndFollow(263);  //文法的开始符是system_goal:263
    createLLTable();
    printTable();
    //2.输入字符串，进行分析
    string input;
    int inputCode[MAX],len;
    cout << "请输入要分析的字符串 (输入'回车'结束): ";
    cin>>input;
    input += '#';//加入结束符
    strToNum(input,inputCode,len);
    cout<<endl;
    cout<<"综合分析过程如下："<<endl;
    cout<<"栈(符号)                      "<<"栈(数值)                      "<<"输入串              "<<"What_to_do"<<endl;
    for(int i = 0; i < 100; ++i) cout<<"-";
    cout<<endl;
    analyseProc(input,inputCode);
    return 0;
}
//初始化文法表达式formulas
void initFormula() {
    std::ifstream file("../input.txt");
    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return;
    }
    std::string line;
    int row = 0;
    while (std::getline(file, line))
    {
        std::istringstream iss(line);
        int col = 0;
        int value;
        while (iss >> value)
        {
            formulas[row][col] = value;
            col++;
        }
        if(col > lenForm){lenForm = col;}
        row++;
    }
    formsNum = row;
    file.close();
    // for(int i = 0; i<50; i++){
    //     cout<<"-";
    // }
    cout<<endl;
    cout<<"LL(1)文法如下："<<endl;
    printf("\n");
    for(int i=0; i<formsNum; i++){
        cout<<i<<" ";
        //表达式左部
        int left = formulas[i][0];
        cout<<VN[left-OFFSET]<<"->";
        for(int j=1; j<lenForm; j++){
            int right = formulas[i][j];{
                if(right != -1){
                    // -1为空内容
                    if(right == 0){
                        cout<<"null"<<" ";
                    }
                    else if(right <= 6){
                        cout<<VT[right]<<" ";
                    }else{
                        cout<<VN[right-OFFSET]<<" ";
                    }
                }
            }
        }
        cout<<endl;
    }
    
    cout<<endl;
}

bool isVT(int idx){
    if(idx >=0 && idx <=6){return true;}
    else{return false;}
}

//求取指定字符的first集合
void getFirst(int target){
    for (int i = 0; i < formsNum; ++i) {
        if (formulas[i][0] - OFFSET == target) {
            // 找到该非终结符的产生式
            if (isVT(formulas[i][1])) {
                firstSet[target].insert({formulas[i][1], i});
            } else {
                //X->Y1...Yj..Yk
                bool canProduceEmpty = true;
                for (int j = 1; j < lenForm && formulas[i][j] != -1; ++j) {
                    int Yj = formulas[i][j];
                    if (isVT(Yj)) {
                        //1.递归出口-终结符，并加入集合(排除了空弧）
                        if (Yj != 0) {
                            firstSet[target].insert({Yj, i});
                            canProduceEmpty = false;
                        }
                        break;
                    } else {
                        int idx = Yj - OFFSET;  //非终结符索引
                        if (!visited[idx]) {
                            //该非终结符的first集合还未求取,递归，先求取
                            getFirst(idx);
                        }
                        bool hasEmpty = false;
                        for (auto elem: firstSet[idx]) {
                            if (elem.first != 0) {
                                firstSet[target].insert({elem.first, i});
                            } else {
                                hasEmpty = true;
                            }
                        }
                        if (!hasEmpty) {
                            canProduceEmpty = false;
                            break;
                        }
                    }
                }
                if (canProduceEmpty) {
                    //右部所有均能产生空弧，则空弧加入first(X)
                    firstSet[target].insert({0, i});
                }
            }
        }
    }
    visited[target] = true;
}

void getFollow(){
    bool changed = true;
    while (changed) {
        //直至所有follow集合不再变化结束求解
        changed = false;
        for (int i = 0; i < formsNum; ++i) {
            for (int j = 1; j < lenForm && formulas[i][j] != -1; ++j) {
                if (!isVT(formulas[i][j])) {
                    int B = formulas[i][j] - OFFSET;
                    int followSizeBefore = followSet[B].size();
                    //1.A->αBβ
                    if (formulas[i][j + 1] != -1 && j + 1 < lenForm) {
                        int beta = formulas[i][j + 1];
                        if (isVT(beta) && beta != 0) {
                            //1.1 β为终结符，直接插入
                            followSet[B].insert(beta);
                        } else {
                            //1.2 β为非终结符
                            int idx = beta - OFFSET;  //Vn索引
                            for (auto elem : firstSet[idx]) {
                                //将beta的first集合除去空弧加入follow(B)
                                if (elem.first != 0) {
                                    followSet[B].insert(elem.first);
                                }
                            }
                            //1.3 β->空弧，则将follow(A)加入follow(B)中
                            for(const auto& elem : firstSet[idx]) {
                                if(elem.first == 0){
                                    int A = formulas[i][0] - OFFSET;
                                    for (auto elem : followSet[A]) {
                                        followSet[B].insert(elem);
                                    }
                                }
                            }
                        }
                    } else {
                        //2.A->αB
                        int A = formulas[i][0] - OFFSET;
                        for (auto elem : followSet[A]) {
                            followSet[B].insert(elem);
                        }
                    }

                    if (followSet[B].size() > followSizeBefore) {
                        changed = true;
                    }
                }
            }
        }
    }
}

void getAllFirstAndFollow(int start){
    //1.求取first集合
    for(int i = 0; i < lenVN; ++i){
        getFirst(i);
    }
    //2.求取follow
//    for(int i = 0; i<lenVN; ++i){flag[i] = -1;}
//    followSet[start-OFFSET].insert(0);
//    for(int i = 0; i < lenVN; ++i){
//        getFollow(i);
//    }
    followSet[start-OFFSET].insert(0);//初始状态加入#
    getFollow();
    cout<<"First集如下："<<endl;
    //输出结果
    for(int i = 0; i < lenVN; ++i){
        cout<<"First("<<VN[i]<<")={";
        int tmp=0;
        for(auto elem : firstSet[i]){
            if(elem.first == 0){
                cout<<"null";
            }else{
                cout<<VT[elem.first];
            }
            tmp++;
            if(tmp!=firstSet[i].size()) cout<<",";
        }
        cout<<"}"<<endl;
    }
    printf("\n\n");
    cout<<"Follow集如下："<<endl;
    //输出结果
    for(int i = 0; i < lenVN; ++i){
        cout<<"Follow("<<VN[i]<<")={";
        int tmp=0;
        for(int j : followSet[i]){
            if(j == 0){
                cout<<"#";
            }else{
                cout<<VT[j];
            }
            tmp++;
            if(tmp!=followSet[i].size()) cout<<",";
        }
        cout<<"}"<<endl;
    }
    // for(int i=0;i<50;i++){cout<<"-";}
    cout<<endl;
}

void createLLTable() {
    //初始化
    for(int i = 0; i < lenVN; ++i){
        for(int j = 0; j < lenVT; ++j)
            LLTable[i][j]=-1;
    }
    //根据first集合和follow集合更新
    for(int i = 0; i < lenVN; ++i){
        for(auto elem : firstSet[i]){
            if(elem.first != 0) {
                LLTable[i][elem.first]=elem.second;
            }
            else{
                //存在空弧属于first(i)，则将所有的follow(i)加入table中
                for(auto j : followSet[i]){
                    LLTable[i][j] = elem.second;
                }
            }
        }
    }
}

void printTable(){
    cout<<"预测分析表如下："<<endl;
    cout << setw(12)<<VT[0];
    for (int i = 1; i < lenVT; i++) {
        cout << setw(5) << VT[i];
    }
    cout << endl;

    for (int i = 0; i < lenVN; i++) {
        // 设置行标题的宽度，假设最长的行标题是 "system_goal"，长度为 11
        cout << setw(11) << left << VN[i];
        for (int j = 0; j < lenVT; j++) {
            // 使用 setiosflags(ios::left) 来设置左对齐
            cout << setiosflags(ios::left) << setw(5) << LLTable[i][j];
        }
        cout << endl;
    }
    cout << endl;
    // for(int i = 0; i<50;++i) cout<<"-";
    cout<<endl;
}

//编码转换
void strToNum(string str,int res[],int& len){
    len = str.size();
    for(int i=0;i<len;i++)
    {
        switch(str[i])
        {
            case'(': res[i]=4; break;
            case'+': res[i]=2; break;
            case')': res[i]=5; break;
            case';': res[i]=1; break;
            case'*': res[i]=3; break;
            case'#': res[i]=0; break;
            default:res[i]=7;

        }

        if(str[i]>='0'&&str[i]<='9')
            res[i]=6;
    }
}

//打印分析内容
void printAnalysisContent(int stTop, string str, int p){
    int strlen=0,numlen = 0;
    for (int i = 0; i <= stTop; ++i) {
        string elem = (st.data[i] <= 6) ? VT[st.data[i]] : VN[st.data[i] - OFFSET];
        cout << elem << " ";
        strlen = strlen +elem.size() + 1;   //+1空格
    }

    for(int i = strlen; i < 30; ++i) cout<<" ";

    // 栈（数值）
    for (int i = 0; i <= stTop; ++i) {
        cout << st.data[i] << " "; //
        numlen = to_string(st.data[i]).size() + numlen + 1;
    }
    for(int i = numlen; i < 30; ++i) cout<<" ";
    // 输入串
    for (int i = p; i < str.size(); ++i) {
        cout << str[i];
    }
    for(int i = 0; i < 20-str.size()+p; i++) cout<<" ";
}

//文法分析
void analyseProc(string str,int strCode[]){
    //初始化栈
    st.top = -1;
    st.top++;
    st.data[st.top] = 263; //将system_goal压入栈中
    int p = 0,action;    //活动指针
    while(st.top != -1){
        //栈非空开始分析
        printAnalysisContent(st.top,str,p);
        int topNum = st.data[st.top];
        int strNum = strCode[p];
        if(isVT(topNum)){
            //栈顶元素是终结符
            if(topNum != strNum){
                //报错
                cout<<"Failed to analyse this syntax!"<<endl;
                break;
            }else{
                st.top--; //出栈该元素
                p++;
                cout<<endl;
            }
        }else{
            //栈顶元素是非终结符
            //根据LLTable获取下一步动作
            action = LLTable[topNum-OFFSET][strNum];
            cout<<action<<endl;
            if(action == -1){
                //报错
                cout<<str<<"Failed to analyse this syntax!"<<endl;
                break;
            }else{
                st.top--;  //出栈该元素,进行推导
                for(int i = lenForm -1 ; i > 0; --i ){
                    //-1是为了使每个产生式规则一致填充的数组
                    //0 表示空弧推导
                    int code = formulas[action][i];
                    if(code != -1 && code != 0){
                        //将formulas中的产生式规则逆序押进栈中
                        st.top++;
                        st.data[st.top] = code;
                    }
                }
            }
        }
        if(st.top == -1 && strCode[p] == 0){
            for(int i=0;i<100;i++) cout<<"-";
            cout<<endl;
            cout<< str <<"    is valid syntax!"<<endl;
        }
    }

}
