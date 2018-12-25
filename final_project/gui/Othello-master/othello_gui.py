#  Kevan Hong-Nhan Nguyen 71632979.  ICS 32 Lab sec 9.  Project #5.

import othello
import othello_models
import tkinter

import numpy as np
from ctypes import *

chess_board = np.zeros([8, 8])
now_turn = 1


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

#### NOTE! You can change the game's settings by going to the menu
#### bar and clicking on
####
#### Game > Game Settings
####
#### Otherwise, the game's settings will remain the same.
####
#### If you want to play a new game, you just click on
#### Game > New Game


# Default / Initial Game Settings
DEFAULT_ROWS = 8
DEFAULT_COLUMNS = 8
DEFAULT_FIRST_PLAYER = othello.BLACK
DEFAULT_TOP_LEFT_PLAYER = othello.WHITE
DEFAULT_VICTORY_TYPE = othello.MOST_CELLS

# GUI Constants
BACKGROUND_COLOR = othello_models.BACKGROUND_COLOR
GAME_HEIGHT = 300
GAME_WIDTH = 300


class OthelloGUI:
    def __init__(self):
        # Initial Game Settings
        self._rows = DEFAULT_ROWS
        self._columns = DEFAULT_COLUMNS
        self._first_player = DEFAULT_FIRST_PLAYER
        self._top_left_player = DEFAULT_TOP_LEFT_PLAYER
        self._victory_type = DEFAULT_VICTORY_TYPE

        # Create my othello gamestate here (drawn from the original othello game code)
        self._game_state = othello.OthelloGame(self._rows, self._columns,
                                               self._first_player, self._top_left_player,
                                               self._victory_type)

        # Initialize all my widgets and window here
        self._root_window = tkinter.Tk()
        self._root_window.configure(background=BACKGROUND_COLOR)
        self._board = othello_models.GameBoard(self._game_state, GAME_WIDTH, GAME_HEIGHT, self._root_window)
        self._black_score = othello_models.Score(othello.BLACK, self._game_state, self._root_window)
        self._white_score = othello_models.Score(othello.WHITE, self._game_state, self._root_window)
        self._player_turn = othello_models.Turn(self._game_state, self._root_window)

        # Bind my game board with these two events.
        self._board.get_board().bind('<Configure>', self._on_board_resized)
        self._board.get_board().bind('<Button-1>', self._on_board_clicked)

        # Create our menu that can be accessed at the top of the GUI
        self._menu_bar = tkinter.Menu(self._root_window)
        self._game_menu = tkinter.Menu(self._menu_bar, tearoff=0)
        self._game_menu.add_command(label='New Game', command=self._new_game)
        self._game_menu.add_command(label='Game Settings', command=self._configure_game_settings)
        self._game_menu.add_separator()
        self._game_menu.add_command(label='Exit', command=self._root_window.destroy)
        self._menu_bar.add_cascade(label='Game', menu=self._game_menu)

        # Layout all the widgets here using grid layout
        self._root_window.config(menu=self._menu_bar)
        self._black_score.get_score_label().grid(row=0, column=0,
                                                 sticky=tkinter.S)
        self._white_score.get_score_label().grid(row=0, column=1,
                                                 sticky=tkinter.S)
        self._board.get_board().grid(row=1, column=0, columnspan=2,
                                     padx=50, pady=10,
                                     sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)
        self._player_turn.get_turn_label().grid(row=2, column=0, columnspan=2,
                                                padx=10, pady=10)

        # Configure the root window's row/column weight (from the grid layout)
        self._root_window.rowconfigure(0, weight=1)
        self._root_window.rowconfigure(1, weight=1)
        self._root_window.rowconfigure(2, weight=1)
        self._root_window.columnconfigure(0, weight=1)
        self._root_window.columnconfigure(1, weight=1)

    def start(self) -> None:
        ''' Runs the mainloop of the root window '''
        self._root_window.mainloop()

    def _configure_game_settings(self) -> None:
        ''' Pops out an options window to configure the game settings '''
        dialog = othello_models.OptionDialog(self._rows, self._columns,
                                             self._first_player, self._top_left_player,
                                             self._victory_type)
        dialog.show()
        if dialog.was_ok_clicked():
            # If the user clicked 'OK', then change all of the current game
            # settings to whatever the user chose them to be
            self._rows = dialog.get_rows()
            self._columns = dialog.get_columns()
            self._first_player = dialog.get_first_player()
            self._top_left_player = dialog.get_top_left_player()
            self._victory_type = dialog.get_victory_type()

            # Create a new game with these settings now
            self._new_game()

    def _new_game(self) -> None:
        ''' Creates a new game with current _game_state settings '''
        self._game_state = othello.OthelloGame(self._rows, self._columns,
                                               self._first_player, self._top_left_player,
                                               self._victory_type)
        self._board.new_game_settings(self._game_state)
        self._board.redraw_board()
        self._black_score.update_score(self._game_state)
        self._white_score.update_score(self._game_state)
        self._player_turn.update_turn(self._game_state.get_turn())

    def _on_board_clicked(self, event: tkinter.Event) -> None:
        ''' Attempt to play a move on the board if it's valid '''
        move = self._convert_point_coord_to_move(event.x, event.y)
        row = move[0]
        col = move[1]
        try:
            # me
            global now_turn
            if now_turn == 1:
                try:
                    self._game_state.move(row, col)
                except:
                    raise EOFError
                deploy_pos[4] = BLACK if deploy_pos[4] == WHITE else WHITE
                print('ai_move')
                deploy_pos[2] = row
                deploy_pos[3] = col
                # ai_2.ai_move(deploy_pos)
                update_chess(deploy_pos[2], deploy_pos[3], deploy_pos[4])
                deploy_pos[0] = deploy_pos[2]
                deploy_pos[1] = deploy_pos[3]
                ai_1.deploy(deploy_pos)
                print('deploy pos', deploy_pos[2], deploy_pos[3])
                # self._game_state.move(deploy_pos[2], deploy_pos[3])
                print(chess_board)
                deploy_pos[0] = deploy_pos[2]
                deploy_pos[1] = deploy_pos[3]
                now_turn = 0
                print('ai1')
                ai_1.python_show_grid()
                # print('ai2')
                # ai_2.python_show_grid()

                # deploy_pos[4] = BLACK if deploy_pos[4] == WHITE else WHITE
                # print('ai_move')
                # ai_2.ai_move(deploy_pos)
                # update_chess(deploy_pos[2], deploy_pos[3], deploy_pos[4])
                # deploy_pos[0] = deploy_pos[2]
                # deploy_pos[1] = deploy_pos[3]
                # ai_1.deploy(deploy_pos)
                # print('deploy pos', deploy_pos[2], deploy_pos[3])
                # self._game_state.move(deploy_pos[2], deploy_pos[3])
                # print(chess_board)
                # deploy_pos[0] = deploy_pos[2]
                # deploy_pos[1] = deploy_pos[3]
                # now_turn = 0
                # print('ai1')
                # ai_1.python_show_grid()
                # print('ai2')
                # ai_2.python_show_grid()


            else:
                deploy_pos[4] = BLACK if deploy_pos[4] == WHITE else WHITE
                ai_1.ai_move(deploy_pos)
                update_chess(deploy_pos[2], deploy_pos[3], deploy_pos[4])
                deploy_pos[0] = deploy_pos[2]
                deploy_pos[1] = deploy_pos[3]
                ai_2.deploy(deploy_pos)
                print('deploy pos', deploy_pos[2], deploy_pos[3])
                if deploy_pos[2] != -1:
                    self._game_state.move(deploy_pos[2], deploy_pos[3])
                print(chess_board)
                deploy_pos[0] = deploy_pos[2]
                deploy_pos[1] = deploy_pos[3]
                print('ai1')
                ai_1.python_show_grid()
                print('ai2')
                ai_2.python_show_grid()
                now_turn = 1

            # self._game_state.move(row, col)
            # self._game_state.move(4,2)
            self._board.update_game_state(self._game_state)
            self._board.redraw_board()
            self._black_score.update_score(self._game_state)
            self._white_score.update_score(self._game_state)

            if self._game_state.is_game_over():
                self._player_turn.display_winner(self._game_state.return_winner())
            else:
                self._player_turn.switch_turn(self._game_state)
        except:
            pass

    def _convert_point_coord_to_move(self, pointx: int, pointy: int) -> None:
        ''' Converts canvas point to a move that can be inputted in the othello game '''
        row = int(pointy // self._board.get_cell_height())
        if row == self._board.get_rows():
            row -= 1
        col = int(pointx // self._board.get_cell_width())
        if col == self._board.get_columns():
            col -= 1
        # return (3,2)
        return (row, col)

    def _on_board_resized(self, event: tkinter.Event) -> None:
        ''' Called whenever the canvas is resized '''
        self._board.redraw_board()


if __name__ == '__main__':
    OthelloGUI().start()
