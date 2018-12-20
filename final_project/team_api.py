import numpy as np
from ctypes import *

chess_board = np.zeros([8, 8])


def update_chess(chess_pos_x, chess_pos_y, color):
    chess_board[chess_pos_x][chess_pos_y] = color
    if chess_pos_x == -1:
        return
    chess_board[chess_pos_x][chess_pos_y] = color
    for x_dir in [-1, 0, 1]:
        for y_dir in [-1, 0, 1]:
            new_x = chess_pos_x
            new_y = chess_pos_y
            if x_dir == 0 and y_dir == 0:
                continue
            new_x += x_dir
            new_y += y_dir
            while 8 > new_x >= 0 and 8 > new_y >= 0 and chess_board[new_x][new_y] != 0:
                if chess_board[new_x][new_y] == color:
                    while new_x != chess_pos_x or new_y != chess_pos_y:
                        new_x -= x_dir
                        new_y -= y_dir
                        chess_board[new_x][new_y] = color
                    break
                new_x += x_dir
                new_y += y_dir


BLACK = 1
WHITE = -1
ai_1 = cdll.LoadLibrary("C:\\Users\\xieji\\Documents\\GitHub\\AI_Homework\\week_5\\ai.dll")
ai_2 = cdll.LoadLibrary("C:\\Users\\xieji\\Documents\\GitHub\\AI_Homework\\week_5\\ai.dll")

deploy_pos = (c_int * 5)()
deploy_pos[0] = 2
deploy_pos[1] = 3
# ai_1.add(deploy_pos)
# print(deploy_pos[2])
# ai_1.add(deploy_pos)
# print(deploy_pos[2])

chess_board[3][3] = -1
chess_board[3][4] = 1
chess_board[4][3] = 1
chess_board[4][4] = -1
deploy_pos[0] = -1
deploy_pos[2] = 0
deploy_pos[4] = WHITE
print(chess_board)
while deploy_pos[0] != -1 or deploy_pos[2] != -1:
    deploy_pos[4] = BLACK if deploy_pos[4] == WHITE else WHITE
    ai_2.ai_move(deploy_pos)
    update_chess(deploy_pos[2], deploy_pos[3], deploy_pos[4])
    ai_1.deploy(deploy_pos)
    print('deploy pos', deploy_pos[2], deploy_pos[3])
    print(chess_board)
    deploy_pos[0] = deploy_pos[2]
    deploy_pos[1] = deploy_pos[3]
    deploy_pos[4] = BLACK if deploy_pos[4] == WHITE else WHITE
    ai_1.ai_move(deploy_pos)
    update_chess(deploy_pos[2], deploy_pos[3], deploy_pos[4])
    ai_2.deploy(deploy_pos)
    print('deploy pos', deploy_pos[2], deploy_pos[3])
    print(chess_board)
print(np.sum(chess_board))
