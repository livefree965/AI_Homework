import copy

record_nodes = []

max_frontier_size = 0
max_explored_size = 0


class Node:
    def __init__(self, state, pre_node, path_cost):
        self.state = state  # 节点目前的位置，用大小为2的列表记录坐标
        self.pre_node = pre_node  # 指向路径的上一个节点
        self.path_cost = path_cost  # 记录从开始节点到现在的代价花费


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
    cost = 0
    path = []
    while (node.pre_node != None):
        path.append(node.state)
        node = node.pre_node
    for i in reversed(path):
        print(i)
        cost += 1
    print('cost sum: ', cost)
    pass


def print_graph(node, maze_data):
    path = []
    while (node.pre_node != None):
        path.append(node.state)
        node = node.pre_node
    for i in reversed(path):
        maze_data[i[0]] = list(maze_data[i[0]])
        maze_data[i[0]][i[1]] = 'R'
        maze_data[i[0]] = ''.join(maze_data[i[0]])
    for i in maze_data:
        print(i.strip().replace('0', ' ').replace('1', '%'))
    pass


def depth_limited_search(now_node, end_node, limit_depth, explored, maze_data):
    global max_explored_size, max_frontier_size
    max_explored_size += 1
    if limit_depth == 0:  # 如果已经搜索到最大深度则停止
        return False
    if now_node.state == end_node.state:  # 如果找到解则返回解
        return now_node
    explored.append(now_node.state)  # 将该节点标记为已探索
    # 当计算空间复杂度时用
    # max_explored_size = max(len(explored), max_explored_size)
    childlist = []  # 存储子节点
    for action in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        new_pos = [now_node.state[0] + action[0], now_node.state[1] + action[1]]
        if maze_data[new_pos[0]][new_pos[1]] == '1':  # 节点不可走，不加入列表
            continue
        child = Node(new_pos, now_node, now_node.path_cost + 1)
        if child.state not in explored:  # 节点并未被探索过
            childlist.append(child)
    if len(childlist) == 0:  # 如果没有子节点，则路径无解，返回
        explored.pop()
        return False
    res = False
    for child in childlist:  # 遍历子节点，更深入一层
        res = depth_limited_search(child, end_node, limit_depth - 1, explored, maze_data)
        if res != False:  # 如果找到解则返回
            break
    explored.pop()  # 弹出已探索的当前节点
    return res


def iterative_deepen_search():
    maze_data = read_maze('MazeData.txt')
    node = Node(maze_data[1], None, 0)
    goal_node = Node(maze_data[2], None, 0)
    maze_data = maze_data[0]
    for i in range(100):  # 不断加大深度寻找解
        global max_explored_size, max_frontier_size
        max_explored_size = 0
        frontier = [node]
        explored = []
        res = depth_limited_search(copy.deepcopy(node), goal_node, i, explored, maze_data)
        if res != False:  # 找到解则结束循环
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
        global max_frontier_size, max_explored_size
        frontier.sort(key=lambda x: x.path_cost, reverse=True)
        # 每次根据路径消耗进行排序
        if len(frontier) == 0:  # 没有边缘节点了则返回
            return None
        node = frontier.pop()  # 取出最小路径总代价的节点
        if node.state == goal_node.state:  # 找到解则返回解
            return node
        explored.append(node.state)
        global max_frontier_size, max_explored_size
        max_explored_size = max(len(explored), max_explored_size)
        for action in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            new_pos = [node.state[0] + action[0], node.state[1] + action[1]]
            if maze_data[new_pos[0]][new_pos[1]] == '1':  # 不是一条可用的路径，跳过
                continue
            child = Node(new_pos, node, node.path_cost + 1)
            if child.state not in explored and not is_state_in_nodeset(child.state, frontier)[0]:
                # 没有被探索过或者作为边缘节点
                frontier.append(child)
            else:
                # 如果节点为边缘节点，比较之前的路径花费和现在的路径花费，选最小的
                res = is_state_in_nodeset(child.state, frontier)
                if res[0] and res[1] > child.path_cost:
                    res[1].path_cost = child.path_cost
                    res[1].pre_node = child.pre_node
        max_frontier_size = max(len(frontier), max_frontier_size)


def BFS():
    maze_data = read_maze('MazeData.txt')
    node = Node(maze_data[1], None, 0)
    goal_node = Node(maze_data[2], None, 0)
    maze_data = maze_data[0]
    frontier = [node]  # 边缘节点
    explored = []  # 已探索节点
    while True:
        global max_frontier_size, max_explored_size
        if len(frontier) == 0:  # 如果没有边缘节点，则说明没有解
            break
        now_node = frontier[0]  # 弹出节点
        frontier.pop(0)
        if now_node.state == goal_node.state:  # 如果到达解，返回解
            return now_node
        explored.append(now_node.state)  # 标记为已探索
        max_explored_size = len(explored) if max_explored_size < len(explored) else max_explored_size
        for action in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            new_pos = [now_node.state[0] + action[0], now_node.state[1] + action[1]]
            if maze_data[new_pos[0]][new_pos[1]] == '1':
                continue
            child = Node(new_pos, now_node, now_node.path_cost + 1)
            if child.state not in explored:  # 将当前节点的子节点全部加入队列
                frontier.append(child)
        max_frontier_size = len(frontier) if max_frontier_size < len(frontier) else max_frontier_size
    return False


def gener_mat(src: list):
    obj_list = [0] * 36
    obj_lists = []
    for i in range(18):
        obj_lists.append(copy.deepcopy(obj_list))
    for node in src:
        obj_lists[node.state[0]][node.state[1]] = node.path_cost
    return obj_lists


if __name__ == "__main__":
    # final_node = uniform_cost_search()
    final_node = iterative_deepen_search()
    # final_node = BFS()
    maze_data = read_maze('MazeData.txt')[0]
    print_path(final_node)
    print_graph(final_node, maze_data)
    print('max explored:', max_explored_size)
    print('max frontier:', max_frontier_size)
