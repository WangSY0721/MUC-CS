import numpy as np
from dlgo import gotypes

# 定义棋盘列的字母
COLS = 'ABCDEFGHJKLMNOPQRST'
# 定义棋子对应的字符
STONE_TO_CHAR = {
    None: ' . ',
    gotypes.Player.black: ' x ',
    gotypes.Player.white: ' o ',
}


# 打印棋手的走棋
def print_move(player, move):
    # 如果走棋是过手
    if move.is_pass:
        move_str = 'passes'
    # 如果走棋是认输
    elif move.is_resign:
        move_str = 'resigns'
    # 否则，打印走棋的坐标
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))


# 打印棋盘
def print_board(board):
    # 从最后一行开始打印
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        # 从第一列开始打印
        for col in range(1, board.num_cols + 1):
            # 获取棋盘上的棋子
            stone = board.get(gotypes.Point(row=row, col=col))
            # 将棋子转换为字符
            line.append(STONE_TO_CHAR[stone])
        # 打印行
        print('%s%d %s' % (bump, row, ''.join(line)))
    # 打印列
    print('    ' + '  '.join(COLS[:board.num_cols]))


# 将坐标转换为棋盘上的点
def point_from_coords(coords):
    # 获取列
    col = COLS.index(coords[0]) + 1
    # 获取行
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)


# 将棋盘上的点转换为坐标
def coords_from_point(point):
    return '%s%d' % (
        COLS[point.col - 1],
        point.row
    )


# 定义走棋的年龄
class MoveAge():
    def __init__(self, board):
        # 初始化走棋的年龄为-1
        self.move_ages = - np.ones((board.num_rows, board.num_cols))

    # 获取走棋的年龄
    def get(self, row, col):
        return self.move_ages[row, col]

    # 重置走棋的年龄
    def reset_age(self, point):
        self.move_ages[point.row - 1, point.col - 1] = -1

    # 添加走棋的年龄
    def add(self, point):
        self.move_ages[point.row - 1, point.col - 1] = 0

    # 增加走棋的年龄
    def increment_all(self):
        self.move_ages[self.move_ages > -1] += 1
