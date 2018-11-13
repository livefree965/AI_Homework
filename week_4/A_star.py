import copy
import prettytable as pt


# tk_root.mainloop()


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


class Node:
    def __init__(self, x, y, grid: list, path_cost, parent=None):
        self.x = x
        self.y = y
        self.grid = grid
        self.grid_hash = hash(str(grid))
        self.path_cost = path_cost
        self.estimate_cost = cal_estimate_cost(self.grid)
        self.parent = parent


def is_hash_in_list(obj_hash, src_list):
    for grid in src_list:
        if obj_hash == grid.grid_hash:
            return grid
    return False


sample_data = [[11, 3, 1, 7], [4, 9, 6, 2], [15, 12, 8, 10], [14, 0, 5, 13]]
puzzle_data = [[11, 3, 1, 7], [4, 6, 8, 2], [15, 9, 10, 13], [14, 12, 5, 0]]
goal_data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
goal_hash = hash(str(goal_data))


def show_final_path(final_node: Node):
    ans = []
    while final_node:
        ans.append(final_node)
        final_node = final_node.parent
    print('cost', len(ans))
    while len(ans):
        show_grid(ans.pop().grid)


max_cost = 0
if __name__ == "__main__":
    begin_node = Node(3, 3, puzzle_data, 0)
    open_list = [begin_node]
    close_list = []
    while len(open_list) > 0:
        open_list.sort(key=lambda x: x.estimate_cost + x.path_cost)
        now_node = open_list.pop(0)
        # show_grid(now_node.grid)
        # print(now_node.path_cost)
        if now_node.path_cost > max_cost:
            print('now path cost: ', now_node.path_cost, 'now estimate: ', now_node.estimate_cost)
            print(len(open_list), len(close_list))
            max_cost = now_node.path_cost
            show_grid(now_node.grid)
        if now_node.grid_hash == goal_hash:
            print('find solution:')
            show_final_path(now_node)
            break
        close_list.append(now_node)
        actions = [[0, 1], [0, -1], [-1, 0], [1, 0]]
        for action in actions:
            new_pos = [action[0] + now_node.x, action[1] + now_node.y]
            if 0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 4:
                new_grid = copy.deepcopy(now_node.grid)
                new_grid[new_pos[0]][new_pos[1]] = 0
                new_grid[now_node.x][now_node.y] = now_node.grid[new_pos[0]][new_pos[1]]
                new_grid_hash = hash(str(new_grid))
                if is_hash_in_list(new_grid_hash, close_list):
                    continue
                if is_hash_in_list(new_grid_hash, open_list):
                    old_node = is_hash_in_list(new_grid_hash, open_list)
                    old_g = old_node.path_cost
                    new_g = now_node.path_cost + 1
                    if new_g < old_g:
                        print('better road')
                        old_node.path_cost = now_node.path_cost + 1
                        old_node.parent = now_node
                        pass
                else:
                    new_node = Node(new_pos[0], new_pos[1], new_grid, now_node.path_cost + 1, parent=now_node)
                    open_list.append(new_node)
            else:
                continue
    # print('solution not found')
