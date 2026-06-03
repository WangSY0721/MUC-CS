#ifndef GRAPH_H
#define GRAPH_H
#include<cstring>
#include<iostream>
#include<fstream>
#include<vector>
#include<set>
#include<queue>
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
    void BuildGraph();
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

#endif