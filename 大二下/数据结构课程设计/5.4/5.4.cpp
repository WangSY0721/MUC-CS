#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <climits>

using namespace std;

// 定义红黑树节点的颜色
enum Color { RED, BLACK };

// 红黑树节点结构
struct Node {
    int id;            // 学号
    string name;       // 姓名
    string major;      // 专业
    bool color;        // 颜色
    Node *left, *right, *parent;  // 左右子节点和父节点指针

    // 构造函数
    Node(int id, string name, string major)
            : id(id), name(name), major(major), color(RED), left(NULL), right(NULL), parent(NULL) {}
};

// 红黑树类
class RedBlackTree {
private:
    Node* root;  // 根节点
    Node* TNULL; // NULL节点

    // 初始化NULL节点
    void initializeNULLNode(Node* node, Node* parent) {
    	node->id = 0;          // 将节点ID设置为0，表示这是一个特殊的空节点
    	node->name = "";       // 将节点名称设置为空字符串
   	node->major = "";      // 将节点专业设置为空字符串
   	node->color = BLACK;   // 将节点颜色设置为黑色，NIL节点必须是黑色
    	node->left = NULL;     // 将节点的左子节点设置为NULL
    	node->right = NULL;    // 将节点的右子节点设置为NULL
    	node->parent = parent; // 将节点的父节点设置为传入的父节点
    }


    // 前序遍历辅助函数
    void preOrderHelper(Node* node) {
        if (node != TNULL) {
            cout << node->id << " " << node->name << " " << node->major << " ";
            preOrderHelper(node->left);
            preOrderHelper(node->right);
        }
    }

    // 中序遍历辅助函数
    void inOrderHelper(Node* node) {
        if (node != TNULL) {
            inOrderHelper(node->left);
            cout << node->id << " " << node->name << " " << node->major << " ";
            inOrderHelper(node->right);
        }
    }

    // 后序遍历辅助函数
    void postOrderHelper(Node* node) {
        if (node != TNULL) {
            postOrderHelper(node->left);
            postOrderHelper(node->right);
            cout << node->id << " " << node->name << " " << node->major << " ";
        }
    }

    // 查找树中节点的辅助函数，返回比较次数
    Node* searchTreeHelper(Node* node, int key, int &compCount) {
        if (node == TNULL || key == node->id) {
            return node;
        }

        compCount++;
        if (key < node->id) {
            return searchTreeHelper(node->left, key, compCount);
        }
        return searchTreeHelper(node->right, key, compCount);
    }

    // 修复删除节点后的红黑树性质
    void fixDelete(Node* x) {
        Node* s;
        while (x != root && x->color == BLACK) {
            if (x == x->parent->left) {
                s = x->parent->right;
                if (s->color == RED) {
                    s->color = BLACK;
                    x->parent->color = RED;
                    leftRotate(x->parent);
                    s = x->parent->right;
                }

                if (s->left->color == BLACK && s->right->color == BLACK) {
                    s->color = RED;
                    x = x->parent;
                } else {
                    if (s->right->color == BLACK) {
                        s->left->color = BLACK;
                        s->color = RED;
                        rightRotate(s);
                        s = x->parent->right;
                    }

                    s->color = x->parent->color;
                    x->parent->color = BLACK;
                    s->right->color = BLACK;
                    leftRotate(x->parent);
                    x = root;
                }
            } else {
                s = x->parent->left;
                if (s->color == RED) {
                    s->color = BLACK;
                    x->parent->color = RED;
                    rightRotate(x->parent);
                    s = x->parent->left;
                }

                if (s->right->color == BLACK && s->left->color == BLACK) {
                    s->color = RED;
                    x = x->parent;
                } else {
                    if (s->left->color == BLACK) {
                        s->right->color = BLACK;
                        s->color = RED;
                        leftRotate(s);
                        s = x->parent->left;
                    }

                    s->color = x->parent->color;
                    x->parent->color = BLACK;
                    s->left->color = BLACK;
                    rightRotate(x->parent);
                    x = root;
                }
            }
        }
        x->color = BLACK;
    }

   // 辅助函数用于红黑树节点替换
void rbTransplant(Node* u, Node* v) {
    if (u->parent == NULL) {
        // 如果 u 是根节点，将根节点设置为 v
        root = v;
    } else if (u == u->parent->left) {
        // 如果 u 是其父节点的左子节点，将父节点的左子节点设置为 v
        u->parent->left = v;
    } else {
        // 如果 u 是其父节点的右子节点，将父节点的右子节点设置为 v
        u->parent->right = v;
    }
    // 将 v 的父节点设置为 u 的父节点
    v->parent = u->parent;
}

    // 删除节点的辅助函数
void deleteNodeHelper(Node* node, int key) {
    Node* z = TNULL;  // 用于指向要删除的节点
    Node* x, *y;      // 辅助指针
    // 查找键值为 key 的节点
    while (node != TNULL){
        if (node->id == key) {
            z = node;
        }

        if (node->id <= key) {
            node = node->right;
        } else {
            node = node->left;
        }
    }

    // 如果未找到 key，输出提示信息并返回
    if (z == TNULL) {
        cout << "Key not found in the tree" << endl;
        return;
    }

    y = z;  // 设置 y 为要删除的节点
    int yOriginalColor = y->color;  // 保存 y 的原始颜色

    // 如果 z 没有左子节点，用右子节点替换 z
    if (z->left == TNULL) {
        x = z->right;
        rbTransplant(z, z->right);
    // 如果 z 没有右子节点，用左子节点替换 z
    } else if (z->right == TNULL) {
        x = z->left;
        rbTransplant(z, z->left);
    // 如果 z 有两个子节点
    } else {
        y = minimum(z->right);  // 找到 z 的右子树中的最小节点
        yOriginalColor = y->color;  // 更新 y 的颜色
        x = y->right;  // 设置 x 为 y 的右子节点
        if (y->parent == z) {
            x->parent = y;
        } else {
            rbTransplant(y, y->right);
            y->right = z->right;
            y->right->parent = y;
        }

        rbTransplant(z, y);
        y->left = z->left;
        y->left->parent = y;
        y->color = z->color;
    }

    // 删除 z 节点
    delete z;

    // 如果 y 的原始颜色是黑色，修复红黑树的性质
    if (yOriginalColor == BLACK){
        fixDelete(x);
    }
}

    // 修复插入节点后的红黑树性质
void fixInsert(Node* k) {
    Node* u;
    // 当父节点是红色时，进入循环
    while (k->parent->color == RED) {
        // 父节点是右子节点的情况
        if (k->parent == k->parent->parent->right) {
            u = k->parent->parent->left; // 叔父节点
            // 叔父节点是红色的情况
            if (u->color == RED) {
                u->color = BLACK;
                k->parent->color = BLACK;
                k->parent->parent->color = RED;
                k = k->parent->parent;
            } else {
                // 叔父节点是黑色的情况
                if (k == k->parent->left) {
                    k = k->parent;
                    rightRotate(k);
                }
                k->parent->color = BLACK;
                k->parent->parent->color = RED;
                leftRotate(k->parent->parent);
            }
        // 父节点是左子节点的情况
        } else {
            u = k->parent->parent->right; // 叔父节点
            // 叔父节点是红色的情况
            if (u->color == RED) {
                u->color = BLACK;
                k->parent->color = BLACK;
                k->parent->parent->color = RED;
                k = k->parent->parent;
            } else {
                // 叔父节点是黑色的情况
                if (k == k->parent->right) {
                    k = k->parent;
                    leftRotate(k);
                }
                k->parent->color = BLACK;
                k->parent->parent->color = RED;
                rightRotate(k->parent->parent);
            }
        }
        // 检查是否达到根节点
        if (k == root) {
            break;
        }
    }
    // 将根节点颜色设置为黑色
    root->color = BLACK;
}


    // 打印红黑树的辅助函数
    void printHelper(Node* root, string indent, bool last) {
        if (root != TNULL) {
            cout << indent;
            if (last) {
                cout << "R----";
                indent += "   ";
            } else {
                cout << "L----";
                indent += "|  ";
            }

            string sColor = root->color?"RED":"BLACK";
            cout << root->id << "(" << sColor << ")" << endl;
            printHelper(root->left, indent, false);
            printHelper(root->right, indent, true);
        }
    }

public:
    // 构造函数
    RedBlackTree() {
        TNULL = new Node(0, "", "");
        initializeNULLNode(TNULL, NULL);
        root = TNULL;
    }

    // 前序遍历
    void preorder() {
        preOrderHelper(this->root);
    }

    // 中序遍历
    void inorder() {
        inOrderHelper(this->root);
    }

    // 后序遍历
    void postorder() {
        postOrderHelper(this->root);
    }

    // 查找树中的节点
    Node* searchTree(int k, int &compCount) {
        return searchTreeHelper(this->root, k, compCount);
    }

    // 查找最小值节点
    Node* minimum(Node* node) {
        while (node->left != TNULL) {
            node = node->left;
        }
        return node;
    }

    // 查找最大值节点
    Node* maximum(Node* node) {
        while (node->right != TNULL) {
            node = node->right;
        }
        return node;
    }

    // 查找节点的后继
    Node* successor(Node* x) {
        if (x->right != TNULL) {
            return minimum(x->right);
        }

        Node* y = x->parent;
        while (y != TNULL && x == y->right) {
            x = y;
            y = y->parent;
        }
        return y;
    }

    // 查找节点的前驱
    Node* predecessor(Node* x) {
        if (x->left != TNULL) {
            return maximum(x->left);
        }

        Node* y = x->parent;
        while (y != TNULL && x == y->left) {
            x = y;
            y = y->parent;
        }

        return y;
    }

    // 左旋转
    void leftRotate(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        if (y->left != TNULL) {
            y->left->parent = x;
        }
        y->parent = x->parent;
        if (x->parent == NULL) {
            this->root = y;
        } else if (x == x->parent->left) {
            x->parent->left = y;
        } else {
            x->parent->right = y;
        }
        y->left = x;
        x->parent = y;
    }

    // 右旋转
    void rightRotate(Node* x) {
        Node* y = x->left;
        x->left = y->right;
        if (y->right != TNULL) {
            y->right->parent = x;
        }
        y->parent = x->parent;
        if (x->parent == NULL) {
            this->root = y;
        } else if (x == x->parent->right) {
            x->parent->right = y;
        } else {
            x->parent->left = y;
        }
        y->right = x;
        x->parent = y;
    }

    // 插入节点
    void insert(int id, string name, string major) {
        Node* node = new Node(id, name, major);
        node->parent = NULL;
        node->id = id;
        node->name = name;
        node->major = major;
        node->left = TNULL;
        node->right = TNULL;
        node->color = RED;

        Node* y = NULL;
        Node* x = this->root;

        while (x != TNULL) {
            y = x;
            if (node->id < x->id) {
                x = x->left;
            } else {
                x = x->right;
            }
        }

        node->parent = y;
        if (y == NULL) {
            root = node;
        } else if (node->id < y->id) {
            y->left = node;
        } else {
            y->right = node;
        }

        if (node->parent == NULL){
            node->color = BLACK;
            return;
        }

        if (node->parent->parent == NULL) {
            return;
        }

        fixInsert(node);
    }

    // 获取红黑树根节点
    Node* getRoot() {
        return this->root;
    }

    // 删除节点
    void deleteNode(int data) {
        deleteNodeHelper(this->root, data);
    }

    // 打印红黑树
    void printTree() {
        if (root) {
            printHelper(this->root, "", true);
        }
    }

    // 中序遍历显示红黑树
    void displayInOrder() {
        displayInOrderHelper(this->root);
    }

    // 中序遍历辅助函数
    void displayInOrderHelper(Node* root) {
        if (root != TNULL) {
            displayInOrderHelper(root->right);
            cout << root->id << " " << root->name << " " << root->major << endl;
            displayInOrderHelper(root->left);
        }
    }

    // 计算红黑树中节点的平均比较次数
    int calculateAverageComparison(Node* node, int depth, int &totalDepth, int &nodeCount) {
        if (node == TNULL) {
            return 0;
        }

        nodeCount++;
        totalDepth += depth;

        calculateAverageComparison(node->left, depth + 1, totalDepth, nodeCount);
        calculateAverageComparison(node->right, depth + 1, totalDepth, nodeCount);
    }

    // 获取红黑树中节点的平均比较长度
    double getAverageComparisonLength(bool searchSuccess) {
        int totalDepth = 0;
        int nodeCount = 0;

        calculateAverageComparison(this->root, 0, totalDepth, nodeCount);

        if (nodeCount == 0) {
            return 0;
        }

        if (searchSuccess) {
            return static_cast<double>(totalDepth) / nodeCount;
        } else {
            return static_cast<double>(totalDepth + nodeCount) / (nodeCount + 1);
        }
    }
};

// 从文件读取数据并插入红黑树
void readFromFile(const char* filename, RedBlackTree &tree) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "无法打开文件 " << filename << endl;
        return;
    }

    int id;
    string name, major;
    while (file >> id >> name >> major) {
        tree.insert(id, name, major);
    }

    file.close();
}

int main() {
    RedBlackTree tree;
    readFromFile("students.txt", tree); 

    int choice;
    int id;
    string name, major;
    int comparisons;

    while (true) {
        cout << "\n菜单:\n";
        cout << "1. 输入查找表长度n，显示生成的n个随机数\n";
        cout << "2. 按学号递减次序输出\n";
        cout << "3. 显示平均查找长度\n";
        cout << "4. 输入查找数据，显示依次比较的数据、比较次数以及查找结果\n";
        cout << "5. 输入插入数据，显示插入结果，以及平均查找长度\n";
        cout << "6. 输入删除数据，显示删除结果，以及平均查找长度\n";
        cout << "7. 退出\n";
        cout << "请输入选择: ";
        cin >> choice;

        switch (choice) {
            case 1:
                int n;
                cout << "输入查找表长度n: ";
                cin >> n;
                srand(time(0));
                for (int i = 0; i < n; i++) {
                    cout << rand() % 100 + 1 << " ";
                }
                cout << endl;
                break;
            case 2:
                tree.displayInOrder();
                break;
            case 3:
                cout << "成功查找的平均比较长度: " << tree.getAverageComparisonLength(true) << endl;
                cout << "失败查找的平均比较长度: " << tree.getAverageComparisonLength(false) << endl;
                break;
            case 4:
                cout << "输入查找数据的学号: ";
                cin >> id;
                comparisons = 0;
                if (tree.searchTree(id, comparisons) != NULL) {
                    cout << "查找成功, 比较次数: " << comparisons << endl;
                } else {
                    cout << "查找失败, 比较次数: " << comparisons << endl;
                }
                break;
            case 5:
                cout << "输入插入数据 (学号 姓名 专业): ";
                cin >> id >> name >> major;
                tree.insert(id, name, major);
                cout << "插入成功, 成功查找的平均比较长度: " << tree.getAverageComparisonLength(true) << endl;
                break;
            case 6:
                cout << "输入删除数据的学号: ";
                cin >> id;
                tree.deleteNode(id);
                cout << "删除成功, 成功查找的平均比较长度: " << tree.getAverageComparisonLength(true) << endl;
                break;
            case 7:
                return 0;
            default:
                cout << "无效选择，请重新输入\n";
        }
    }

    return 0;
}
