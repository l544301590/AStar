import threading
import time


# node type
NOTHING = 0
OBSTACLE = 1
START = 2
GOAL = 3


"""
class Node:
    def __init__(self, row, col, type):
        self.row = row
        self.col = col
        self.type = type
        self.g = 0
        self.h = 0
        self.parent = None
"""


class Astar():
    def __init__(self, nodes):
        """
        :param nodes: 2D Nodes list including the info of start end goal
        """
        self.nodes = nodes
        self.open = []
        self.close = []
        self.path = []  # record current path

        self.st_node = self._get_start()  # start node
        self.gl_node = self._get_goal()  # goal node

        self.open.append(self.st_node)
        self.cur_node = self.st_node

        self.achieved = False  # if the goal is achieved

    def in_open(self, i, j):
        if self.nodes[i][j] in self.open:
            return True
        return False

    def in_close(self, i, j):
        if self.nodes[i][j] in self.close:
            return True
        return False

    def _get_start(self):
        """get start Node

        :return: start Node
        """
        st_node = []
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[0])):
                if self.nodes[i][j].type == START:
                    st_node.append(self.nodes[i][j])
        if len(st_node) == 0:
            raise Exception("No start")
        elif len(st_node) > 1:
            raise Exception("Several starts")
        else:
            return st_node[0]

    def _get_goal(self):
        """get goal Node

        :return: goal Node
        """
        goal_node = []
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[0])):
                if self.nodes[i][j].type == GOAL:
                    goal_node.append(self.nodes[i][j])
        if len(goal_node) == 0:
            raise Exception("No goal")
        elif len(goal_node) > 1:
            raise Exception("Several goals")
        return goal_node[0]

    def _out_of_bound(self, x, y):
        if x < 0 or x > len(self.nodes) - 1 or y < 0 or y > len(self.nodes[0]) - 1:
            return True
        if self.nodes[x][y].type == 1:
            return True
        return False

    def _achieved(self, node):
        if node is self.gl_node:
            return True
        return False

    def a_star(self):
        """one round

        :return:
        """
        # find the Node with min(g+h) in open
        min_f = 65535
        for node in self.open:
            if node.g + node.h < min_f:
                min_f = node.g + node.h
                self.cur_node = node

        if self._achieved(self.cur_node):
            self.achieved = True

        self.open.remove(self.cur_node)
        self.close.append(self.cur_node)

        neighborsIJ = [
            (self.cur_node.row+1, self.cur_node.col),
            (self.cur_node.row-1, self.cur_node.col),
            (self.cur_node.row,   self.cur_node.col+1),
            (self.cur_node.row,   self.cur_node.col-1)
        ]

        for i, j in neighborsIJ:
            if self._out_of_bound(i, j):
                continue
            node = self.nodes[i][j]
            if (node not in self.close) and (node not in self.open):
                self.open.append(node)
                node.g = self.cur_node.g + 1
                node.h = abs(node.row-self.gl_node.row) + abs(node.col-self.gl_node.col)
                node.parent = self.cur_node



