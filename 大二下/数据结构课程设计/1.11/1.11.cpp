#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LEN 100
#define MAX_EVENTS 10
#define MAX_SCHOOLS 100
#define MAX_STUDENTS 1000
#define maxsize 2//输入项目排名最大名额 如8就是取前8名
// 学生信息结构定义
typedef struct {
    int ID;
    char name[MAX_NAME_LEN];
    char school[MAX_NAME_LEN];
    char event[MAX_NAME_LEN];
    int grade;
} Student;

// 学院信息结构定义
typedef struct {
    char name[MAX_NAME_LEN];
    int grade;
} School;

// 初始化学生列表
void initStudentList(Student students[], int *studentCount) {
    *studentCount = 0;
}

// 从文件读取学生报名数据
void readStudentData(const char *filename, Student students[], int *studentCount) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("无法打开文件");
        return;
    }

    while (fscanf(file, "%d %s %s %s", &students[*studentCount].ID, students[*studentCount].name,
                  students[*studentCount].school, students[*studentCount].event) != EOF) {
        students[*studentCount].grade = 0;
        (*studentCount)++;
    }

    fclose(file);
}

// 显示报名数据
void displayStudentData(Student students[], int studentCount) {
    for (int i = 0; i < studentCount; i++) {
        printf("%d %s %s %s\n", students[i].ID, students[i].name, students[i].school, students[i].event);
    }
}

// 根据学生ID和项目查找学生
int findStudent(Student students[], int studentCount, int ID, const char *event) {
    for (int i = 0; i < studentCount; i++) {
        if (students[i].ID == ID && strcmp(students[i].event, event) == 0) {
            return i;
        }
    }
    return -1;
}

// 获取参加某个项目的学生人数
int countStudentsInEvent(Student students[], int studentCount, const char *event) {
    int count = 0;
    for (int i = 0; i < studentCount; i++) {
        if (strcmp(students[i].event, event) == 0) {
            count++;
        }
    }
    return count;
}

// 输入每个项目前8名的成绩
void inputScores(Student students[], int studentCount, const char *events[], int eventCount) {
    int ID;
    for (int e = 0; e < eventCount; e++) {
        int participants = countStudentsInEvent(students, studentCount, events[e]);
        int maxInput = participants < maxsize ? participants : maxsize;
        for (int i = 1; i <= maxInput; i++) {
            int index;
            do {
                printf("%s 第%d名运动员编号：", events[e], i);
                scanf("%d", &ID);
                index = findStudent(students, studentCount, ID, events[e]);
                if (index == -1) {
                    printf("运动员 %d 未参加 %s\n", ID, events[e]);
                }
            } while (index == -1);
            students[index].grade = 9 - i;
        }
    }
}

// 查询项目成绩
void queryEventGrades(Student students[], int studentCount) {
    char event[MAX_NAME_LEN];
    printf("输入要查询的项目名称：");
    scanf("%s", event);
    printf("项目排名：\n");
    int participants = countStudentsInEvent(students, studentCount, event);
    int maxDisplay = participants < 8 ? participants : 8;
    for (int i = 1; i <= maxDisplay; i++) {
        for (int j = 0; j < studentCount; j++) {
            if (strcmp(students[j].event, event) == 0 && students[j].grade == 9 - i) {
                printf("%d %s\n", i, students[j].name);
            }
        }
    }
    printf("\n");
}

// 修改运动员成绩
void modifyStudentGrade(Student students[], int studentCount) {
    int ID;
    char name[MAX_NAME_LEN];
    char event[MAX_NAME_LEN];
    int newGrade;

    printf("输入运动员编号：");
    scanf("%d", &ID);
    printf("输入运动员姓名：");
    scanf("%s", name);
    printf("输入项目名称：");
    scanf("%s", event);

    int index = findStudent(students, studentCount, ID, event);
    if (index == -1 || strcmp(students[index].name, name) != 0) {
        printf("未找到匹配的运动员信息\n");
        return;
    }

    printf("输入新的成绩：");
    scanf("%d", &newGrade);
    students[index].grade = newGrade;
    printf("成绩已更新\n");
}

// 根据学院总分输出总成绩排名
void outputSchoolRank(Student students[], int studentCount, const char *schools[], int schoolCount) {
    School schoolRanks[MAX_SCHOOLS];

    for (int i = 0; i < schoolCount; i++) {
        strcpy(schoolRanks[i].name, schools[i]);
        schoolRanks[i].grade = 0;
    }

    for (int i = 0; i < studentCount; i++) {
        for (int j = 0; j < schoolCount; j++) {
            if (strcmp(students[i].school, schoolRanks[j].name) == 0) {
                schoolRanks[j].grade += students[i].grade;
            }
        }
    }

    // 排序
    for (int i = 0; i < schoolCount - 1; i++) {
        for (int j = i + 1; j < schoolCount; j++) {
            if (schoolRanks[i].grade < schoolRanks[j].grade) {
                School temp = schoolRanks[i];
                schoolRanks[i] = schoolRanks[j];
                schoolRanks[j] = temp;
            }
        }
    }

    // 输出排名
    for (int i = 0; i < schoolCount; i++) {
        printf("%d %s\n", schoolRanks[i].grade, schoolRanks[i].name);
    }
    printf("\n");
}

// 保存数据到文件
void saveDataToFile(const char *filename, Student students[], int studentCount) {
    FILE *file = fopen(filename, "w");
    if (!file) {
        perror("无法打开文件");
        return;
    }

    for (int i = 0; i < studentCount; i++) {
        fprintf(file, "%d %s %s %s %d\n", students[i].ID, students[i].name, students[i].school, students[i].event, students[i].grade);
    }

    fclose(file);
}

int main() {
    Student students[MAX_STUDENTS];
    int studentCount;

    const char *events[MAX_EVENTS] = {"男子100米", "女子跳远", "男子200米", "女子铅球", "男子400米", "女子标枪", "男子跳高", "女子800米", "男子1500米"};
    const char *schools[MAX_SCHOOLS] = {"信息工程学院", "理学院", "法学院", "历史学院", "经济学院", "管理学院", "工程学院", "医学院", "外国语学院", "艺术学院"};

    initStudentList(students, &studentCount);
    readStudentData("text1.txt", students, &studentCount);

    int choice;
    while (1) {
        printf("\n菜单:\n");
        printf("1. 显示从文件读取的内容\n");
        printf("2. 显示报名数据\n");
        printf("3. 输入运动员的得分\n");
        printf("4. 查询成绩\n");
        printf("5. 修改成绩\n");
        printf("6. 输出成绩排名\n");
        printf("7. 保存数据到文件\n");
        printf("8. 退出\n");
        printf("请输入选择: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("从文件读取的内容：\n");
//                readStudentData("text1.txt", students, &studentCount);
                displayStudentData(students, studentCount);
                break;
            case 2:
                printf("报名数据：\n");
                displayStudentData(students, studentCount);
                break;
            case 3:
                inputScores(students, studentCount, events, 9);
                break;
            case 4:
                queryEventGrades(students, studentCount);
                break;
            case 5:
                modifyStudentGrade(students, studentCount);
                break;
            case 6:
                outputSchoolRank(students, studentCount, schools, 10);
                break;
            case 7:
                saveDataToFile("text2.txt", students, studentCount);
                break;
            case 8:
                return 0;
            default:
                printf("无效选择，请重新输入\n");
        }
    }

    return 0;
}
