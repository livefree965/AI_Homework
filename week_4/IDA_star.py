import copy
import prettytable as pt
import random


def cal_estimate_cost(grid):
    res = 0
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                res += abs((grid[i][j] - 1) % 4 - j) + abs(int((grid[i][j] - 1) / 4) - i)
    return res


def show_grid(grid):
    tb = pt.PrettyTable(header=False, hrules=pt.ALL)
    for i in range(4):
        tb.add_row(grid[i])
    print(tb)


def gener_grid(steps):
    goal_data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    zero_pos = [3, 3]
    next_list = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    for i in range(steps):
        while True:
            next_choice = random.randint(0, 3)
            next_pos = [zero_pos[0] + next_list[next_choice][0], zero_pos[1] + next_list[next_choice][1]]
            if 0 <= next_pos[0] < 4 and 0 <= next_pos[1] < 4:
                break
        goal_data[zero_pos[0]][zero_pos[1]] = goal_data[next_pos[0]][next_pos[1]]
        goal_data[next_pos[0]][next_pos[1]] = 0
        zero_pos = [next_pos[0], next_pos[1]]
    return goal_data


class Node:
    def __init__(self, x, y, grid: list, path_cost, parent=None):
        self.x = x
        self.y = y
        self.grid = grid
        self.grid_hash = hash(str(grid))
        self.path_cost = path_cost
        self.estimate_cost = cal_estimate_cost(self.grid)
        self.parent = parent

    def get_zero_pos(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    self.x = i
                    self.y = j


def is_hash_in_list(obj_hash, src_list):
    for grid in src_list:
        if obj_hash == grid.grid_hash:
            return grid
    return False


sample_data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 12], [13, 14, 11, 15]]
puzzle_data = [[11, 3, 1, 7], [4, 6, 8, 2], [15, 9, 10, 13], [14, 12, 5, 0]]
goal_data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
goal_hash = hash(str(goal_data))
open_list = []
close_list = []


def show_final_path(final_node: Node):
    ans = []
    while final_node:
        ans.append(final_node)
        final_node = final_node.parent
    while len(ans):
        show_grid(ans.pop().grid)


def depth_limited_search(now_node, limit_depth):
    global close_list, goal_hash
    if limit_depth == 0:  # 如果已经搜索到最大深度则停止
        return False
    if now_node.grid_hash == goal_hash:  # 如果找到解则返回解
        return now_node
    close_list.append(now_node)  # 将该节点标记为已探索
    # 当计算空间复杂度时用
    # max_explored_size = max(len(explored), max_explored_size)
    childlist = []  # 存储子节点
    for action in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        new_pos = [now_node.x + action[0], now_node.y + action[1]]
        if not (0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 4):  # 节点不可走，不加入列表
            continue
        new_grid = copy.deepcopy(now_node.grid)
        new_grid[new_pos[0]][new_pos[1]] = 0
        new_grid[now_node.x][now_node.y] = now_node.grid[new_pos[0]][new_pos[1]]
        new_grid_hash = hash(str(new_grid))
        if is_hash_in_list(new_grid_hash, close_list):
            continue
        new_node = Node(new_pos[0], new_pos[1], new_grid, now_node.path_cost + 1, parent=now_node)
        childlist.append(new_node)
    if len(childlist) == 0:  # 如果没有子节点，则路径无解，返回
        close_list.pop()
        return False
    res = False
    for child in childlist:  # 遍历子节点，更深入一层
        res = depth_limited_search(child, limit_depth - 1)
        if res != False:  # 如果找到解则返回
            break
    close_list.pop()  # 弹出已探索的当前节点
    return res


def iterative_deepen_search():
    global open_list, close_list
    global sample_data, puzzle_data, goal_data, goal_hash
    begin_node = Node(2, 2, puzzle_data, 0)
    begin_node.get_zero_pos()
    goal_node = Node(3, 3, goal_data, 0)
    open_list = [begin_node]
    close_list = []
    for i in range(100):  # 不断加大深度寻找解
        close_list = []
        print(i)
        res = depth_limited_search(begin_node, i)
        if res != False:  # 找到解则结束循环
            print('depth', i, 'found')
            return res
    return False


max_cost = 0
if __name__ == "__main__":
    begin_node = Node(3, 3, sample_data, 0)
    open_list = [begin_node]
    close_list = []
    iterative_deepen_search()
