#include <iostream>
#include <vector>
#include <set>
#include <memory.h>
#include <random>

#define WHITE 1
#define BLACK -1
#define GRID_SIZE 6
#define MAXPLAYER -1
#define MINPLAYER 1
#define SEARCH_DEPTH 6
using namespace std;

int METHOD_TRUN = 10;
int weights2[6][6] = {{50,  -10, 0, 0, -10, 50},
                      {-10, -20, 0, 0, -20, -10},
                      {0,   0,   0, 0, 0,   0},
                      {0,   0,   0, 0, 0,   0},
                      {-10, -20, 0, 0, -20, -10},
                      {50,  -10, 0, 0, -10, 50}};

struct Node {
    int x;
    int y;
    int color;
    vector<pair<int, int>> change_way;

    Node(int x_, int y_, int color_) {
        x = x_;
        y = y_;
        color = color_;
    }
};

int round_pos[8][2] = {{-1, -1},
                       {-1, 0},
                       {-1, 1},
                       {0,  -1},
                       {0,  1},
                       {1,  -1},
                       {1,  0},
                       {1,  1}};

vector<Node> deploy_option(int grid[GRID_SIZE][GRID_SIZE], int color) {
    vector<Node> res;
    int obj_color;
    if (color == WHITE)
        obj_color = BLACK;
    else
        obj_color = WHITE;
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            if (grid[i][j] != 0)
                continue;
            else {
                int newx, newy;
                Node node(i, j, color);
                for (auto &round_po : round_pos) {
                    newx = i + round_po[0];
                    newy = j + round_po[1];
                    if (newx < 0 || newx >= GRID_SIZE || newy < 0 || newy >= GRID_SIZE || grid[newx][newy] != obj_color)
                        continue;
                    while (newx >= 0 && newx < GRID_SIZE && newy >= 0 && newy < GRID_SIZE &&
                           grid[newx][newy] == obj_color) {
                        newx += round_po[0];
                        newy += round_po[1];
                    }
                    if (newx >= 0 && newx < GRID_SIZE && newy >= 0 && newy < GRID_SIZE && grid[newx][newy] == color) {
                        pair<int, int> ans(round_po[0], round_po[1]);
                        node.change_way.push_back(ans);
                    }
                }
                if (!node.change_way.empty())
                    res.push_back(node);
            }
        }
    }
    return res;
};

double value_grid(int grid[GRID_SIZE][GRID_SIZE]) {
    double res = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            res -= grid[i][j] * abs((i - 2.5) * (j - 2.5));
        }
    }


//    double res = 0;
//    for (int i = 0; i < 6; ++i) {
//        for (int j = 0; j < 6; ++j) {
//            res -= grid[i][j] * weights2[i][j];
//        }
//    }

//    double res = 0;
//    int steps = 0;
//    int after_res = 0;
//    for (int i = 0; i < 6; ++i) {
//        for (int j = 0; j < 6; ++j) {
//            if (grid[i][j] != 0) {
//                steps++;
//                after_res -= grid[i][j];
//            }
//            res -= grid[i][j] * weights2[i][j];
//        }
//    }
//    if (steps > 20)
//        return after_res;

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

bool gameend(int grid[GRID_SIZE][GRID_SIZE]) {
    int res = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            res -= grid[i][j];
        }
    }
    return res > 0;
}

bool deploy_chess(int grid[GRID_SIZE][GRID_SIZE], Node &obj) {
    int obj_color;
    if (obj.color == WHITE)
        obj_color = BLACK;
    else
        obj_color = WHITE;
    int newx, newy;
    newx = obj.x;
    newy = obj.y;
    for (int i = 0; i < obj.change_way.size(); ++i) {
        while (grid[newx][newy] != obj.color) {
            grid[newx][newy] = obj.color;
            newx += obj.change_way[i].first;
            newy += obj.change_way[i].second;
        }
    }
    return true;
};

double alphabeta(int grid[GRID_SIZE][GRID_SIZE], int depth, double alpha, double beta, int player) {
    if (depth == 0) {
        return value_grid(grid);
    }
    int tmp[GRID_SIZE][GRID_SIZE];
    memcpy(tmp, grid, 36 * sizeof(int));
    if (player == MAXPLAYER) {
        vector<Node> choices = deploy_option(grid, BLACK);
        if (choices.empty())
            return value_grid(grid);
        for (auto &choice : choices) {
            memcpy(tmp, grid, 36 * sizeof(int));
            deploy_chess(grid, choice);
            alpha = max(alpha, alphabeta(tmp, depth - 1, alpha, beta, MINPLAYER));
            if (beta <= alpha)
                break;
        }
        return alpha;
    } else {
        vector<Node> choices = deploy_option(grid, WHITE);
        if (choices.empty()) {
            if (gameend(grid))
                return 100000;
            else
                return -100000;
        }
        for (int i = 0; i < choices.size(); ++i) {
            memcpy(tmp, grid, 36 * sizeof(int));
            deploy_chess(tmp, choices[i]);
            beta = min(beta, alphabeta(tmp, depth - 1, alpha, beta, MAXPLAYER));
            if (beta <= alpha)
                break;
        }
        return beta;
    }

}

bool show_grid(int grid[GRID_SIZE][GRID_SIZE], vector<Node> *potent = nullptr) {
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

extern "C" {
bool make_move(int grid[GRID_SIZE][GRID_SIZE], int player);
};

bool make_move(int grid[GRID_SIZE][GRID_SIZE], int player) {
    if (player == MAXPLAYER) {
        vector<Node> choices = deploy_option(grid, BLACK);
        if (choices.empty())
            return false;
        int tmp[GRID_SIZE][GRID_SIZE];
        int ai_choice = 0;
        double max_alpha = -10000;
        for (int i = 0; i < choices.size(); ++i) {
            memcpy(tmp, grid, 36 * sizeof(int));
            deploy_chess(tmp, choices[i]);
            double alpha = alphabeta(tmp, SEARCH_DEPTH, -1000000, 1000000, MINPLAYER);
            if (max_alpha < alpha) {
                ai_choice = i;
                max_alpha = alpha;
            }
        }
        deploy_chess(grid, choices[ai_choice]);
    } else {
        vector<Node> choices = deploy_option(grid, WHITE);
        if (choices.empty())
            return false;
        int tmp[GRID_SIZE][GRID_SIZE];
        int ai_choice = 0;
        double min_alpha = 10000;
        for (int i = 0; i < choices.size(); ++i) {
            memcpy(tmp, grid, 36 * sizeof(int));
            deploy_chess(tmp, choices[i]);
            double alpha = alphabeta(tmp, SEARCH_DEPTH, -1000000, 1000000, MAXPLAYER);
            if (min_alpha > alpha) {
                ai_choice = i;
                min_alpha = alpha;
            }
        }
        deploy_chess(grid, choices[ai_choice]);
    }
    return true;
};

bool random_move(int grid[GRID_SIZE][GRID_SIZE], int player) {
    if (player == MAXPLAYER) {
        vector<Node> choices = deploy_option(grid, BLACK);
        if (choices.empty())
            return false;
        int tmp[GRID_SIZE][GRID_SIZE];
        int ai_choice = rand() % choices.size();
        deploy_chess(grid, choices[ai_choice]);
    } else {
        vector<Node> choices = deploy_option(grid, WHITE);
        if (choices.empty())
            return false;
        int tmp[GRID_SIZE][GRID_SIZE];
        int ai_choice = rand() % choices.size();
        deploy_chess(grid, choices[ai_choice]);
    }
    return true;
};

bool input_move(int grid[GRID_SIZE][GRID_SIZE], int player) {
    vector<Node> choices;
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
    grid[2][2] = 1;
    grid[2][3] = -1;
    grid[3][2] = -1;
    grid[3][3] = 1;
}


void show_value(int grid[GRID_SIZE][GRID_SIZE], int player) {
    vector<Node> choices;
    int tmp[GRID_SIZE][GRID_SIZE];
    if (player == MAXPLAYER)
        choices = deploy_option(grid, BLACK);
    else
        choices = deploy_option(grid, WHITE);
    cout << "estimate value" << endl;
    show_grid(grid, &choices);
    char now_char = 'A';
    for (auto &choice : choices) {
        memcpy(tmp, grid, 36 * sizeof(int));
        deploy_chess(tmp, choice);
        double alpha = alphabeta(tmp, SEARCH_DEPTH, -1000000, 1000000, MINPLAYER);
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
        vector<Node> choices = deploy_option(grid, WHITE);
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
        vector<Node> choices = deploy_option(grid, WHITE);
        cout << "human move:" << endl;
        flag += input_move(grid, MINPLAYER);
        show_grid(grid);
    };
}

int self_fight() {
    int grid[GRID_SIZE][GRID_SIZE] = {0};
    init_grid(grid);
    int flag = true;
    while (flag) {
        flag = false;
//        cout << "wait human and now value --------------------------------" << endl;
//        show_value(grid, MAXPLAYER);
        flag += make_move(grid, MAXPLAYER);
//        cout << "---------------------------------------------------------" << endl;
//        cout << "wait AI and now value --------------------------------" << endl;
//        show_value(grid, MINPLAYER);
        vector<Node> choices = deploy_option(grid, WHITE);
        flag += random_move(grid, MINPLAYER);
//        cout << "---------------------------------------------------------" << endl;
    };
    int black = 0, white = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            if (grid[i][j] == 1)
                white++;
            else if (grid[i][j] == -1)
                black++;
        }
    }
    return black - white;
}

int main() {
//    human_black();
    int win = 0, lose = 0, tie = 0, res;
    for (int j = 0; j < 20; ++j) {
        win = lose = tie = 0;
        METHOD_TRUN++;
        cout << "Now method turn: " << METHOD_TRUN << endl;
        for (int i = 0; i < 100; ++i) {
            res = self_fight();
            if (res > 0)
                win++;
            else if (res == 0)
                tie++;
            else
                lose++;
            cout << "lose: " << lose << " tie: " << tie << " win: " << win << endl;
        }
    }
    return 0;
}