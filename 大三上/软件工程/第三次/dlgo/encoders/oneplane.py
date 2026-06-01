# 6-3 使用简单的单平面围棋棋盘编码器对游戏状态进行编码
import numpy as np

from dlgo.encoders.base import Encoder
from dlgo.agent.goboard import Point



# 6-3 使用简单的单平面围棋棋盘编码器对游戏状态进行编码
class OnePlaneEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self):  # <1>用名称“oneplane”来指代这个编码器
        return 'oneplane'

    def encode(self, game_state):  # <2>编码逻辑：对于棋盘上的每一个交叉点，如果该点落下的是当前执子方的棋子，则在矩阵中填充1；如果是对手方的棋子，则填充-1；如果该点为空点，则填充0
        board_matrix = np.zeros(self.shape())
        next_player = game_state.next_player
        for r in range(self.board_height):
            for c in range(self.board_width):
                p = Point(row=r + 1, col=c + 1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    continue
                if go_string.color == next_player:
                    board_matrix[0, r, c] = 1
                else:
                    board_matrix[0, r, c] = -1
        return board_matrix


# 6-4 使用单平面围棋棋盘编码器对交叉点进行编码和解码
    def encode_point(self, point):  # <1>将棋盘交叉点转换为整数索引
        return self.board_width * (point.row - 1) + (point.col - 1)

    def decode_point_index(self, index):  # <2>将整数索引转换为棋盘交叉点
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)

    def num_points(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width




# tag::oneplane_create[]
def create(board_size):
    return OnePlaneEncoder(board_size)
# end::oneplane_create[]
