//
// Created by xieji on 2018/12/3.
//
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <cstring>
#include <memory.h>

#define GRID_SIZE 8
int OBJ_LEVEL = 8;
using namespace std;
vector<int *> ans;
int grid[GRID_SIZE * GRID_SIZE] = {0};

int get_pos(const int &x, const int &y) {
    return x * GRID_SIZE + y;
}

void show_grid() {
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            printf("%c  ", grid[i * GRID_SIZE + j] == 1 ? 'A' : 'O');
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


bool constraint_fine(int pos) {
    if (grid[pos] == 1)
        return false;
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

bool forward_check() {
    bool res = false;
    for (int i = 0; i < GRID_SIZE * GRID_SIZE; ++i) {
        res += constraint_fine(i);
        if (res)
            return true;
    }
    return false;
}

bool is_in_ans(int *grid) {
    bool res;
    for (int i = 0; i < ans.size(); ++i) {
        res = true;
        for (int j = 0; j < GRID_SIZE * GRID_SIZE; ++j) {
            if (grid[j] != ans[i][j]) {
                res = false;
                break;
            }
        }
        if (res)
            return true;
    }
    return false;
}

void backtrack(int level) {
    if (level == OBJ_LEVEL) {
        if (!is_in_ans(grid)) {
            printf("--------------------------------------------------\n");
            show_grid();
            int *res = new int[GRID_SIZE * GRID_SIZE];
            memcpy(res, grid, sizeof(int) * GRID_SIZE * GRID_SIZE);
            ans.push_back(res);
        }
        return;
    }
    int pos = 0;
    for (; pos < GRID_SIZE * GRID_SIZE; ++pos) {
        if (constraint_fine(pos)) {
            grid[pos] = 1;
//            printf("--------------------------------------------------\n");
//            show_grid();
//            show_grid();
            backtrack(level + 1);
            grid[pos] = 0;
        }
    }
}

int main() {
//    grid[get_pos(0, 3)] = 1;
    backtrack(0);
    printf("sum: %d\n", int(ans.size()));
    int n = 8;
    return 0;
}
