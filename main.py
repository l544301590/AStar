# In order to have algorithms executed step by step, there is two way
# 1. Let each algorithm class implement Thread. Sleep for a while at each end of the 'while'
# 2. Give MyWin a timer to control all the algorithms' execution, and use 'yield' in algorithms

import wx
import Astar
import random
import numpy as np


# node type
NOTHING = 0
OBSTACLE = 1
START = 2
GOAL = 3

# const
A = 20  # length of each side


class Node:
    def __init__(self, row, col, type):
        self.row = row
        self.col = col
        self.type = type
        self.g = 0
        self.h = 0
        self.parent = None


def mp1():
    """map1

    :return:
    """
    mp = [[NOTHING for j in range(20)] for i in range(20)]
    for i in range(5, 15):
        mp[i][10] = OBSTACLE
    mp[10][0] = START
    mp[10][19] = GOAL
    return mp


def gen_nodes_from_map(mp):
    """

    :param mp: 2D int list
    :return: nodes
    """
    nodes = []
    for i in range(len(mp)):
        nodes.append([])
        for j in range(len(mp[0])):
            nodes[i].append(Node(i, j, mp[i][j]))
    return nodes


def gen_nodes_randomly(map_size=(30, 30), obstacle_count=200):
    """It is a simple randomization

    :param map_size:
    :param obstacle_count:
    :return:
    """
    assert obstacle_count < map_size[0]*map_size[1]-2, "Too many obstacles!"
    assert map_size[0] > 8 and map_size[1] > 8, "Too small map!"

    np_arr = np.array([0 for i in range(map_size[0]*map_size[1])])

    indexes = random.sample(range(len(np_arr)), obstacle_count+2)
    for i in indexes:
        np_arr[i] = OBSTACLE
    np_arr[indexes[0]] = START
    np_arr[indexes[1]] = GOAL

    mp = list(np_arr.reshape(map_size))
    return gen_nodes_from_map(mp)


class MyWin(wx.Frame):

    def __init__(self, parent, title, size, nodes):
        super(MyWin, self).__init__(parent, title=title, size=size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Center()
        self.Show(True)
        self.alg1 = Astar.Astar(nodes)

    def on_paint(self, e):
        dc = wx.PaintDC(self)
        brush = wx.Brush(wx.Colour(160, 160, 160))
        dc.SetBackground(brush)
        dc.Clear()

        for i in range(len(self.alg1.nodes)):
            for j in range(len(self.alg1.nodes[0])):
                rgb = 160, 160, 160
                if self.alg1.nodes[i][j].type == OBSTACLE:
                    rgb = 0, 0, 0
                elif self.alg1.in_open(i, j):
                    rgb = 102, 255, 153
                elif self.alg1.in_close(i, j):
                    rgb = 255, 255, 102
                self._draw_rect(dc, j*A, i*A, rgb)

        st_node = self.alg1.st_node
        gl_node = self.alg1.gl_node
        cur_node = self.alg1.cur_node

        p = cur_node
        brush = wx.Brush(wx.Colour(153, 153, 255))
        dc.SetBrush(brush)
        while p:
            dc.DrawRectangle(p.col*A, p.row*A, A, A)
            p = p.parent

        self._draw_shadow(dc, st_node.col*A, st_node.row*A, (255, 0, 0))
        self._draw_shadow(dc, gl_node.col*A, gl_node.row*A, (255, 0, 0))
        self._draw_rect(dc, cur_node.col*A, cur_node.row*A, (255, 0, 0))

    def _draw_rect(self, dc, posX, posY, rgb):
        brush = wx.Brush(colour=wx.Colour(rgb))
        pen = wx.Pen()
        pen.SetWidth(1)
        pen.SetColour(wx.Colour(200, 200, 200))
        dc.SetBrush(brush)
        dc.SetPen(pen)
        dc.DrawRectangle(posX, posY, A, A)

    def _draw_shadow(self, dc, posX, posY, rgb):
        brush = wx.Brush(colour=wx.Colour(rgb))
        brush.SetStyle(wx.BRUSHSTYLE_BDIAGONAL_HATCH)
        pen = wx.Pen()
        pen.SetWidth(1)
        pen.SetColour(wx.Colour(200, 200, 200))
        dc.SetBrush(brush)
        dc.SetPen(pen)
        dc.DrawRectangle(posX, posY, A, A)

    def OnKeyDown(self, event):
        if self.alg1.achieved:
            return
        self.alg1.a_star()
        self.Refresh(False)


if __name__ == '__main__':
    app = wx.App()
    nodes = gen_nodes_randomly()
    MyWin(None, "abc", (len(nodes)*A, len(nodes[0])*A), nodes)
    app.MainLoop()
