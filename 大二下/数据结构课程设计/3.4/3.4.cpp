#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LEN 100

// 家庭成员节点结构定义
typedef struct FamilyMember {
    char name[MAX_NAME_LEN];
    struct FamilyMember* child;
    struct FamilyMember* sibling;
} FamilyMember;

// 创建新家庭成员节点
FamilyMember* createFamilyMember(const char* name) {
    FamilyMember* newMember = (FamilyMember*)malloc(sizeof(FamilyMember));
    strcpy(newMember->name, name);
    newMember->child = NULL;
    newMember->sibling = NULL;
    return newMember;
}

// 查找家庭成员节点
FamilyMember* findFamilyMember(FamilyMember* root, const char* name) {
    // 如果当前节点为空，返回 NULL
    if (root == NULL) return NULL;

    // 比较当前节点的名称与目标名称，如果匹配，返回当前节点
    if (strcmp(root->name, name) == 0) return root;

    // 递归查找当前节点的子节点
    FamilyMember* found = findFamilyMember(root->child, name);
    // 如果在子节点中找到匹配的成员，返回该成员
    if (found) return found;

    // 递归查找当前节点的兄弟节点
    return findFamilyMember(root->sibling, name);
}


// 插入孩子到家庭成员节点
void insertChild(FamilyMember* parent, FamilyMember* child) {
    // 如果父节点没有孩子，直接将新孩子节点设置为父节点的第一个孩子
    if (parent->child == NULL) {
        parent->child = child;
    } else {
        // 父节点已有孩子，遍历孩子链表找到末尾
        FamilyMember* sibling = parent->child;
        while (sibling->sibling != NULL) {
            sibling = sibling->sibling;
        }
        // 将新孩子节点插入到链表的末尾
        sibling->sibling = child;
    }
}


// 从文件中读入家庭成员并建立家谱
FamilyMember* buildFamilyTree(const char* filename) {
    // 打开文件
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("无法打开文件");
        return NULL;
    }

    // 初始化变量
    FamilyMember* root = NULL;
    char line[256];
    char parentName[MAX_NAME_LEN], childName[MAX_NAME_LEN];

    // 读取文件中的每一行
    while (fgets(line, sizeof(line), file)) {
        line[strcspn(line, "\n")] = '\0'; // 去掉换行符
        char* token = strtok(line, "(");
        if (!token) continue;

        // 获取父母名字
        strcpy(parentName, token);

        // 查找或创建父母节点
        FamilyMember* currentParent = findFamilyMember(root, parentName);
        if (!currentParent) {
            currentParent = createFamilyMember(parentName);
            if (root == NULL) {
                root = currentParent;
            } else {
                // 找到树中的最后一个父母节点，并将新的父母节点插入到它的兄弟链中
                FamilyMember* lastParent = root;
                while (lastParent->sibling != NULL) {
                    lastParent = lastParent->sibling;
                }
                lastParent->sibling = currentParent;
            }
        }

        // 处理孩子节点
        token = strtok(NULL, ")");
        if (!token) continue;

        char* childToken = strtok(token, ",");
        while (childToken != NULL) {
            strcpy(childName, childToken);
            FamilyMember* child = createFamilyMember(childName);
            insertChild(currentParent, child);
            childToken = strtok(NULL, ",");
        }
    }

    // 关闭文件并返回根节点
    fclose(file);
    return root;
}

void printFamilyTree(FamilyMember* root, int level) {
    if (root == NULL) return;
    for (int i = 0; i < level; ++i) {
        printf("  ");
    }
//	printf("level:%d ",level);
    printf("%s\n", root->name);

    printFamilyTree(root->child, level + 1);

    printFamilyTree(root->sibling, level);
}

// 计算家族代数
int calculateGenerations(FamilyMember* root) {
    if (root == NULL) return 0;
//	printf("%s ",root->name);
    int childDepth = calculateGenerations(root->child);
//	printf(" %d ",childDepth);
    int siblingDepth = calculateGenerations(root->sibling)-1;
//	printf("\n");
//	printf("%sslibingdepth:%d\n",root->name,siblingDepth);
    return 1 + (childDepth > siblingDepth ? childDepth : siblingDepth);
}

// 统计指定辈份的人数并显示
int countGenerationMembers(FamilyMember* root, int targetLevel, int currentLevel) {
    // 如果当前节点为空，返回 0
    if (root == NULL) return 0;

    // 定义计数变量
    int childCount = 0, siblingCount = 0;

    // 检查当前节点是否在目标层级
    if (currentLevel == targetLevel) {
        // 打印当前节点的名字
        printf("%s ", root->name);
        // 当前节点是目标层级的一个成员
        siblingCount = 1;
    }

    // 递归统计子节点中的符合条件的成员数量
    childCount = countGenerationMembers(root->child, targetLevel, currentLevel + 1);

    // 递归统计兄弟节点中的符合条件的成员数量
    siblingCount += countGenerationMembers(root->sibling, targetLevel, currentLevel);

    // 返回子节点和兄弟节点中符合条件的成员数量之和
    return childCount + siblingCount;
}


// 查找指定人并显示其祖先和所有后代
void findMemberAndDisplayAncestorsDescendants(FamilyMember* root, const char* name) {
    FamilyMember* member = findFamilyMember(root, name);
    if (!member) {
        printf("未找到成员 %s\n", name);
        return;
    }

    // 显示祖先
    printf("祖先: ");
    FamilyMember* temp = root;
    while (temp != NULL) {
        if (findFamilyMember(temp, name)) {
            printf("%s ", temp->name);
        }
        temp = temp->sibling;
    }
    printf("\n");

    // 显示后代
    printf("后代: ");
    printFamilyTree(member->child, 0);
    printf("\n");
}

// 查找最近祖先的辅助函数
FamilyMember* findClosestAncestorHelper(FamilyMember* root, FamilyMember* member1, FamilyMember* member2) {
	int count = 0;
    if (root == NULL) return NULL;
//	printf("%s\n",root->name);
	
    if (root == member1 || root == member2) return root;
	FamilyMember* p = root->child;
    FamilyMember* left = findClosestAncestorHelper(p, member1, member2);//子树
	if(left){
		count++;
//		printf("%s ",left->name);	
	}
	FamilyMember* right;
	right = NULL;
	if(p){
		p = p->sibling;
		while(p&& count<2){
			right = findClosestAncestorHelper(p, member1, member2);
			if(right){
				count++;
//				printf("%s ",right->name);
				if(!left){
					left = right;//借left存right
				}
			}
			p = p->sibling;
		}
		
		if (count == 2) {
//			printf("%s",root->name);
			//		count = 0;
			return root;
		}
		
		//找到，返回祖先
		return left?left:right;//找到一个
	}
	else{
		return left?left:right;
	}
}

// 查找两个人的最近祖先
FamilyMember* findClosestAncestorHelper(FamilyMember* root, FamilyMember* member1, FamilyMember* member2) {
    int count = 0;
    if (root == NULL) return NULL;

    // 如果当前节点是目标成员之一，直接返回当前节点
    if (root == member1 || root == member2) return root;

    // 递归查找子节点
    FamilyMember* p = root->child;
    FamilyMember* left = findClosestAncestorHelper(p, member1, member2);
    if (left) {
        count++;
    }

    FamilyMember* right;
    right = NULL;

    // 递归查找兄弟节点
    if (p) {
        p = p->sibling;
        while (p && count < 2) {
            right = findClosestAncestorHelper(p, member1, member2);
            if (right) {
                count++;
                if (!left) {
                    left = right; // 借 left 存储 right
                }
            }
            p = p->sibling;
        }

        // 如果在子树中找到两个目标成员，返回当前节点作为最近共同祖先
        if (count == 2) {
            return root;
        }

        // 返回找到的目标成员指针，如果只找到一个
        return left ? left : right;
    } else {
        // 返回找到的目标成员指针，如果只找到一个
        return left ? left : right;
    }
}

// 判断两个人是否是直系亲属
int isDirectRelation(FamilyMember* root, const char* name1, const char* name2) {
    FamilyMember* member1 = findFamilyMember(root, name1);
    FamilyMember* member2 = findFamilyMember(root, name2);
    if (!member1 || !member2) return 0;

    FamilyMember* temp = member1;
    while (temp != NULL) {
        if (temp == member2) return 1;
        temp = parent(root,temp);
    }

    temp = member2;
    while (temp != NULL) {
        if (temp == member1) return 1;
        temp = parent(root,temp);
    }

    return 0;
}

// 插入新人
void insertNewMember(FamilyMember* root, const char* parentName, const char* childName) {
    FamilyMember* parent = findFamilyMember(root, parentName);
    if (!parent) {
        printf("未找到父节点 %s\n", parentName);
        return;
    }
    FamilyMember* child = createFamilyMember(childName);
    insertChild(parent, child);
}

    // 递归删除成员及其后代
    void deleteMemberAndDescendants(FamilyMember* root, FamilyMember* member) {
    // 递归删除所有子节点
    FamilyMember* child = member->child;
    while (child != NULL) {
        FamilyMember* nextChild = child->sibling;
        deleteMemberAndDescendants(root, child);
        child = nextChild;
    }

    // 从树中删除成员
    if (parent(root, member)->child == member) {
        parent(root, member)->child = member->sibling;
    } else {
        FamilyMember* sibling = parent(root, member)->child;
        while (sibling->sibling != member) {
            sibling = sibling->sibling;
        }
        sibling->sibling = member->sibling;
    }

    // 释放内存
    free(member);
}


int main() {
    FamilyMember* root = buildFamilyTree("family.txt");
    int choice;
    char name[MAX_NAME_LEN], parentName[MAX_NAME_LEN], childName[MAX_NAME_LEN];
    int generation;

    while (1) {
        printf("\n菜单:\n");
        printf("1. 显示家谱\n");
        printf("2. 求出家族代数\n");
        printf("3. 统计指定辈份的人数\n");
        printf("4. 查找指定人，并显示其祖先和所有后代\n");
        printf("5. 求出两个人的最近祖先\n");
        printf("6. 判断两个人是否直系亲属\n");
        printf("7. 插入一个新人\n");
        printf("8. 删除某人，并将其后代一并删除\n");
        printf("9. 退出\n");
        printf("请输入选择: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("家谱:\n");
                printFamilyTree(root, 0);
                break;
            case 2:
                printf("家族代数: %d\n", calculateGenerations(root));
                break;
            case 3:
                printf("输入辈份: ");
                scanf("%d", &generation);
                while(generation > calculateGenerations(root)){
                    printf("对不起,输入的辈分过大！请重新输入或输入0进入菜单。\n");
                    printf("输入辈份: ");
                    scanf("%d",&generation);
                    if(!generation)break;
                }
                if(generation)printf("指定辈份的人数: %d\n", countGenerationMembers(root, generation, 1));
                break;
            case 4:
                printf("输入查找的成员名字: ");
                scanf("%s", name);
                findMemberAndDisplayAncestorsDescendants(root, name);
                break;
            case 5:
            {
                printf("输入第一个成员名字: ");
                scanf("%s", name);
                printf("输入第二个成员名字: ");
                scanf("%s", parentName); // 使用 parentName 临时存放第二个名字
                FamilyMember* ancestor = findClosestAncestor(root, name, parentName);
                if (ancestor) {
                    printf("最近的祖先是: %s\n", ancestor->name);
                } else {
                    printf("未找到共同祖先\n");
                }
            }
                break;
            case 6:
                printf("输入第一个成员名字: ");
                scanf("%s", name);
                printf("输入第二个成员名字: ");
                scanf("%s", parentName); // 使用 parentName 临时存放第二个名字
                if (isDirectRelation(root, name, parentName)) {
                    printf("是直系亲属\n");
                } else {
                    printf("不是直系亲属\n");
                }
                break;
            case 7:
                printf("输入父节点名字: ");
                scanf("%s", parentName);
                printf("输入新成员名字: ");
                scanf("%s", childName);
                insertNewMember(root, parentName, childName);
                printf("插入成功\n");
                break;
            case 8:
                printf("输入删除的成员名字: ");
                scanf("%s", name);
                deleteMember(root, name);
                printf("删除成功\n");
                break;
            case 9:
                return 0;
            default:
                printf("无效选择，请重新输入\n");
        }
    }

    return 0;
}
