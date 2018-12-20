import othello_module
from ctypes import *

res = cdll.LoadLibrary("C:\\Users\\xieji\\Documents\\GitHub\\AI_Homework\\week_5\\main.dll")
grid = (c_int * 36)()


class AI:
    def __init__(self, setting: '[L]east, [M]ost', level: '[R]egular, [E]asy, [M]edium, [H]ard'):
        self._setting = setting
        self._level = level

        if self._level == 'R':
            self._level = 'H'
            if self._setting == 'M':
                self._setting_most = False
            else:
                self._setting_most = True
        else:
            if self._setting == 'M':
                self._setting_most = True
            else:
                self._setting_most = False

    def make_move(self, game_state: othello_module.GameState) -> None:
        self.game_state = game_state

        self._find_options()
        self._find_sides_n_corners()
        if self._level == 'R':
            if self._setting == 'M':
                self._make_move_L()
            else:
                self._make_move_M()

        else:
            if self._setting == 'M':
                self._make_move_M()
            else:
                self._make_move_L()

    def _make_move_L(self) -> None:
        if self._basic != [] and self._level == 'H':
            spot = self._find_valuable(self._basic)
        elif self._on_side != [] and self._level == 'M':
            spot = self._find_valuable(self._on_side)
        else:
            spot = self._find_valuable(self._options)
        for i in range(6):
            for j in range(6):
                if self.game_state.board[i][j] == ' ':
                    grid[i] = 0
                elif self.game_state.board[i][j] == 'W':
                    grid[i] = 1
                else:
                    grid[i] = -1
        if self.game_state.current_turn == 'W':
            res.make_move(grid, 0)
        else:
            res.make_move(grid, 1)
        for i in range(6):
            for j in range(6):
                if self.game_state.board[i][j] == ' ' and grid[i][j] != 0:
                    self.game_state.drop_piece(i, j)
                    print(i, j)

    def _make_move_M(self) -> None:

        if self._in_corner != [] and self._level == 'H':
            spot = self._find_valuable(self._in_corner)
        elif self._on_side != [] and self._level == 'M':
            spot = self._find_valuable(self._on_side)
        else:
            spot = self._find_valuable(self._options)
        for i in range(6):
            for j in range(6):
                if self.game_state.board[i][j] == ' ':
                    grid[i * 6 + j] = 0
                elif self.game_state.board[i][j] == 'W':
                    grid[i * 6 + j] = 1
                else:
                    grid[i * 6 + j] = -1
        if self.game_state.current_turn == 'W':
            res.make_move(grid, 0)
        else:
            res.make_move(grid, 1)
        for i in range(6):
            for j in range(6):
                if self.game_state.board[i][j] == ' ' and grid[i * 6 + j] != 0:
                    self.game_state.drop_piece(i, j)
                    print(i, j)

    def _find_options(self) -> None:
        self._options = []

        for row in range(self.game_state.rows):
            for col in range(self.game_state.cols):
                if self.game_state.board[row][col] == ' ':
                    flips = len(self.game_state._find_all_flips_for_cell(row, col))
                    if flips != 0:
                        self._options.append(((row, col), flips))

    def _find_sides_n_corners(self) -> None:

        self._on_side = []
        self._in_corner = []
        self._basic = []

        for i in self._options:
            if (i[0][0] == 0 and i[0][1] == 0) or \
                    (i[0][0] == self.game_state.rows - 1 and i[0][1] == self.game_state.cols - 1) or \
                    (i[0][0] == self.game_state.rows - 1 and i[0][1] == 0) or \
                    (i[0][0] == 0 and i[0][1] == self.game_state.cols - 1):
                self._in_corner.append(i)
            elif i[0][0] == 0 or i[0][0] == self.game_state.rows - 1:
                self._on_side.append(i)
            elif i[0][1] == 0 or i[0][1] == self.game_state.cols - 1:
                self._on_side.append(i)
            else:
                self._basic.append(i)

    def _find_valuable(self, lst: [tuple]) -> None:
        lst.sort(key=_return_count, reverse=self._setting_most)
        return lst[0]


def _return_count(t: tuple) -> None:
    return t[1]
