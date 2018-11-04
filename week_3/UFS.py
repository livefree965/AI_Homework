import copy


class Node:
    def __init__(self, state, pre_node, path_cost):
        self.state = state
        self.pre_node = pre_node
        self.path_cost = path_cost


def read_maze(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
        for line_pos, line_data in enumerate(data[21:39]):
            for cell_pos, cell in enumerate(line_data):
                if cell == 'S':
                    beg = [line_pos, cell_pos]
                if cell == 'E':
                    end = [line_pos, cell_pos]
        return [data[21:39], beg, end]


def is_state_in_nodeset(state, nodeset):
    for node in nodeset:
        if state[0] == node.state[0] and state[1] == node.state[1]:
            return [True, node.path_cost]
    return [False, None]


def print_path(node):
    path = []
    while (node.pre_node != None):
        path.append(node.state)
        node = node.pre_node
    for i in reversed(path):
        print(i)
    pass


def depth_limited_search(now_node, end_node, limit_depth, explored, maze_data):
    if limit_depth == 0:
        return False
    if now_node.state == end_node.state:
        return now_node
    explored.append(now_node.state)
    childlist = []
    for action in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        new_pos = [now_node.state[0] + action[0], now_node.state[1] + action[1]]
        if maze_data[new_pos[0]][new_pos[1]] == '1':
            continue
        child = Node(new_pos, now_node, now_node.path_cost + 1)
        if child.state not in explored:
            childlist.append(child)
    if len(childlist) == 0:
        return False
    res = False
    for child in childlist:
        res = depth_limited_search(child, end_node, limit_depth - 1, explored, maze_data)
        if res != False:
            break
    explored.pop()
    return res


def iterative_deepen_search():
    maze_data = read_maze('MazeData.txt')
    node = Node(maze_data[1], None, 0)
    goal_node = Node(maze_data[2], None, 0)
    maze_data = maze_data[0]
    for i in range(100):
        frontier = [node]
        explored = []
        res = depth_limited_search(copy.deepcopy(node), goal_node, i, explored, maze_data)
        if res != False:
            print('depth', i, 'found')
            return res
    return False


def uniform_cost_search():
    maze_data = read_maze('MazeData.txt')
    node = Node(maze_data[1], None, 0)
    goal_node = Node(maze_data[2], None, 0)
    maze_data = maze_data[0]
    frontier = [node]
    explored = []
    while True:
        frontier.sort(key=lambda x: x.path_cost, reverse=True)
        if len(frontier) == 0:
            return None
        node = frontier.pop()
        if node.state == goal_node.state:
            return node
        explored.append(node.state)
        for action in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            new_pos = [node.state[0] + action[0], node.state[1] + action[1]]
            if maze_data[new_pos[0]][new_pos[1]] == '1':
                continue
            child = Node(new_pos, node, node.path_cost + 1)
            if child.state not in explored and not is_state_in_nodeset(child.state, frontier)[0]:
                frontier.append(child)
            else:
                res = is_state_in_nodeset(child.state, frontier)
                if res[0] and res[1] > child.path_cost:
                    res[1].path_cost = child.path_cost
                    res[1].pre_node = child.pre_node


if __name__ == "__main__":
    # final_node = uniform_cost_search()
    final_node = iterative_deepen_search()
    print_path(final_node)
