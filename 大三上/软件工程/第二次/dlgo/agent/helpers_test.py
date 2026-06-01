import unittest

from .helpers import is_point_an_eye
from ..goboard import Board
from ..gotypes import Player, Point


class EyeTest(unittest.TestCase):
    # 测试角落情况：检查在棋盘角落处是否能构成眼
    def test_corner(self):
        board = Board(19, 19)  # 创建一个 19x19 的棋盘
        # 在棋盘上放置 3 个黑棋，形成一个 L 形
        board.place_stone(Player.black, Point(1, 2))
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.black, Point(2, 1))

        # 检查 (1, 1) 位置是否为黑方的眼，应该为 True
        self.assertTrue(is_point_an_eye(board, Point(1, 1), Player.black))
        # 检查 (1, 1) 位置是否为白方的眼，应该为 False
        self.assertFalse(is_point_an_eye(board, Point(1, 1), Player.white))

    # 测试不成立的眼：检查角落附近的点是否能形成眼
    def test_corner_false_eye(self):
        board = Board(19, 19)  # 创建一个 19x19 的棋盘
        # 放置 2 个黑棋，形成不完整的 L 形
        board.place_stone(Player.black, Point(1, 2))
        board.place_stone(Player.black, Point(2, 1))

        # 检查 (1, 1) 位置是否为黑方的眼，应该为 False，因为没有完全控制四个角落
        self.assertFalse(is_point_an_eye(board, Point(1, 1), Player.black))

        # 在 (2, 2) 位置放置白棋，破坏了形成眼的条件
        board.place_stone(Player.white, Point(2, 2))
        # 再次检查 (1, 1) 位置是否为黑方的眼，应该为 False
        self.assertFalse(is_point_an_eye(board, Point(1, 1), Player.black))

    # 测试中央情况：检查棋盘中央是否能形成眼
    def test_middle(self):
        board = Board(19, 19)  # 创建一个 19x19 的棋盘
        # 在棋盘中间放置多个黑棋，形成一个眼的形状
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.black, Point(3, 2))
        board.place_stone(Player.black, Point(4, 2))
        board.place_stone(Player.black, Point(4, 3))
        board.place_stone(Player.white, Point(4, 4))
        board.place_stone(Player.black, Point(3, 4))
        board.place_stone(Player.black, Point(2, 4))
        board.place_stone(Player.black, Point(2, 3))

        # 检查 (3, 3) 位置是否为黑方的眼，应该为 True，因为已经控制了足够的角落
        self.assertTrue(is_point_an_eye(board, Point(3, 3), Player.black))


if __name__ == '__main__':
    unittest.main()  # 运行单元测试
