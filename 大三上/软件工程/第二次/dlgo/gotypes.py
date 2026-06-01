import enum
from collections import namedtuple

__all__ = [
    'Player',
    'Point',
]



# 定义一个枚举类，表示玩家
class Player(enum.Enum):
    black = 1  # 黑色玩家
    white = 2  # 白色玩家

    # 定义一个属性，返回另一个玩家
    @property
    def other(self):
        return Player.black if self == Player.white else Player.white


# 定义一个命名元组，表示棋盘上的一个点
class Point(namedtuple('Point', 'row col')):
    # 定义一个方法，返回该点的邻居点
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

    # 定义一个方法，返回该点的深拷贝
    def __deepcopy__(self, memodict={}):
        return self