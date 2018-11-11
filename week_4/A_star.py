class Node:
    def __init__(self, x, y, path_cost, parent=None):
        self.x = x
        self.y = y
        self.path_cost = path_cost
        self.parent = parent


puzzle_data = [[11, 3, 1, 7], [4, 6, 8, 2], [15, 9, 10, 13], [14, 12, 5, 0]]

open_list = []
close_list = []
