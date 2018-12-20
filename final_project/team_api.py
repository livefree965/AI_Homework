import numpy as np
from ctypes import *


def update_chess(chess_pos_x, chess_pos_y, color):
    if chess_pos_x == -1:
        return
    chess_board[chess_pos_x][chess_pos_y] = color
    for x_dir in [-1, 0, 1]:
        for y_dir in [-1, 0, 1]:
            new_x = chess_pos_x
            new_y = chess_pos_y
            if x_dir == 0 and y_dir == 0:
                continue
            while chess_board[new_x][new_y] != 0:
                new_x += x_dir
                new_y += y_dir
                if chess_board[new_x][new_y] == color:
                    while new_x != chess_pos_x:
                        new_x -= x_dir
                        new_y -= y_dir
                        chess_board[new_x][new_y] = color
                    break


BLACK = 1
WHITE = -1
ai_1 = cdll.LoadLibrary("C:\\Users\\xieji\\Documents\\GitHub\\AI_Homework\\final_project\\ai.dll")
ai_2 = cdll.LoadLibrary("C:\\Users\\xieji\\Documents\\GitHub\\AI_Homework\\final_project\\ai.dll")

deploy_pos = (c_int * 5)()
deploy_pos[0] = 2
deploy_pos[1] = 3
ai_1.add(deploy_pos)
print(deploy_pos[2])
chess_board = np.zeros([8, 8])
chess_board[3][3] = 1
chess_board[3][4] = -1
chess_board[4][3] = -1
chess_board[4][4] = 1
deploy_pos[0] = -1
deploy_pos[2] = 0
deploy_pos[4] = WHITE
print(chess_board)
while deploy_pos[0] != -1 and deploy_pos[2] != -1:
    deploy_pos[4] = BLACK if deploy_pos[4] == WHITE else WHITE
    ai_2.deploy(deploy_pos)
    update_chess(deploy_pos[2], deploy_pos[3], deploy_pos[4])
    deploy_pos[0] = deploy_pos[2]
    deploy_pos[1] = deploy_pos[3]
    deploy_pos[4] = BLACK if deploy_pos[4] == WHITE else WHITE
    ai_1.deploy(deploy_pos)
