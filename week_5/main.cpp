#include <iostream>
#include <vector>
#include <set>
#include <memory.h>
#include <random>
#include <pthread.h>
#include "value_funciton.h"

#define WHITE 1
#define BLACK -1
#define MAXPLAYER -1
#define MINPLAYER 1
int SEARCH_DEPTH = 6;
using namespace std;

int METHOD_TRUN = 20;
int weights2[8][8] = {{50,  -10, 0, 0, 0, 0, -10, 50},
                      {-10, -20, 0, 0, 0, 0, -20, -10},
                      {0,   0,   0, 0, 0, 0, 0,   0},
                      {0,   0,   0, 0, 0, 0, 0,   0},
                      {-10, -20, 0, 0, 0, 0, -20, -10},
                      {50,  -10, 0, 0, 0, 0, -10, 50}};
int python_grid[8][8] = {{0, 0, 0, 0,  0,  0, 0, 0},
                         {0, 0, 0, 0,  0,  0, 0, 0},
                         {0, 0, 0, 0,  0,  0, 0, 0},
                         {0, 0, 0, 1,  -1, 0, 0, 0},
                         {0, 0, 0, -1, 1,  0, 0, 0},
                         {0, 0, 0, 0,  0,  0, 0, 0},
                         {0, 0, 0, 0,  0,  0, 0, 0},
                         {0, 0, 0, 0,  0,  0, 0, 0}};

//python_grid[3][3]=-1;
//python_grid[3][4]=1;
//python_grid[4][3]=1;
//python_grid[4][4]=-1;
int python_decide[2];

struct Action {
    int x; //x,y 为坐标
    int y;
    int color; //准备下的棋的颜色
    vector<pair<int, int>> change_way; //下棋后翻转对方的方向

    Action(int x_, int y_, int color_) {
        x = x_;
        y = y_;
        color = color_;
    }
};

struct AlphaPara {
    int (*grid)[GRID_SIZE];
    int depth;
    double alpha;
    double beta;
    int player;
    double result;

    AlphaPara(int (*grid_)[GRID_SIZE], int depth_, double alpha_, double beta_, int player_) {
        grid = grid_;
        depth = depth_;
        alpha = alpha_;
        beta = beta_;
        player = player_;
    }
};

struct AlphaTree {
    int (*GRID)[GRID_SIZE];
    int player;
    int alpha;
    int beta;
    vector<struct AlphaTree *> children;

    AlphaTree(int(*grid_)[GRID_SIZE], int player_, int alpha_, int beta_) {
        GRID = grid_;
        player = player_;
        alpha = alpha_;
        beta = beta_;
    }
};

int directions[8][2] = {{-1, -1},
                        {-1, 0},
                        {-1, 1},
                        {0,  -1},
                        {0,  1},
                        {1,  -1},
                        {1,  0},
                        {1,  1}};
//一个棋子最多有8个方向进行翻转

vector<Action> deploy_option(int grid[GRID_SIZE][GRID_SIZE], int color) {
    vector<Action> res;
    int oppoent_color;
    if (color == WHITE)
        oppoent_color = BLACK;
    else
        oppoent_color = WHITE; //对手颜色
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            if (grid[i][j] != 0)
                continue;   //位置已经有棋子
            else {
                int newx, newy;     //从现在的位置开始探索不同方向上的坐标
                Action action(i, j, color); //创建关于该位置的行动
                for (auto &direction : directions) {
                    newx = i + direction[0];    //遍历所有方向，先走一步
                    newy = j + direction[1];
                    if (newx < 0 || newx >= GRID_SIZE || newy < 0 || newy >= GRID_SIZE ||
                        grid[newx][newy] != oppoent_color)
                        continue;   //如果该方向第一个点不是对手棋子，则该方向不能进行翻转
                    while (newx >= 0 && newx < GRID_SIZE && newy >= 0 && newy < GRID_SIZE &&
                           grid[newx][newy] == oppoent_color) {
                        newx += direction[0];
                        newy += direction[1];
                    }
                    //往该方向一直寻找，直到位置不是对方的棋子
                    if (newx >= 0 && newx < GRID_SIZE && newy >= 0 && newy < GRID_SIZE && grid[newx][newy] == color) {
                        //找到，坐标合理并且位置为自己的棋子，说明可以翻转
                        pair<int, int> ans(direction[0], direction[1]);
                        action.change_way.push_back(ans);
                        //该方向有效，记录下来放入容器
                    }
                }
                if (!action.change_way.empty())
                    //如果有方向可以翻转，则该位置下子有效，加入集合
                    res.push_back(action);
            }
        }
    }
    return res;
};


void deploy_chess(int grid[GRID_SIZE][GRID_SIZE], Action &action) {
    int newx, newy;
//    cout << "now pos" << action.x << " " << action.y << endl;
    grid[action.x][action.y] = action.color;
    for (int x_dir = -1; x_dir < 2; x_dir++) {
        for (int y_dir = -1; y_dir < 2; y_dir++) {
            newx = action.x;
            newy = action.y;
            if (x_dir == 0 && y_dir == 0)
                continue;
            newx += x_dir;
            newy += y_dir;
            while (grid[newx][newy] != 0 && newx >= 0 && newx < 8 && newy >= 0 && newy < 8) {
                if (grid[newx][newy] == action.color) {
                    while (newx != action.x || newy != action.y) {
                        newx -= x_dir;
                        newy -= y_dir;
                        grid[newx][newy] = action.color;
//                        cout << "change " << newx << " " << newy << endl;
                    }
                    break;
                }
                newx += x_dir;
                newy += y_dir;
            }
        }
    }
};

double alphabeta(int grid[GRID_SIZE][GRID_SIZE], int depth, double alpha, double beta, int player) {
    if (depth == 0) {
        return value_grid(grid);
    }
    //到达探索深度，直接返回棋盘评估值
    int tmp[GRID_SIZE][GRID_SIZE];  //新建临时棋盘
    if (player == MAXPLAYER) {
        vector<Action> choices = deploy_option(grid, BLACK);    //查找是否有行动可选择
        if (choices.empty())
            return value_grid(grid);
        for (auto &choice : choices) {
            memcpy(tmp, grid, GRID_SIZE * GRID_SIZE * sizeof(int));
            deploy_chess(tmp, choice);     //tmp是grid的副本
            alpha = max(alpha, alphabeta(tmp, depth - 1, alpha, beta, MINPLAYER));//递归获得下一层的alpha并取最大值
            if (beta <= alpha)
                break;  //剪枝
        }
        return alpha;
    } else {
        vector<Action> choices = deploy_option(grid, WHITE);
        if (choices.empty()) {
            return value_grid(grid);
        }
        for (auto &choice : choices) {
            memcpy(tmp, grid, GRID_SIZE * GRID_SIZE * sizeof(int));
            deploy_chess(tmp, choice);
            beta = min(beta, alphabeta(tmp, depth - 1, alpha, beta, MAXPLAYER));
            if (beta <= alpha)
                break;
        }
        return beta;
    }
}

void *alphabeta_thread(void *arg) {
    AlphaPara *params = (AlphaPara *) arg;
    int (*grid)[GRID_SIZE] = params->grid;
    int depth = params->depth;
    double alpha = params->alpha;
    double beta = params->beta;
    int player = params->player;
    params->result = alphabeta(grid, depth, alpha, beta, player);
    pthread_exit(NULL);

}

bool show_grid(int grid[GRID_SIZE][GRID_SIZE], vector<Action> *potent = nullptr) {
    int tmp[GRID_SIZE][GRID_SIZE];
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            tmp[i][j] = grid[i][j];
        }
    }
    char poten_char = 'A';
    if (potent != nullptr) {
        for (int i = 0; i < potent->size(); i++) {
            tmp[potent[0][i].x][potent[0][i].y] = poten_char;
            poten_char++;
        }
    }
    for (auto &i : tmp) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            if (i[j] == WHITE)
                cout << "# ";
            else if (i[j] == BLACK)
                cout << "@ ";
            else if (i[j] >= 'A')
                cout << char(i[j]) << " ";
            else
                cout << "_ ";
        }
        cout << endl;
    }
};

bool random_move(int grid[GRID_SIZE][GRID_SIZE], int player) {
    if (player == MAXPLAYER) {
        vector<Action> choices = deploy_option(grid, BLACK);
        if (choices.empty())
            return false;
        int tmp[GRID_SIZE][GRID_SIZE];
        int ai_choice = rand() % choices.size();
        deploy_chess(grid, choices[ai_choice]);
    } else {
        vector<Action> choices = deploy_option(grid, WHITE);
        if (choices.empty())
            return false;
        int tmp[GRID_SIZE][GRID_SIZE];
        int ai_choice = rand() % choices.size();
        deploy_chess(grid, choices[ai_choice]);
        python_decide[0] = choices[ai_choice].x;
        python_decide[1] = choices[ai_choice].y;
    }
    return true;
};
extern "C" {
void deploy(int *pos);
bool make_move(int grid[GRID_SIZE][GRID_SIZE], int player);
void ai_move(int *pos);
void ran_move(int *pos);
void python_show_grid();
void reload();
};

void python_show_grid() {
    show_grid(python_grid);
}

void ai_move(int *pos) {
//    show_grid(python_grid);
    int player;
    if (pos[4] == 1)
        player = MAXPLAYER;
    else
        player = MINPLAYER;
    bool res = make_move(python_grid, player);
    pos[2] = python_decide[0];
    pos[3] = python_decide[1];
    if (!res)
        pos[2] = -1;
}

void ran_move(int *pos) {
//    show_grid(python_grid);
    int player;
    if (pos[4] == 1)
        player = MAXPLAYER;
    else
        player = MINPLAYER;
    bool res = random_move(python_grid, player);
    pos[2] = python_decide[0];
    pos[3] = python_decide[1];
    if (!res)
        pos[2] = -1;
}

void deploy(int *pos) {
    if (pos[0] != -1) {
        Action action(pos[0], pos[1], -pos[4]);
        deploy_chess(python_grid, action);
    }
}

void reload() {
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < 8; ++j) {
            python_grid[i][j] = 0;
        }
    }
    python_grid[3][3] = 1;
    python_grid[3][4] = -1;
    python_grid[4][3] = -1;
    python_grid[4][4] = 1;
}

bool make_move(int grid[GRID_SIZE][GRID_SIZE], int player) {
    vector<Action> choices = deploy_option(grid, player);    //获取可以下棋的选择点
    if (choices.empty())    //查看是否可以下棋，不可以则返回false
        return false;
    int tmp[GRID_SIZE][GRID_SIZE];
    int ai_choice = 0;
    double now_alpha = player == BLACK ? -10000 : 10000;
    for (int i = 0; i < choices.size(); ++i) {
        memcpy(tmp, grid, GRID_SIZE * GRID_SIZE * sizeof(int));
        deploy_chess(tmp, choices[i]);  //取其中一个下棋点下棋
        double alpha = alphabeta(tmp, SEARCH_DEPTH, -1000000, 1000000, 1 ^ player);  //搜索返回预期的局面的结果
        if (now_alpha < alpha) {
            ai_choice = i;
            now_alpha = alpha;
        }
        //如果取到了更优的结果，更新
    }
    deploy_chess(grid, choices[ai_choice]); //正式采取这个下棋
    cout << "my move:" << endl;
    cout << choices[ai_choice].x << " " << choices[ai_choice].y << endl;
    return true;
};


bool input_move(int grid[GRID_SIZE][GRID_SIZE], int player) {
    vector<Action> choices;
    if (player == MAXPLAYER)
        choices = deploy_option(grid, BLACK);
    else
        choices = deploy_option(grid, WHITE);
    char human_choice;
//    show_grid(grid, &choices);
    if (!choices.empty()) {
        cin >> human_choice;
        human_choice -= 65;
        auto final_choice = int(human_choice);
        deploy_chess(grid, choices[final_choice]);
        return true;
    } else
        return false;

}

void init_grid(int grid[GRID_SIZE][GRID_SIZE]) {
    grid[3][3] = 1;
    grid[3][4] = -1;
    grid[4][3] = -1;
    grid[4][4] = 1;
}


void show_value(int grid[GRID_SIZE][GRID_SIZE], int player) {
    vector<Action> choices;
    int tmp[GRID_SIZE][GRID_SIZE];
    if (player == MAXPLAYER)
        choices = deploy_option(grid, BLACK);
    else
        choices = deploy_option(grid, WHITE);
    int oppent;
    if (player == MAXPLAYER)
        oppent = MINPLAYER;
    else
        oppent = MAXPLAYER;
    cout << "estimate value" << endl;
    show_grid(grid, &choices);
    char now_char = 'A';
    for (auto &choice : choices) {
        memcpy(tmp, grid, GRID_SIZE * GRID_SIZE * sizeof(int));
        deploy_chess(tmp, choice);
        double alpha = alphabeta(tmp, SEARCH_DEPTH, -1000000, 1000000, oppent);
        cout << now_char << " :" << alpha << endl;
        now_char++;
    }
    cout << endl;
};

int human_black() {
    int grid[GRID_SIZE][GRID_SIZE] = {0};
    init_grid(grid);
    int flag = true;
    while (flag) {
        flag = false;
        cout << "wait human and now value --------------------------------" << endl;
        show_value(grid, MAXPLAYER);
        flag += input_move(grid, MAXPLAYER);
        cout << "---------------------------------------------------------" << endl;
        cout << "wait AI and now value --------------------------------" << endl;
        show_value(grid, MINPLAYER);
        vector<Action> choices = deploy_option(grid, WHITE);
        flag += make_move(grid, MINPLAYER);
        cout << "---------------------------------------------------------" << endl;
    };
};

int human_white() {
    int grid[GRID_SIZE][GRID_SIZE] = {0};
    init_grid(grid);
    int flag = true;
    while (flag) {
        flag = false;
        show_value(grid, MAXPLAYER);
        flag += make_move(grid, MAXPLAYER);
        cout << "ai moved:" << endl;
        show_grid(grid);
        vector<Action> choices = deploy_option(grid, WHITE);
        cout << "human move:" << endl;
        flag += input_move(grid, MINPLAYER);
        show_grid(grid);
    };
}

void multi_thread() {
    int grid[GRID_SIZE][GRID_SIZE] = {0};
    init_grid(grid);
    struct AlphaTree root(grid, BLACK, -1000000, 1000000);

}

bool make_move_multithread(int grid[GRID_SIZE][GRID_SIZE], int player) {
    vector<Action> choices = deploy_option(grid, player);    //获取可以下棋的选择点
    if (choices.empty())    //查看是否可以下棋，不可以则返回false
        return false;
    int tmp[GRID_SIZE][GRID_SIZE];
    int ai_choice = 0;
    double now_alpha = player == BLACK ? -10000 : 10000;
    pthread_t thread_array[15];
    unsigned int choices_size = choices.size();
    double *alpha_set = new double[choices_size];
    AlphaPara **para_set = new AlphaPara *[choices_size];
    for (int i = 0; i < choices.size(); ++i) {
        memcpy(tmp, grid, GRID_SIZE * GRID_SIZE * sizeof(int));
        deploy_chess(tmp, choices[i]);  //取其中一个下棋点下棋
        AlphaPara tmp_para(tmp, SEARCH_DEPTH, -1000000, 1000000, 1 ^ player);
        para_set[i] = &tmp_para;
        double alpha_1 = alphabeta(tmp, SEARCH_DEPTH, -1000000, 1000000, 1 ^ player);  //搜索返回预期的局面的结果
        pthread_create(&thread_array[i], NULL, alphabeta_thread, (void *) &tmp_para);
//        pthread_join(thread_array[i],NULL);
        //如果取到了更优的结果，更新
    }
    for (int i = 0; i < choices_size; ++i) {
        pthread_join(thread_array[i], NULL);
    }
    for (int i = 0; i < choices_size; ++i) {
        double alpha = para_set[i]->result;
        if (now_alpha < alpha) {
            ai_choice = i;
            now_alpha = alpha;
        }
    }
    deploy_chess(grid, choices[ai_choice]); //正式采取这个下棋
    cout << "my move:" << endl;
    cout << choices[ai_choice].x << " " << choices[ai_choice].y << endl;
    return true;
};

int self_fight() {
    int grid[GRID_SIZE][GRID_SIZE] = {0};
    init_grid(grid);
    int flag = true;
    while (flag) {
        flag = false;
        cout << "wait human and now value --------------------------------" << endl;
        show_value(grid, MAXPLAYER);
//        flag += make_move(grid, MAXPLAYER);
        flag += make_move_multithread(grid, MAXPLAYER);
        cout << "---------------------------------------------------------" << endl;
        cout << "wait AI and now value --------------------------------" << endl;
        show_value(grid, MINPLAYER);
        vector<Action> choices = deploy_option(grid, WHITE);
        flag += random_move(grid, MINPLAYER);
//        cout << "---------------------------------------------------------" << endl;
    };
    int black = 0, white = 0;
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            if (grid[i][j] == 1)
                white++;
            else if (grid[i][j] == -1)
                black++;
        }
    }
    return black - white;
}

int main() {

    self_fight();
    int win = 0, lose = 0, tie = 0, res;
    for (int j = 0; j < 5; ++j) {
        win = lose = tie = 0;
        cout << "SEARCH DEPTH: " << SEARCH_DEPTH << endl;
        for (int i = 0; i < 200; ++i) {
            res = self_fight();
            if (res > 0)
                win++;
            else if (res == 0)
                tie++;
            else
                lose++;
        }
        cout << "lose: " << lose << " tie: " << tie << " win: " << win << " ratio: " << win / 200.0 << endl;
        SEARCH_DEPTH++;
    }

    return 0;
}