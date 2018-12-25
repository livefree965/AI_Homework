//
// Created by root on 12/25/18.
//
#include "value_funciton.h"
#include <cmath>
using namespace std;
double value_grid(int grid[GRID_SIZE][GRID_SIZE]) {
    //落子数
//    double res = 0;
//    for (int i = 0; i < 6; ++i) {
//        for (int j = 0; j < 6; ++j) {
//            res -= grid[i][j];
//        }
//    }

    //曼哈顿乘积
    double res = 0;
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            res -= grid[i][j] * abs((i - 3.5) * (j - 3.5));
        }
    }

    //固定权重
//    double res = 0;
//    for (int i = 0; i < 6; ++i) {
//        for (int j = 0; j < 6; ++j) {
//            res -= grid[i][j] * weights2[i][j];
//        }
//    }

    //动态权重
//    double res = 0;
//    int steps = 0;
//    int after_res = 0;
//    for (int i = 0; i < 6; ++i) {
//        for (int j = 0; j < 6; ++j) {
//            if (grid[i][j] != 0) {
//                steps++;
//                after_res -= grid[i][j];
//            }
//        }
//    }
//    if (steps > METHOD_TRUN)
//        return after_res;
//    else {
//        for (int i = 0; i < 6; ++i) {
//            for (int j = 0; j < 6; ++j) {
//                if (weights2[i][j] == 50) {
//                    res -= grid[i][j] * (70 - steps);
//                } else if (weights2[i][j] == -20)
//                    res -= grid[i][j] * (-50 + steps);
//                else if (weights2[i][j] == -10)
//                    res -= grid[i][j] * (-40 + steps);
//            }
//        }
//    }
//    res += deploy_option(grid, BLACK).size();
    return res;
}