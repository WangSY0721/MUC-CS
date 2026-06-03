#include <iostream>
#include <fstream>
#include <set>
#include <queue>
#include <vector>
#include <map>
#include <iomanip> // for std::setw

using namespace std;

const int N = 100;

class Graph
{
public:
    //集合序号
    char index;
    //状态数量
    int StateNum;
    //初始点数量、终止点数量
    int StartNum, StopNum;
    //转换函数数量，字符集大小
    int TransNum, LetterSize;
    //终止状态集合，初始状态集合
    int StopState[N], StartState;
    //字符集合
    char LetterSet[N];
    //状态集合
    set< pair<char, set<int> > > stateSet;
    //状态队列
    queue< set<int> > stateQueue;
    //当前状态集合
    set<int> currentState;
    //转换集合
    vector<pair<int, char> > Edge[N];
    Graph();
    //建图
    void BuildGraph(const string& filename);
    //添加转换条件
    void add(int a, int b, char signal);
    //NFA确定化
    void deterDFA();
    //状态查找函数
    int findState(set<int>);
    //重载求闭包函数
    set<int> getClosure(int cur);
    set<int> getClosure(set<int> cur);
    set<int> getClosure(set<int> cur, char signal);
    //展示结果
    void showDFA();
protected:
};

Graph::Graph()
{
    //从A开始编状态集合名称
    index = 'A';
}

void Graph::BuildGraph(const string& filename)
{
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "无法打开文件: " << filename << endl;
        return;
    }

    //读入状态数量
    file >> StateNum;
    cout << "StateNum:" << StateNum << endl;
    //读入初始状态
    file >> StartState;
    cout << "StartState:" << StartState << endl;
    //读入终止状态
    file >> StopNum;
    for (int i = 0; i < StopNum; i++)
    {
        file >> StopState[i];
    }
    cout << "StopNum:" << StopNum << endl;
    cout << "StopState:";
    for (int i = 0; i < StopNum; i++)
    {
        cout << StopState[i] << ' ';
    }
    cout << endl;

    //读入字符集合
    file >> LetterSize;
    for (int i = 0; i < LetterSize; i++)
    {
        file >> LetterSet[i];
    }
    cout << "LetterSize:" << LetterSize << endl;
    cout << "LetterSet:";
    for (int i = 0; i < LetterSize; i++)
    {
        cout << LetterSet[i] << ' ';
    }
    cout << endl;

    //读入转换函数
    file >> TransNum;
    for (int i = 0; i < TransNum; i++)
    {
        int a, b;
        char w;
        file >> a >> w >> b;
        add(a, b, w);
    }
    cout << "TransNum:" << TransNum << endl;
    cout << "Trans:" << endl;
    for (int i = 0; i < StateNum; i++)
    {
        if (Edge[i].size() == 0) continue;
        for (auto k : Edge[i])
        {
            cout << i << ' ' << k.second << ' ' << k.first << endl;
        }
    }

    file.close();
}

//a代表起点，b代表终点，signal代表对应字符
void Graph::add(int a, int b, char signal)
{
    Edge[a].push_back({ b, signal });
}

//查找状态集中是否有当前状态
int Graph::findState(set<int> cur)
{
    for (auto k : stateSet)
    {
        if (k.second == cur)
            return 1;
    }
    return -1;
}

//求状态集合为cur,字符为signal的Closure
set<int> Graph::getClosure(set<int> cur, char signal)
{
    set<int> newset;
    for (set<int>::iterator it = cur.begin(); it != cur.end(); it++)
    {
        for (auto k : Edge[*it])
        {
            //cout<<k.first<<' '<<k.second<<endl;
            if (k.second == signal)
            {
                newset.insert(k.first);
                //cout<<k.first<<endl;
            }
        }
    }
    return newset;
}

//求状态集合为cur的ε-Closure ('#'表示ε弧)
set<int> Graph::getClosure(set<int> cur)
{
    set<int> newset = cur;
    queue<int> q;
    set<int> visited; // Add a visited set to track visited states
    for (set<int>::iterator it = cur.begin(); it != cur.end(); it++)
    {
        q.push(*it);
        visited.insert(*it); // Mark the state as visited
    }
    while (!q.empty())
    {
        int t = q.front();
        q.pop();
        set<int> newele = getClosure(t);
        for (set<int>::iterator it = newele.begin(); it != newele.end(); it++)
        {
            if (visited.find(*it) == visited.end()) // Check if the state is already visited
            {
                q.push(*it);
                newset.insert(*it);
                visited.insert(*it); // Mark the new state as visited
            }
        }
    }
    return newset;
}

//求状态只有cur的ε-Closure
set<int> Graph::getClosure(int cur)
{
    set<int> newset;
    for (auto k : Edge[cur])
    {
        if (k.second == '#')
            newset.insert(k.first);
    }
    return newset;
}

//NFA确定化
void Graph::deterDFA()
{
    int start = StartState;
    //将初始状态加到当前状态集合
    currentState.insert(start);
    //求ε-Closure得到I
    currentState = getClosure(currentState);
    //将I加到状态集合和队列
    stateSet.insert({ index, currentState });
    stateQueue.push(currentState);
    cout << "----------------------------------" << endl;
    cout << " I        Ia        Ib" << endl;
    cout << "----------------------------------" << endl;
    //当状态集合队列不为空
    while (!stateQueue.empty())
    {
        //取队头状态集合并弹出，依次求其I,Ia和Ib
        auto temp = stateQueue.front();
        for (auto k : stateSet)
        {
            if (k.second == temp)
                cout << " " << k.first;
        }
        stateQueue.pop();
        //求Ia, Ib ...
        for (int j = 0; j < LetterSize; j++)
        {
            currentState = temp;
            //先求对应字符的Closure
            currentState = getClosure(temp, LetterSet[j]);
            //再求该Closure的ε-Closure
            currentState = getClosure(currentState);
            if (currentState.size() > 0)
            {
                if (findState(currentState) == -1)
                {
                    //若求得的状态集合没有出现在总的状态集合和队列中，则加入
                    stateSet.insert({ ++index, currentState });
                    stateQueue.push(currentState);
                }
                for (auto k : stateSet)
                {
                    //取出该状态集合对应的字母名称
                    if (k.second == currentState)
                        cout << "\t\t" << k.first;
                }
            }
        }
        cout << endl;
    }
    cout << "----------------------------------" << endl;
}

void Graph::showDFA()
{
    cout << "DFA States and their compositions:" << endl;
    for (auto k : stateSet)
    {
        char id = k.first;
        auto state = k.second;
        cout << id << ' ';
        bool isFinal = false;

        for (set<int>::iterator it = state.begin(); it != state.end(); it++)
        {
            cout << *it << ' ';
            for (int i = 0; i < StopNum; i++)
            {
                if (*it == StopState[i])
                {
                    isFinal = true;
                }
            }
        }

        cout << (isFinal ? "(Final State)" : "") << endl;
    }

    // Printing the transition matrix
    cout << "\nDFA Transition Matrix:" << endl;
    cout << "State ";
    for (int j = 0; j < LetterSize; j++)
    {
        cout << std::setw(5) << LetterSet[j] << " ";
    }
    cout << endl;

    for (auto k : stateSet)
    {
        char id = k.first;
        cout << id << "     ";
        for (int j = 0; j < LetterSize; j++)
        {
            currentState = k.second;
            currentState = getClosure(k.second, LetterSet[j]);
            currentState = getClosure(currentState);

            if (currentState.size() > 0)
            {
                for (auto state : stateSet)
                {
                    if (state.second == currentState)
                    {
                        cout << std::setw(5) << state.first << " ";
                    }
                }
            }
            else
            {
                cout << std::setw(5) << "-" << " ";
            }
        }
        cout << endl;
    }
}

Graph G;
int main()
{
    G.BuildGraph("input.txt");
    G.deterDFA();
    G.showDFA();
    return 0;
}