#include <stdio.h>
#include <string.h>

struct student {  //学生信息结构体
    int id;  //学号
    char name[20];  //姓名
    char gender[10];  //性别
    int score_chinese;  //语文成绩
    int score_math;  //数学成绩
    int score_english;  //英语成绩
};

const int MAX_NUM=100;  //学生数量上限
struct student students[MAX_NUM];  //存储所有学生的信息
int num_students=5;  //当前学生数量

void show_student(struct student s){  //显示一个学生的信息
    printf("%s\t学号:%d,性别:%s,语文:%d,数学:%d,英语:%d\n",s.name,s.id,s.gender,s.score_chinese,s.score_math,s.score_english);
}

void show_all_student_info(){  //显示所有同学的信息
    for(int i=0;i<num_students;i++){
        show_student(students[i]);
    }
}

void search_student_info(char name[]){  //查找指定姓名的信息
    for(int i=0;i<num_students;i++){
        if(strstr(students[i].name,name)!=NULL){  //模糊查找
            show_student(students[i]);
        }
    }
}

void modify_student_info(char name[]){  //修改指定姓名的信息
    for(int i=0;i<num_students;i++) {
        if (strcmp(students[i].name,name)==0){
            printf("当前该同学的信息为：\n");
            show_student(students[i]);
            printf("请输入修改后的信息（学号、姓名、性别、语文成绩、数学成绩、英语成绩，用空格分隔）:\n");
            struct student s;
            scanf("%d %s %s %d %d %d",&s.id,s.name,s.gender,&s.score_chinese,&s.score_math,&s.score_english);
            strcpy(students[i].name,s.name);
            students[i].id=s.id;
            strcpy(students[i].gender,s.gender);
            students[i].score_chinese=s.score_chinese;
            students[i].score_math=s.score_math;
            students[i].score_english=s.score_english;
            printf("修改成功！\n");
            return;
        }
    }
    printf("查无此人！\n");
}

void show_failed_student_info(){  //显示有不及格同学的信息
    for(int i=0;i<num_students;i++){
        if (students[i].score_chinese<60||students[i].score_math<60||students[i].score_english<60){
            show_student(students[i]);
        }
    }
}

void sort_by_course(int course){  //按指定课程排序输出
    struct student tmp;
    for(int i=0;i<num_students-1;i++){
        for(int j=i+1;j<num_students;j++){
            switch(course){
                case 1:  //语文
                    if(students[i].score_chinese<students[j].score_chinese){
                        tmp=students[i];
                        students[i]=students[j];
                        students[j]=tmp;
                    }
                    break;
                case 2:  //数学
                    if(students[i].score_math<students[j].score_math){
                        tmp=students[i];
                        students[i]=students[j];
                        students[j]=tmp;
                    }
                    break;
                case 3:  //英语
                    if(students[i].score_english<students[j].score_english){
                        tmp=students[i];
                        students[i]=students[j];
                        students[j]=tmp;
                    }
                    break;
                default:
                    break;
            }
        }
    }
    printf("按照第%d门课程排序后的结果：\n",course);
    show_all_student_info();
}

void add_new_student(){  //增加一个新同学
    if(num_students>=MAX_NUM){
        printf("增加失败，学生数量已达上限！\n");
        return;
    }
    printf("请输入新同学的信息(学号、姓名、性别、语文成绩、数学成绩、英语成绩(用空格分隔)):\n");
    struct student s;
    scanf("%d %s %s %d %d %d",&s.id,s.name,s.gender,&s.score_chinese,&s.score_math,&s.score_english);
    strcpy(students[num_students].name,s.name);
    students[num_students].id=s.id;
    strcpy(students[num_students].gender,s.gender);
    students[num_students].score_chinese=s.score_chinese;
    students[num_students].score_math=s.score_math;
    students[num_students].score_english=s.score_english;
    num_students++;
    printf("添加成功！\n");
}

void delete_student_info(char name[]){  //删除指定姓名的信息
    for(int i=0;i<num_students;i++){
        if(strcmp(students[i].name,name)==0){
            for(int j=i;j<num_students-1;j++){
                students[j]=students[j+1];
            }
            num_students--;
            printf("删除成功！\n");
            return;
        }
    }
    printf("查无此人！\n");
}

void Menu()
{
	printf("|----------------------------------------------|\n");
	printf("|----------------学生管理系统------------------|\n");
	printf("|----------------------------------------------|\n");
	printf("|***        1.显示所有同学的信息            ***|\n");
	printf("|***        2.查找指定姓名的信息            ***|\n");
	printf("|***        3.修改指定姓名的信息            ***|\n");
	printf("|***        4.显示有不及格同学的信息        ***|\n");
	printf("|***        5.按指定课程排序输出            ***|\n");
	printf("|***        6.增加一个新同学                ***|\n");
	printf("|***        7.删除指定姓名的信息            ***|\n");
	printf("|***        0.退出                          ***|\n");
	printf("|----------------------------------------------|\n");
	printf("|----------------------------------------------|\n");
	printf("输入您要执行的操作对应数字：");
}

int main()
{
    //初始化学生信息
    strcpy(students[0].name,"zhang");
    students[0].id=1;
    strcpy(students[0].gender,"女");
    students[0].score_chinese=97;
    students[0].score_math=45;
    students[0].score_english=95;

    strcpy(students[1].name,"liu");
    students[1].id=2;
    strcpy(students[1].gender,"男");
    students[1].score_chinese=86;
    students[1].score_math=100;
    students[1].score_english=90;

    strcpy(students[2].name,"wang");
    students[2].id=3;
    strcpy(students[2].gender, "男");
    students[2].score_chinese=68;
    students[2].score_math=77;
    students[2].score_english=88;

    strcpy(students[3].name,"xie");
    students[3].id=4;
    strcpy(students[3].gender,"男");
    students[3].score_chinese=50;
    students[3].score_math=98;
    students[3].score_english=100;

    strcpy(students[4].name,"xu");
    students[4].id=5;
    strcpy(students[4].gender,"女");
    students[4].score_chinese=90;
    students[4].score_math=98;
    students[4].score_english=68;

    int choice=-1;
    while(choice!=0){
        Menu();
        scanf("%d",&choice);
        switch (choice){
            case 0:
                printf("谢谢使用学生信息管理系统！\n");
                break;
            case 1:
            	printf("以下为所有学生信息：\n");
                show_all_student_info();
                printf("\n");
                break;
            case 2:
                printf("请输入要查找的姓名：");
                char name[20];
                scanf("%s", name);
                search_student_info(name);
                printf("\n");
                break;
            case 3:
            	printf("请输入要修改信息的同学的姓名：");
                char name2[20];
                scanf("%s",name2);
				modify_student_info(name2);
				printf("\n");
				break;
            case 4:
                show_failed_student_info();
                printf("\n");
                break;
            case 5:
            	printf("请输入要排序的课程（1.语文 2.数学 3.英语）：");
                int course;
                scanf("%d", &course);
                sort_by_course(course);
                printf("\n");
                break;
            case 6:
            	add_new_student();
                printf("\n");
                break;
            case 7:
            	printf("请输入要删除信息的同学的姓名：");
                char name3[20];
                scanf("%s",name3);
                delete_student_info(name3);
                printf("\n");
                break;
            default:
                printf("您的输入有误，请重新输入！\n");
                break;
        }
    }
    return 0;
}