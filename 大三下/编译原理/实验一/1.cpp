#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAXLENGTH 255
#define MAXIDENTIFIERS 1000

// 关键字表
char *KEY_WORDS[7] = {"main", "int", "char", "if", "else", "for", "while"};

// 符号表
typedef struct {
    char *symbol;
    int code;
} Symbol;

Symbol SYMBOLS[] = {
        {"=", 21}, {"+", 22}, {"-", 23}, {"*", 24}, {"/", 25},
        {"(", 26}, {")", 27}, {"[", 28}, {"]", 29}, {"{", 30},
        {"}", 31}, {",", 32}, {":", 33}, {";", 34}, {">", 35},
        {"<", 36}, {">=", 37}, {"<=", 38}, {"==", 39}, {"!=", 40},
        {"&", 41}, {"&&", 42}, {"||", 43}
};

// 标识符表
char IdentifierTbl[MAXIDENTIFIERS][MAXLENGTH] = {""};

// 单词符号二元式数据结构
typedef struct {
    int code;        // 存放种别编码
    char value[MAXLENGTH]; // 存放单词符号的内容
} WORD;

int findSymbolCode(const char *symbol) {
    for (int i = 0; i < sizeof(SYMBOLS) / sizeof(Symbol); i++) {
        if (strcmp(SYMBOLS[i].symbol, symbol) == 0) {
            return SYMBOLS[i].code;
        }
    }
    return -1; // Symbol not found
}

int isKeyword(char *str) {
    for (int i = 0; i < 7; i++) {
        if (strcmp(KEY_WORDS[i], str) == 0) {
            return i + 1; // 返回关键字对应的种别编码
        }
    }
    return 0;
}

// 过滤注释
void filterResource(char r[]) {
    char tempString[MAXLENGTH * 10];
    int count = 0;
    for (int i = 0; r[i] != '\0'; i++) {
        if (r[i] == '/' && r[i + 1] == '/') {
            while (r[i] != '\n' && r[i] != '\0') {
                i++;
            }
        }
        if (r[i] == '/' && r[i + 1] == '*') {
            i += 2;
            while (r[i] != '*' || r[i + 1] != '/') {
                i++;
                if (r[i] == '\0') {
                    printf("注释出错, 没有找到 */, 程序结束!！！\n");
                    exit(0);
                }
            }
            i += 2;
        }
        if (r[i] != '\n' && r[i] != '\t' && r[i] != '\v' && r[i] != '\r') {
            tempString[count++] = r[i];
        }
    }
    tempString[count] = '\0';
    strcpy(r, tempString);
}

WORD Scanner(const char *source, int *index) {
    WORD word = {0, ""};
    char buffer[MAXLENGTH] = {0};
    int j = 0;
    char currentChar;

    while ((currentChar = source[*index]) != '\0') {
        (*index)++;
        if (isspace(currentChar)) {
            if (j != 0) break; // 单词结束
        } else if (isalpha(currentChar)) {
            buffer[j++] = currentChar; // 继续读取标识符或关键字
            while (isalnum(source[*index]) || source[*index] == '_') {
                buffer[j++] = source[*index];
                (*index)++;
            }
            break;
        } else if (isdigit(currentChar)) {
            buffer[j++] = currentChar; // 继续读取数字
            while (isdigit(source[*index])) {
                buffer[j++] = source[*index];
                (*index)++;
            }
            break;
        } else {
            if (j != 0) {
                (*index)--; // 返回到符号前
                break;
            } else {
                buffer[j++] = currentChar;
                if ((strchr("=<>!", source[*index]) && source[*index] == '=')
                    || (currentChar == '&' && source[*index] == '&') ||
                    (currentChar == '|' && source[*index] == '|')) { // 处理双字符运算符
                    buffer[j++] = source[*index];
                    (*index)++;
                }
                break;
            }
        }
    }

    buffer[j] = '\0'; // null - terminate the buffer

    // 查找符号表以获取相应的代码
    if (isdigit(buffer[0])) {
        word.code = 20; // 整型常数
    } else if (isalpha(buffer[0])) {
        int key = isKeyword(buffer);
        if (key) {
            word.code = key; // 关键字
        } else {
            word.code = 10; // 标识符
        }
    } else {
        word.code = findSymbolCode(buffer); // 操作符或界符
        if (word.code == -1) {
            // printf("Error: Unrecognized symbol %s\n", buffer);
            exit(1);
        }
    }
    strcpy(word.value, buffer);

    return word;
}

void analyzeSource(const char *source, FILE *outputFile) {
    int index = 0;
    WORD word;
    while ((word = Scanner(source, &index)).code != 0) {
        if (word.code == 10) { // 处理标识符
            int i;
            for (i = 0; i < MAXIDENTIFIERS; i++) {
                if (strcmp(IdentifierTbl[i], word.value) == 0) {
                    break;
                }
                if (strcmp(IdentifierTbl[i], "") == 0) {
                    strcpy(IdentifierTbl[i], word.value);
                    break;
                }
            }
        }
        // 输出到命令行
        printf("(%d,%s) \n", word.code, word.value);
        // 输出到文件
        fprintf(outputFile, "(%d,%s) \n", word.code, word.value);
    }
}

void printIdentifierTable(FILE *outputFile) {
    for (int i = 0; i < MAXIDENTIFIERS && IdentifierTbl[i][0] != '\0'; i++) {
        // 输出到命令行
        printf("第%d个标识符: %s\n", i + 1, IdentifierTbl[i]);
        // 输出到文件
        fprintf(outputFile, "第%d个标识符: %s\n", i + 1, IdentifierTbl[i]);
    }
}

int main() {
    const char source[] = "main()\n{\nint i = 10;\nwhile(i) i = i - 1;\n}";
    // 对源程序进行过滤处理
    char filteredSource[MAXLENGTH * 10];
    strcpy(filteredSource, source);
    filterResource(filteredSource);

    // 打开文件以写入结果
    FILE *outputFile = fopen("output.txt", "w");
    if (outputFile == NULL) {
        printf("无法打开文件！\n");
        return 1;
    }

    printf("\n二元式代码序列为:\n");
    fprintf(outputFile, "\n二元式代码序列为:\n");
    // 读取二元式代码序列并进行处理
    analyzeSource(filteredSource, outputFile);

    // 输出标识符表
    printf("\n标识符表为:\n");
    fprintf(outputFile, "\n标识符表为:\n");
    printIdentifierTable(outputFile);

    // 关闭文件
    fclose(outputFile);

    return 0;
}    