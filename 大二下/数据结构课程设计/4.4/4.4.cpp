#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUILDINGS 100
#define INF 0x3f

// 定义建筑物结构
typedef struct {
    char name[50];
    char facilities[200];
} Building;

// 定义校园地图
typedef struct {
    Building buildings[MAX_BUILDINGS];
    int edges[MAX_BUILDINGS][MAX_BUILDINGS];
    int buildingCount;
} CampusMap;

// 初始化校园地图
void initCampusMap(CampusMap *map) {
    // 初始化校园地图中的建筑数量为0
    map->buildingCount = 0;

    // 遍历每个建筑的距离矩阵
    for (int i = 0; i < MAX_BUILDINGS; i++) {
        for (int j = 0; j < MAX_BUILDINGS; j++) {
            if (i == j) {
                // 同一个建筑到自己的距离设置为0
                map->edges[i][j] = 0;
            } else {
                // 不同建筑之间的距离初始设置为无穷大（不可达）
                map->edges[i][j] = INF;
            }
        }
    }
}

// 从文件读取数据
void loadBuildings(CampusMap *map, const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("无法打开文件 %s\n", filename);
        return;
    }

    char line[256];
    while (fgets(line, sizeof(line), file) && map->buildingCount < MAX_BUILDINGS) {
        line[strcspn(line, "\n")] = 0; // 去掉换行符
//		printf("%s\n",line);
        char *name = strtok(line, "（");

        char *facilities = strtok(NULL,"（");

//		printf("%s\n",name);
//		printf("%s\n",facilities);
        strcpy(map->buildings[map->buildingCount].name, name);
        strcpy(map->buildings[map->buildingCount].facilities, facilities);
        map->buildingCount++;
    }

    fclose(file);
}

// 添加路径及其权值
void addPath(CampusMap *map, int from, int to, int weight) {
    if (from < 0 || from >= map->buildingCount || to < 0 || to >= map->buildingCount) {
        printf("无效的建筑物索引\n");
        return;
    }
    map->edges[from][to] = weight;
    map->edges[to][from] = weight; // 无向图
}

// 显示校园地图
void displayCampusMap(CampusMap *map) {
    for (int i = 0; i < map->buildingCount; i++) {
        printf("%s（%s）\n", map->buildings[i].name, map->buildings[i].facilities);
    }
}

// 查找建筑物索引
int findBuildingIndex(CampusMap *map, const char *name) {
    for (int i = 0; i < map->buildingCount; i++) {
        if (strcmp(map->buildings[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

// 查找并显示路径
void findShortestPath(CampusMap *map, int start, int end) {
    int dist[MAX_BUILDINGS], prev[MAX_BUILDINGS], selected[MAX_BUILDINGS] = {0};
    
    // 初始化 dist 和 prev 数组
    for (int i = 0; i < map->buildingCount; i++) {
        dist[i] = INF; // 设置初始距离为无穷大
        prev[i] = -1;  // 设置前驱节点为 -1
    }
    dist[start] = 0; // 起始建筑的距离为 0

    // Dijkstra 算法的主循环
    for (int i = 0; i < map->buildingCount; i++) {
        int minDist = INF, u = -1;
        // 找到距离起始建筑最近的未访问节点
        for (int j = 0; j < map->buildingCount; j++) {
            if (!selected[j] && dist[j] < minDist) {
                minDist = dist[j];
                u = j;
            }
        }

        // 如果未找到有效的节点，跳出循环
        if (u == -1) break;
        selected[u] = 1; // 标记节点 u 为已访问

        // 更新与节点 u 相邻的节点的距离
        for (int v = 0; v < map->buildingCount; v++) {
            if (!selected[v] && map->edges[u][v] != INF) {
                int newDist = dist[u] + map->edges[u][v];
                if (newDist < dist[v]) {
                    dist[v] = newDist;
                    prev[v] = u;
                }
            }
        }
    }

    // 检查目标建筑是否可达
    if (dist[end] == INF) {
        printf("无法到达 %s\n", map->buildings[end].name);
        return;
    }

    // 打印最短路径
    printf("从 %s 到 %s 的最短路径：\n", map->buildings[start].name, map->buildings[end].name);
    int path[MAX_BUILDINGS], pathLength = 0;
    for (int v = end; v != -1; v = prev[v]) {
        path[pathLength++] = v;
    }
    for (int i = pathLength - 1; i >= 0; i--) {
        printf("%s", map->buildings[path[i]].name);
        if (i > 0) printf(" -> ");
    }
    printf("\n总距离：%d\n", dist[end]);
}


// 插入新的建筑物
void insertBuilding(CampusMap *map, const char *name, const char *facilities) {
    if (map->buildingCount >= MAX_BUILDINGS) {
        printf("建筑物已达最大数量，无法插入\n");
        return;
    }
    strcpy(map->buildings[map->buildingCount].name, name);
    strcpy(map->buildings[map->buildingCount].facilities, facilities);
    map->buildingCount++;
    printf("已插入建筑物 %s\n", name);
}

// 删除指定建筑物
void deleteBuilding(CampusMap *map, const char *name) {
    int index = findBuildingIndex(map, name);
    if (index == -1) {
        printf("未找到建筑物 %s\n", name);
        return;
    }
    for (int i = index; i < map->buildingCount - 1; i++) {
        map->buildings[i] = map->buildings[i + 1];
        for (int j = 0; j < map->buildingCount; j++) {
            map->edges[i][j] = map->edges[i + 1][j];
            map->edges[j][i] = map->edges[j][i + 1];
        }
    }
    map->buildingCount--;
    printf("已删除建筑物 %s\n", name);
}

// 修改建筑物信息
void modifyBuilding(CampusMap *map, const char *name, const char *newFacilities) {
    int index = findBuildingIndex(map, name);
    if (index == -1) {
        printf("未找到建筑物 %s\n", name);
        return;
    }
    strcpy(map->buildings[index].facilities, newFacilities);
    printf("已修改建筑物 %s 的设施信息\n", name);
}

// 导游路线
void tourRoute(CampusMap *map) {
    printf("导游路线：\n");
    for (int i = 0; i < map->buildingCount; i++) {
        printf("%s -> ", map->buildings[i].name);
    }
    printf("结束\n");
}

// 菜单
void menu(CampusMap *map) {
    int choice;
    char name[50], facilities[200];
    int from, to, weight;

    while (1) {
        printf("\n菜单:\n");
        printf("1. 显示校园地图\n");
        printf("2. 查找建筑物\n");
        printf("3. 插入新的建筑物\n");
        printf("4. 删除指定建筑物\n");
        printf("5. 修改建筑物信息\n");
        printf("6. 添加路径及其权值\n");
        printf("7. 查找最短路径\n");
        printf("8. 显示导游路线\n");
        printf("9. 退出\n");
        printf("请输入选择: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                displayCampusMap(map);
                break;
            case 2:
            {
                printf("请输入建筑物名称: ");
                scanf("%s", name);
                int index = findBuildingIndex(map, name);
                if (index != -1) {
                    printf("%s（%s）\n", map->buildings[index].name, map->buildings[index].facilities);
                } else {
                    printf("未找到建筑物 %s\n", name);
                }
            }
                break;
            case 3:
            {
                printf("请输入新的建筑物名称: ");
                scanf("%s", name);
                printf("请输入建筑物设施信息: ");
                scanf("%s", facilities);
                insertBuilding(map, name, facilities);

            }
                break;
            case 4:
                printf("请输入要删除的建筑物名称: ");
                scanf("%s", name);
                deleteBuilding(map, name);
                break;
            case 5:
                printf("请输入建筑物名称: ");
                scanf("%s", name);
                printf("请输入新的设施信息: ");
                scanf("%s", facilities);
                modifyBuilding(map, name, facilities);
                break;
            case 6:
                printf("请输入起点建筑物索引（0-%d）: ", map->buildingCount - 1);
                scanf("%d", &from);
                printf("请输入终点建筑物索引（0-%d）: ", map->buildingCount - 1);
                scanf("%d", &to);
                printf("请输入路径权值（距离）: ");
                scanf("%d", &weight);
                addPath(map, from, to, weight);
                break;
            case 7:
                printf("请输入起点建筑物名称: ");
                scanf("%s", name);
                from = findBuildingIndex(map, name);
                if (from == -1) {
                    printf("未找到建筑物 %s\n", name);
                    break;
                }
                printf("请输入终点建筑物名称: ");
                scanf("%s", name);
                to = findBuildingIndex(map, name);
                if (to == -1) {
                    printf("未找到建筑物 %s\n", name);
                    break;
                }
                findShortestPath(map, from, to);
                break;
            case 8:
                tourRoute(map);
                break;
            case 9:
                return;
            default:
                printf("无效选择，请重新输入\n");
        }
    }
}

int main() {
    CampusMap map;
    initCampusMap(&map);
    loadBuildings(&map, "buildings.txt");
    menu(&map);
    return 0;
}
