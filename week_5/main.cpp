#include <iostream>
#include <vector>
#include <set>
#include <memory.h>

#define WHITE 1
#define BLACK -1
#define GRID_SIZE 6
#define MAXPLAYER 1
#define MINPLAYER 0
using namespace std;

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
                for (int k = 0; k < 8; ++k) {
                    newx = i + round_pos[k][0];
                    newy = j + round_pos[k][1];
                    if (newx < 0 || newx >= GRID_SIZE || newy < 0 || newy >= GRID_SIZE || grid[newx][newy] != obj_color)
                        continue;
                    while (newx >= 0 && newx < GRID_SIZE && newy >= 0 && newy < GRID_SIZE &&
                           grid[newx][newy] == obj_color) {
                        newx += round_pos[k][0];
                        newy += round_pos[k][1];
                    }
                    if (newx >= 0 && newx < GRID_SIZE && newy >= 0 && newy < GRID_SIZE && grid[newx][newy] == color) {
                        pair<int, int> ans(round_pos[k][0], round_pos[k][1]);
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

int value_grid(int grid[GRID_SIZE][GRID_SIZE]) {
    int blacks = 0, whites = 0;
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            if (grid[i][j] == WHITE)
                whites += 1;
            else if (grid[i][j] == BLACK)
                blacks += 1;
        }
    }
    return blacks - whites;
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

int alphabeta(int grid[GRID_SIZE][GRID_SIZE], int depth, int alpha, int beta, int player) {
    if (depth == 0)
        return value_grid(grid);
    int tmp[GRID_SIZE][GRID_SIZE];
    memcpy(tmp, grid, 36 * sizeof(int));
    vector<Node> choices = deploy_option(grid, BLACK);
    if (choices.empty())
        return value_grid(grid);
    else {
        if (player == MAXPLAYER) {
            for (int i = 0; i < choices.size(); ++i) {
                memcpy(tmp, grid, 36 * sizeof(int));
                deploy_chess(grid, choices[i]);
                alpha = max(alpha, alphabeta(tmp, depth - 1, alpha, beta, MINPLAYER));
                if (beta <= alpha)
                    break;
            }
            return alpha;
        } else {
            for (int i = 0; i < choices.size(); ++i) {
                beta = min(beta, alphabeta(tmp, depth - 1, alpha, beta, MAXPLAYER));
                if (beta <= alpha)
                    break;
            }
            return beta;
        }
    }
}

bool show_grid(int grid[GRID_SIZE][GRID_SIZE], vector<Node> *potent = NULL) {
    int tmp[GRID_SIZE][GRID_SIZE];
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            tmp[i][j] = grid[i][j];
        }
    }
    char poten_char = 'A';
    if (potent != NULL) {
        for (int i = 0; i < potent->size(); i++) {
            tmp[potent[0][i].x][potent[0][i].y] = poten_char;
            poten_char++;
        }
    }
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            if (tmp[i][j] == WHITE)
                cout << "# ";
            else if (tmp[i][j] == BLACK)
                cout << "@ ";
            else if (tmp[i][j] >= 'A' and tmp[i][j] <= 'G')
                cout << char(tmp[i][j]) << " ";
            else
                cout << "_ ";
        }
        cout << endl;
    }
};

int human_black() {
    int grid[GRID_SIZE][GRID_SIZE] = {0};
    grid[2][2] = 1;
    grid[2][3] = -1;
    grid[3][2] = -1;
    grid[3][3] = 1;
    int flag = true;
    while (flag) {
        flag = false;
        vector<Node> choices = deploy_option(grid, BLACK);
        int tmp[GRID_SIZE][GRID_SIZE];
        memcpy(tmp, grid, sizeof(int) * 36);
        show_grid(grid, &choices);
        char human_choice;
        if (!choices.empty()) {
            cin >> human_choice;
            human_choice -= 65;
            int final_choice = int(human_choice);
            deploy_chess(grid, choices[final_choice]);
            cout << "human moved:" << endl;
            show_grid(grid);
            flag = true;
        }
        choices = deploy_option(grid, WHITE);
        if (choices.empty()) {
            cout << "now:" << endl;
            choices = deploy_option(grid, BLACK);
            if (choices.empty())
                continue;
            flag = true;
            continue;
        }
        int ai_choice = 0, min_alpha = 10000;
        for (int i = 0; i < choices.size(); ++i) {
            memcpy(tmp, grid, 36 * sizeof(int));
            deploy_chess(tmp, choices[i]);
            int alpha = alphabeta(tmp, 12, -10000, 10000, MINPLAYER);
            if (min_alpha > alpha) {
                ai_choice = i;
                min_alpha = alpha;
            }
//            cout << alpha << endl;
        }
        cout << "ai moved:" << endl;
        deploy_chess(grid, choices[ai_choice]);
        flag = true;
    }
    cout << value_grid(grid) << endl;
};

int human_white() {
    int grid[GRID_SIZE][GRID_SIZE] = {0};
    grid[2][2] = 1;
    grid[2][3] = -1;
    grid[3][2] = -1;
    grid[3][3] = 1;
    int flag = true;
    while (flag) {
        flag = false;
        vector<Node> choices = deploy_option(grid, BLACK);
        int tmp[GRID_SIZE][GRID_SIZE];
        memcpy(tmp, grid, sizeof(int) * 36);
        int ai_choice = 0, min_alpha = 10000;
        for (int i = 0; i < choices.size(); ++i) {
            memcpy(tmp, grid, 36 * sizeof(int));
            deploy_chess(tmp, choices[i]);
            int alpha = alphabeta(tmp, 12, -10000, 10000, MAXPLAYER);
            if (min_alpha > alpha) {
                ai_choice = i;
                min_alpha = alpha;
            }
        }
        cout << "ai moved:" << endl;
        if (!choices.empty())
            deploy_chess(grid, choices[ai_choice]);
        show_grid(grid);
        cout << "human move:" << endl;
        choices = deploy_option(grid, WHITE);
        show_grid(grid, &choices);
        char human_choice;
        if (!choices.empty()) {
            cin >> human_choice;
            human_choice -= 65;
            int final_choice = int(human_choice);
            deploy_chess(grid, choices[final_choice]);
            cout << "human moved:" << endl;
            show_grid(grid);
            flag = true;
        } else if (!deploy_option(grid, BLACK).empty())
            flag = true;
    }
    cout << value_grid(grid) << endl;
};

int main() {
    human_white();
    return 0;
}