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


bool constraint_check(int pos) {
    int i = pos % GRID_SIZE;
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE) {
        if (grid[i] == 1 && i != pos) {
            return false;
        }
    }
    i = (pos / GRID_SIZE) * GRID_SIZE;
    for (; i < (pos / GRID_SIZE) * GRID_SIZE + GRID_SIZE; i++) {
        if (grid[i] == 1 && i != pos) {
            return false;
        }
    }
    i = pos - (pos % GRID_SIZE) * (GRID_SIZE + 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE + 1) {
        if (grid[i] == 1 && i != pos) {
            return false;
        }
        if (i % GRID_SIZE == GRID_SIZE - 1)
            break;
    }
    i = pos - (GRID_SIZE - (pos % GRID_SIZE) - 1) * (GRID_SIZE - 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE - 1) {
        if (grid[i] == 1 && i != pos) {
            return false;
        }
        if (i % GRID_SIZE == 0)
            break;
    }
    return true;
}

void mark_remove(int pos, int level) {
    int i = pos % GRID_SIZE;
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE) {
        if (grid[i] == 0)
            grid[i] = level;
    }
    i = (pos / GRID_SIZE) * GRID_SIZE;
    for (; i < (pos / GRID_SIZE) * GRID_SIZE + GRID_SIZE; i++) {
        if (grid[i] == 0)
            grid[i] = level;
    }
    i = pos - (pos % GRID_SIZE) * (GRID_SIZE + 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE + 1) {
        if (i < 0) {
            continue;
        }
        if (grid[i] == 0)
            grid[i] = level;
        if (i % GRID_SIZE == GRID_SIZE - 1)
            break;
    }
    i = pos - (GRID_SIZE - (pos % GRID_SIZE) - 1) * (GRID_SIZE - 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE - 1) {
        if (i < 0) {
            continue;
        }
        if (grid[i] == 0)
            grid[i] = level;
        if (i % GRID_SIZE == 0)
            break;
    }
}

void unmark_remove(int pos, int level) {
    int i = pos % GRID_SIZE;
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE) {
        if (grid[i] == level)
            grid[i] = 0;
    }
    i = (pos / GRID_SIZE) * GRID_SIZE;
    for (; i < (pos / GRID_SIZE) * GRID_SIZE + GRID_SIZE; i++) {
        if (grid[i] == level)
            grid[i] = 0;
    }
    i = pos - (pos % GRID_SIZE) * (GRID_SIZE + 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE + 1) {
        if (i < 0) {
            continue;
        }
        if (grid[i] == level)
            grid[i] = 0;
        if (i % GRID_SIZE == GRID_SIZE - 1)
            break;
    }
    i = pos - (GRID_SIZE - (pos % GRID_SIZE) - 1) * (GRID_SIZE - 1);
    for (; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE - 1) {
        if (i < 0) {
            continue;
        }
        if (grid[i] == level)
            grid[i] = 0;
        if (i % GRID_SIZE == 0)
            break;
    }
}

bool forward_check(int level) {
    bool res = false;
    for (int i = level * GRID_SIZE; i < GRID_SIZE * GRID_SIZE; i += GRID_SIZE) {
        res = false;
        for (int j = 0; j < GRID_SIZE; ++j) {
            if (grid[i + j] == 0) {
                res = true;
                break;
            }
        }
        if (!res)
            return false;
    }
    return true;
}


void fc_method(int level) {
//    printf("%d\n", level);
    if (level == OBJ_LEVEL) {
        int *res = new int[GRID_SIZE * GRID_SIZE];
        memcpy(res, grid, sizeof(int) * GRID_SIZE * GRID_SIZE);
        ans.push_back(res);
//        exit(0);
        return;
    }
    int pos = level * GRID_SIZE;
    for (; pos < (level + 1) * GRID_SIZE; ++pos) {
        if (grid[pos] == 0) {
            grid[pos] = 1;
            mark_remove(pos, -level - 1);
            if (forward_check(level + 1)) {
//                printf("--------------------------------------------------\n");
//                show_grid();
                fc_method(level + 1);
                unmark_remove(pos, -level - 1);
                grid[pos] = 0;
            } else {
                unmark_remove(pos, -level - 1);
                grid[pos] = 0;
            }
        }
    }
}


void backtrack(int level) {
    if (level == OBJ_LEVEL) {
        //            printf("--------------------------------------------------\n");
        //            show_grid();
        int *res = new int[GRID_SIZE * GRID_SIZE];
        memcpy(res, grid, sizeof(int) * GRID_SIZE * GRID_SIZE);
        ans.push_back(res);
        return;
    }
    int pos = level * GRID_SIZE;
    for (; pos < (level + 1) * GRID_SIZE; ++pos) {
        if (grid[pos] == 0) {
            grid[pos] = 1;
            if (constraint_check(pos)) {
                backtrack(level + 1);
                grid[pos] = 0;
            } else
                grid[pos] = 0;
        }
    }
}

int main(int argc, char *argv[]) {
    int input = atoi(argv[1]);
    GRID_SIZE = input;
    OBJ_LEVEL = input;
    grid = new int[GRID_SIZE * GRID_SIZE];
    backtrack(0);
//    grid[get_pos(0, 3)] = 1;
//    fc_method(0);
    printf("sum: %d\n", int(ans.size()));
    int n = 8;
    return 0;
}
