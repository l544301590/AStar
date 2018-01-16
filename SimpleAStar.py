def show_map(nodes):
    for i in range(len(nodes)):
        for j in range(len(nodes[0])):
            if nodes[i][j].type == 0:
                print("^", end=" ")
            elif nodes[i][j].type == 1:
                print("#", end=" ")
            elif nodes[i][j].type == 2 or nodes[i][j].type == 3:
                print("@", end=" ")
            else:
                print(".", end=" ")
        print()
    print()


def build_path(nodes, cur_node):
    for i in range(len(nodes)):
        for j in range(len(nodes[0])):
            if nodes[i][j].type == 4:
                nodes[i][j].type = 0
    p = cur_node
    while p.parent:
        nodes[p.x][p.y].type = 4
        p = p.parent


def distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)


def out_of_bound(x, y, nodes):
    if x < 0 or x > len(nodes) - 1 or y < 0 or y > len(nodes[0]) - 1:
        return True
    if nodes[x][y].type == 1:
        return True
    return False


def init_nodes(mp):
    nodes = []
    for i in range(len(mp)):
        nodes.append([])
        for j in range(len(mp[0])):
            nodes[i].append(Node(i, j, mp[i][j]))
    return nodes


class Node:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.g = 0
        self.h = 0
        self.parent = None

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Map:
    def __init__(self, data, sti, stj, edi, edj):
        self.data = data
        self.st = sti, stj
        self.ed = edi, edj


if __name__ == '__main__':

    # 0: space(^); 1: obstacle(#); 2: start(@); 3: end(@); 4: path(.)
    mp1 = Map([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], 4, 1, 5, 8)

    mp2 = Map([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [2, 0, 1, 0, 3],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ], 2, 0, 2, 4)

    mp = mp1
    nodes = init_nodes(mp.data)
    open_list = []
    close_list = []
    path = []

    st_i, st_j = mp.st
    ed_i, ed_j = mp.ed
    cur_node = nodes[st_i][st_j]

    open_list.append(cur_node)

    while open_list:
        # choose the best
        min_f = 65535
        for node in open_list:
            if node.g + node.h <= min_f:
                min_f = node.g + node.h
                cur_node = node

        open_list.remove(cur_node)
        close_list.append(cur_node)

        build_path(nodes, cur_node)
        show_map(nodes)

        # push its neighbors into open_list(four directions)
        neighborsIJ = [
            (cur_node.x, cur_node.y - 1),
            (cur_node.x, cur_node.y + 1),
            (cur_node.x - 1, cur_node.y),
            (cur_node.x + 1, cur_node.y)
        ]
        for i, j in neighborsIJ:
            if (not out_of_bound(i, j, nodes)) and (not nodes[i][j] in close_list) and (not nodes[i][j] in open_list):
                if i == ed_i and j == ed_j:
                    exit()
                open_list.append(nodes[i][j])
                nodes[i][j].parent = cur_node
                nodes[i][j].g = cur_node.g + 1
                nodes[i][j].h = distance(nodes[i][j].x, nodes[i][j].y, ed_i, ed_j)

