# 6-2 按名称创建围棋棋盘编码器
import importlib


__all__ = [
    'Encoder',
    'get_encoder_by_name',
]


# 6-1 用于编码围棋游戏状态的抽象Encoder类
class Encoder:
    def name(self):  # <1>把模型正在使用的编码器名称输出到日志中或存储下来
        raise NotImplementedError()

    def encode(self, game_state):  # <2>将围棋棋盘转换为数值数据
        raise NotImplementedError()

    def encode_point(self, point):  # <3>将棋盘上的一个交叉点转换为一个整数索引
        raise NotImplementedError()

    def decode_point_index(self, index):  # <4>将整数索引转换回围棋棋盘上的交叉点
        raise NotImplementedError()

    def num_points(self):  # <5>棋盘上交叉点的总数，即棋盘宽度乘以棋盘高度
        raise NotImplementedError()

    def shape(self):  # <6>棋盘结构编码后的形状
        raise NotImplementedError()




# 6-2 按名称创建围棋棋盘编码器
def get_encoder_by_name(name, board_size):  # <1>可以根据编码器的名称来创建它的实例
    if isinstance(board_size, int):
        board_size = (board_size, board_size)  # <2>若board_size是一个整数，则依据这个尺寸创建一个正方形棋盘
    module = importlib.import_module('dlgo.encoders.' + name)
    constructor = getattr(module, 'create')  # <3>每个编码器的实现类都必须提供一个“create”函数来创建新实例
    return constructor(board_size)

