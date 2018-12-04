//
// Created by xieji on 2018/12/3.
//
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <cstring>
#include <memory.h>

int GRID_SIZE;
int OBJ_LEVEL;
using namespace std;
vector<int *> ans;
int *grid = NULL;

int get_pos(const int &x, const int &y) {
    return x * GRID_SIZE + y;
}

void show_grid() {
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            printf("%c  ", grid[i * GRID_SIZE + j] == 1 ? 'A' : 'O');
//            printf("%d  ", grid[i * GRID_SIZE + j]);
        }
        printf("\n");
    }
}

bool test_grid(int pos) {
    int i = pos % GRID_SIZE;
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE) {
        grid[i] = 1;
    }
    i = (pos / GRID_SIZE) * GRID_SIZE;
    for (; i < (pos / GRID_SIZE) * GRID_SIZE + GRID_SIZE; i++) {
        grid[i] = 1;
    }
    i = pos - (pos % GRID_SIZE) * (GRID_SIZE + 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE + 1) {
        grid[i] = 1;
        if (i % GRID_SIZE == GRID_SIZE - 1)
            break;
    }
    i = pos - (GRID_SIZE - (pos % GRID_SIZE) - 1) * (GRID_SIZE - 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE - 1) {
        grid[i] = 1;
        if (i % GRID_SIZE == 0)
            break;
    }
    return true;
}


bool constraint_check() {
    int pos;    //chess_man position
    for (int j = 0; j < GRID_SIZE * GRID_SIZE; ++j) {
        if (grid[j] != 1)
            continue;
        pos = j;    //grid[pos] has a chess_man

        //check col
        int i = pos % GRID_SIZE;
        for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE) {
            if (grid[i] == 1 && i != pos) {
                return false;
            }
        }

        //check row
        i = (pos / GRID_SIZE) * GRID_SIZE;
        for (; i < (pos / GRID_SIZE) * GRID_SIZE + GRID_SIZE; i++) {
            if (grid[i] == 1 && i != pos) {
                return false;
            }
        }

        //check / direction
        i = pos - min(pos % GRID_SIZE, pos / GRID_SIZE) * (GRID_SIZE + 1);
        for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE + 1) {
            if (grid[i] == 1 && i != pos) {
                return false;
            }
            if (i % GRID_SIZE == GRID_SIZE - 1)
                break;
        }

        //check \ dirction
        i = pos - min((GRID_SIZE - (pos % GRID_SIZE) - 1), (pos / GRID_SIZE)) * (GRID_SIZE - 1);
        for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE - 1) {
            if (grid[i] == 1 && i != pos) {
                return false;
            }
            if (i % GRID_SIZE == 0)
                break;
        }
    }
    //all satisfy
    return true;
}

void mark_remove(int pos, int level) {
    //下棋后，更新棋盘上不可取的点，等价于更新其他棋子的值域
    //更新行上的值
    int i = pos % GRID_SIZE;
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE) {
        if (grid[i] == 0)
            grid[i] = level;
    }
    //更新列上的值
    i = (pos / GRID_SIZE) * GRID_SIZE;
    for (; i < (pos / GRID_SIZE) * GRID_SIZE + GRID_SIZE; i++) {
        if (grid[i] == 0)
            grid[i] = level;
    }
    //更新 / 方向上的值
    i = pos - min(pos % GRID_SIZE, pos / GRID_SIZE) * (GRID_SIZE + 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE + 1) {
        if (grid[i] == 0)
            grid[i] = level;
        if (i % GRID_SIZE == GRID_SIZE - 1)
            break;
    }
    //更新 \ 方向上的值
    i = pos - min((GRID_SIZE - (pos % GRID_SIZE) - 1), (pos / GRID_SIZE)) * (GRID_SIZE - 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE - 1) {
        if (grid[i] == 0)
            grid[i] = level;
        if (i % GRID_SIZE == 0)
            break;
    }
}

void unmark_remove(int pos, int level) {
    //反向操作，回溯后撤去棋子更新值域
    for (int i = 0; i < GRID_SIZE * GRID_SIZE; ++i) {
        if (grid[i] == level)
            grid[i] = 0;
    }
}

bool forward_check(int level) {
    bool res = false;
    for (int i = level * GRID_SIZE; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE) {
        res = false;//首先认为后续的某一行棋子发生了DWO
        for (int j = 0; j < GRID_SIZE; ++j) {
            if (grid[i + j] == 0) { //棋子有可以取值的点，值域不为空
                res = true; //更新res
                break;  //退出这一行棋子的循环
            }
        }
        if (!res)   //如果这一行的棋子找不到下棋点，发生了DWO
            return false;   //返回失败
    }
    return true;    //所有后续行的棋子值域非空，返回真
}


void fc_method(int level) {
    if (level == OBJ_LEVEL) {
        int *res = new int[GRID_SIZE * GRID_SIZE];
        memcpy(res, grid, sizeof(int) * GRID_SIZE * GRID_SIZE);
        ans.push_back(res);
        return;
    }   //成功找到解
    int pos = level * GRID_SIZE;
    for (; pos < (level + 1) * GRID_SIZE; ++pos) {  //搜索当前行
        if (grid[pos] == 0) {
            grid[pos] = 1;  //放置棋子
            mark_remove(pos, -level - 1);   //更新值域
            if (forward_check(level + 1)) { //如果不发生DWO
                fc_method(level + 1);   //搜下一层棋子
                unmark_remove(pos, -level - 1); //回溯，撤销值域修改
                grid[pos] = 0;  //删去棋子
            } else {
                unmark_remove(pos, -level - 1); //发生DWO，提前回溯
                grid[pos] = 0;
            }
        }
    }
}


void backtrack(int level) {
    if (level == OBJ_LEVEL) {   //搜到了目标层次，所有皇后已经在棋盘上
        int *res = new int[GRID_SIZE * GRID_SIZE];
        memcpy(res, grid, sizeof(int) * GRID_SIZE * GRID_SIZE);//复制棋盘状态到新的数组上
        ans.push_back(res);//将数组放入解的集合
        return;
    }
    int pos = level * GRID_SIZE;    // 皇后是一行一行放置的，根据当前搜索深度确定要尝试放置的行数。
    for (; pos < (level + 1) * GRID_SIZE; ++pos) {
        if (grid[pos] == 0) {   //改为之上没有棋子才可以进行放置
            grid[pos] = 1;  //放下棋子
            if (constraint_check()) {   //检查是否满足约束
                backtrack(level + 1);   //满足约束则进行下一层的放置
                grid[pos] = 0;      //回溯，撤销棋子的放置
            } else
                grid[pos] = 0;  //不满足约束，取消放置
        }
    }
}

int main(int argc, char *argv[]) {
    int input = atoi(argv[1]);
    GRID_SIZE = input;
    OBJ_LEVEL = input;
    grid = new int[GRID_SIZE * GRID_SIZE];
    backtrack(0);
//    grid[ge   t_pos(0, 3)] = 1;
//    fc_method(0);
    printf("sum: %d\n", int(ans.size()));
    int n = 8;
    return 0;
}
