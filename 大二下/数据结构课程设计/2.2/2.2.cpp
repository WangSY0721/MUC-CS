#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 100

typedef struct Node {
    char name[MAX_SIZE];
    struct Node *child;
    struct Node *sibling;
    struct Node *parent;
} Node;

typedef struct List{
    Node *head;
};

// 创建节点
Node* createNode(const char* name) {
    Node *node = (Node *)malloc(sizeof(Node));
    strcpy(node->name, name);
    node->child = NULL;
    node->sibling = NULL;
    node->parent = NULL;
    return node;
}

Node* parseList(char **str);

Node* parseList(char **str) {
    if (**str == '\0' || **str == ')') return NULL;

    char name[50];
    int i = 0;
    while (**str != '\0' && **str != ',' && **str != '(' && **str != ')') {
        name[i++] = **str;
        (*str)++;
    }
    name[i] = '\0';
    Node* node = createNode(name);
    if (**str == '('&& i!= 0) {
        (*str)++;
        node->child = parseList(str);
        node->child->parent = node;
    }
    if(i == 0 && **str == '('){
        (*str)++;
        node = parseList(str);
        node->parent = NULL;
    }
    if (**str == ')') {
        (*str)++;
        return node;
    }
    if (**str == ',') {
        (*str)++;
        node->sibling = parseList(str);
    }
    return node;
}

List* readFromFile(const char *filename) {
    // 尝试以只读模式打开文件
    FILE *file = fopen(filename, "r");
    if (!file) {
        // 如果文件无法打开，打印错误信息并返回NULL
        printf("无法打开文件 %s\n", filename);
        return NULL;
    }

    // 分配缓冲区用于读取文件内容
    char* buffer = (char*)malloc(1024 * sizeof(char));
    // 读取文件内容到缓冲区
    size_t bytesRead = fread(buffer, sizeof(char), 1024, file);
    // 关闭文件
    fclose(file);

    // 将缓冲区指针赋值给str，用于后续解析
    char* str = buffer;
    // 分配List结构体的内存
    List* list = (List*)malloc(sizeof(List));
    // 解析字符串并将结果赋值给list的头节点
    list->head = parseList(&str);

    // 释放缓冲区内存
    free(buffer);
    // 返回解析后的列表结构
    return list;
}


// 显示树结构
void displayTree(Node *root, int level) {
    // 如果当前节点为空，直接返回
    if (root == NULL) return;

    // 根据当前层级打印缩进
    for (int i = 0; i < level; i++) {
        printf("  ");
    }

    // 打印当前节点的名称
    printf("%s\n", root->name);

    // 递归显示子节点，层级增加1
    displayTree(root->child, level + 1);

    // 递归显示兄弟节点，层级保持不变
    displayTree(root->sibling, level);
}

// 显示链表中的所有节点
void displayList(Node* head, int level) {
    Node *current = head;
    // 遍历链表中的每个节点
    while (current != NULL) {
        // 显示当前节点及其子树
        displayTree(current, level);
        // 移动到下一个兄弟节点
        current = current->sibling;
    }
}

// 显示整个树列表
void displayGeneralizedList(List *list) {
    // 如果列表为空或头节点为空，打印提示信息
    if (list == NULL || list->head == NULL) {
        printf("行政表为空\n");
        return;
    }

    // 显示列表的树结构，从头节点开始，初始层级为0
    displayTree(list->head, 0);
}

// 查找节点
Node* findNode(Node *list, const char *name) {
    // 将输入的列表（子树的根节点）赋值给局部变量 root
    Node *root = list;

    // 如果当前节点为空，返回 NULL
    if (root == NULL) return NULL;

    // 比较当前节点的名称与目标名称，如果匹配，返回当前节点
    if (strcmp(root->name, name) == 0) return root;

    // 递归查找当前节点的子节点
    Node *result = findNode(root->child, name);
    // 如果在子节点中找到匹配的节点，返回该节点
    if (result != NULL) return result;

    // 递归查找当前节点的兄弟节点
    return findNode(root->sibling, name);
}

// 查找并显示所有下属行政单位
void displaySubordinateUnits(Node *root, const char *name) {
    Node *node = findNode(root, name);
    if (node) {
        displayTree(node->child, 1);
    } else {
        printf("未找到指定的行政单位 %s\n", name);
    }
}

// 查找并显示所有上属行政单位
void displayAncestorUnits(Node *root, const char *name) {
    Node *node = findNode(root, name);
    Node *p = createNode(root->name);
    if (root) {
        while (node) {
            printf("%s\n", node->name);
            node = node->parent;
        }
    } else {
        printf("未找到指定的行政单位 %s\n", name);
    }
}

// 统计节点数量
int countNodes(Node *root) {
    if (root == NULL) return 0;
    return 1 + countNodes(root->child) + countNodes(root->sibling);
}

// 统计县级或乡镇节点数量
int countxianxiang(Node *root) {
    if (root == NULL) return 0;
    if (strstr(root->name, "县") != NULL || strstr(root->name, "乡") != NULL || strstr(root->name, "镇") != NULL) {
        return 1 + countxianxiang(root->child) + countxianxiang(root->sibling);
    }
    return countxianxiang(root->child) + countxianxiang(root->sibling);
}

// 统计无下属节点数量
int noxiashu(Node *root) {
    if (root == NULL) return 0; // 根节点为空，返回0
    if (root->child == NULL) {
        // 当前节点没有子节点，返回1加上兄弟节点中的无下属节点数量
        return 1 + noxiashu(root->sibling);
    }
    // 当前节点有子节点，递归统计子节点和兄弟节点中的无下属节点数量
    return noxiashu(root->child) + noxiashu(root->sibling);
}

// 插入新的行政单位
void insertNode(Node *root, const char *parentName, const char *name) {
    // 查找指定名称的父节点
    Node *parent = findNode(root, parentName);
    if (parent == NULL) {
        printf("未找到父节点 %s\n", parentName);
        return;
    }

    // 创建新节点
    Node *newNode = createNode(name);
    newNode->parent = parent;

    // 将新节点插入为父节点的子节点
    if (parent->child == NULL) {
        parent->child = newNode;
    } else {
        Node *sibling = parent->child;
        // 找到子节点链表的最后一个节点
        while (sibling->sibling != NULL) {
            sibling = sibling->sibling;
        }
        // 插入新节点为最后一个节点的兄弟节点
        sibling->sibling = newNode;
    }

    printf("已插入节点 %s 到 %s 下\n", name, parentName);
}

// 删除指定的行政单位
void deleteNode(Node **root, const char *name) {
    Node *node = findNode(*root, name);
    if (node == NULL) {
        printf("未找到节点 %s\n", name);
        return;
    }
    if (node == *root) {
        *root = (*root)->sibling;
        free(node);
        return;
    }
    Node *parent = node->parent;
    if (parent != NULL) {
        if (parent->child == node) {
            parent->child = node->sibling;
        } else {
            Node *sibling = parent->child;
            while (sibling->sibling != node) {
                sibling = sibling->sibling;
            }
            sibling->sibling = node->sibling;
        }
    }
    free(node);
    printf("已删除节点 %s\n", name);
}

int countLevels(Node *root) {
    if (root == NULL) return 0;
    int maxChildLevel = 0;
    Node *sli = root;
    while(sli){
        Node *child = sli->child;
        while (child != NULL) {
            int childLevel = countLevels(child);
            if (childLevel > maxChildLevel) {
                maxChildLevel = childLevel;
            }
            child = child->sibling;
        }
        sli = sli ->sibling;
    }
    return maxChildLevel +1;
}


// 打印指定级别的行政单位
void printLevel(Node *root, int level, int currentLevel) {
    if (root == NULL) return;
    if (level == currentLevel) {
        printf("%s\n", root->name);
    }
    printLevel(root->child, level, currentLevel + 1);
    printLevel(root->sibling, level, currentLevel);
}

// 菜单操作
void menu(List *root) {
    int choice;
    char name[100], parentName[100];
    int level;

    while (1) {
        printf("\n菜单:\n");
        printf("1. 显示行政区划\n");
        printf("2. 查找并显示所有下属行政单位\n");
        printf("3. 查找并显示所有上属行政单位\n");
        printf("4. 统计总体行政单位个数\n");
        printf("5. 统计县级或乡镇行政单位个数\n");
        printf("6. 统计无下属行政单位个数\n");
        printf("7. 求出行政级别数\n");
        printf("8. 显示指定级别的行政单位\n");
        printf("9. 插入新的行政单位\n");
        printf("10. 删除指定行政单位\n");
        printf("11. 退出\n");
        printf("请输入选择: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                displayGeneralizedList(root);
                break;


            case 2:
            {
                printf("请输入行政单位名称: ");
                scanf("%s", name);
                displaySubordinateUnits(root->head,name);
            }
                break;
            case 3:
            {
                printf("请输入行政单位名称: ");
                scanf("%s", name);
                displayAncestorUnits(root->head,name);
            }
                break;
            case 4:
                printf("总体行政单位个数: %d\n", countNodes(root->head));
                break;
            case 5:
                printf("县级或乡镇行政单位个数: %d\n", countxianxiang(root->head));
                break;
            case 6:
                printf("无下属行政单位个数: %d\n", noxiashu(root->head));
                break;
            case 7:
                printf("行政级别数: %d\n", countLevels(root->head));//因为文件根root 没有名称，但是算入级别数，故统计时减去根
//				displayList(root->head,countLevels(root->head));
                break;
            case 8:
                printf("请输入级别: ");
                scanf("%d", &level);
                printLevel(root->head, level, 1);
                break;
            case 9:
                printf("请输入父级行政单位名称: ");
                scanf("%s", parentName);
                printf("请输入新的行政单位名称: ");
                scanf("%s", name);
                insertNode(root->head, parentName, name);
                break;
            case 10:
                printf("请输入要删除的行政单位名称: ");
                scanf("%s", name);
                deleteNode(&root->head, name);
                break;
            case 11:
                return;
            default:
                printf("无效选择，请重新输入\n");
        }
    }
}

int main() {
    List *root = readFromFile("cities.txt");
    if (root == NULL) {
        printf("读取文件失败\n");
        return -1;
    }
    menu(root);
    return 0;
}
