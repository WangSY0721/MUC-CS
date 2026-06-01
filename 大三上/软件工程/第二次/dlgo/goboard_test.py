import unittest

import six

from dlgo.goboard import Board, GameState, Move
from dlgo.gotypes import Player, Point


class BoardTest(unittest.TestCase):
    # 测试捕获
    def test_capture(self):
        # 创建一个19x19的棋盘
        board = Board(19, 19)
        # 在(2,2)位置放置黑子
        board.place_stone(Player.black, Point(2, 2))
        # 在(1,2)位置放置白子
        board.place_stone(Player.white, Point(1, 2))
        # 断言(2,2)位置为黑子
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        # 在(2,1)位置放置白子
        board.place_stone(Player.white, Point(2, 1))
        # 断言(2,2)位置为黑子
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        # 在(2,3)位置放置白子
        board.place_stone(Player.white, Point(2, 3))
        # 断言(2,2)位置为黑子
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        # 在(3,2)位置放置白子
        board.place_stone(Player.white, Point(3, 2))
        # 断言(2,2)位置为空
        self.assertIsNone(board.get(Point(2, 2)))

    # 测试捕获两个子
    def test_capture_two_stones(self):
        # 创建一个19x19的棋盘
        board = Board(19, 19)
        # 在(2,2)位置放置黑子
        board.place_stone(Player.black, Point(2, 2))
        # 在(2,3)位置放置黑子
        board.place_stone(Player.black, Point(2, 3))
        # 在(1,2)位置放置白子
        board.place_stone(Player.white, Point(1, 2))
        # 在(1,3)位置放置白子
        board.place_stone(Player.white, Point(1, 3))
        # 断言(2,2)位置为黑子
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        # 断言(2,3)位置为黑子
        self.assertEqual(Player.black, board.get(Point(2, 3)))
        # 在(3,2)位置放置白子
        board.place_stone(Player.white, Point(3, 2))
        # 在(3,3)位置放置白子
        board.place_stone(Player.white, Point(3, 3))
        # 断言(2,2)位置为黑子
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        # 断言(2,3)位置为黑子
        self.assertEqual(Player.black, board.get(Point(2, 3)))
        # 在(2,1)位置放置白子
        board.place_stone(Player.white, Point(2, 1))
        # 在(2,4)位置放置白子
        board.place_stone(Player.white, Point(2, 4))
        # 断言(2,2)位置为空
        self.assertIsNone(board.get(Point(2, 2)))
        # 断言(2,3)位置为空
        self.assertIsNone(board.get(Point(2, 3)))

    # 测试捕获不是自杀
    def test_capture_is_not_suicide(self):
        # 创建一个19x19的棋盘
        board = Board(19, 19)
        # 在(1,1)位置放置黑子
        board.place_stone(Player.black, Point(1, 1))
        # 在(2,2)位置放置黑子
        board.place_stone(Player.black, Point(2, 2))
        # 在(1,3)位置放置黑子
        board.place_stone(Player.black, Point(1, 3))
        # 在(2,1)位置放置白子
        board.place_stone(Player.white, Point(2, 1))
        # 在(1,2)位置放置白子
        board.place_stone(Player.white, Point(1, 2))
        # 断言(1,1)位置为空
        self.assertIsNone(board.get(Point(1, 1)))
        # 断言(2,1)位置为白子
        self.assertEqual(Player.white, board.get(Point(2, 1)))
        # 断言(1,2)位置为白子
        self.assertEqual(Player.white, board.get(Point(1, 2)))

    # 测试移除空地
    def test_remove_liberties(self):
        # 创建一个5x5的棋盘
        board = Board(5, 5)
        # 在(3,3)位置放置黑子
        board.place_stone(Player.black, Point(3, 3))
        # 在(2,2)位置放置白子
        board.place_stone(Player.white, Point(2, 2))
        # 获取(2,2)位置的白子串
        white_string = board.get_go_string(Point(2, 2))
        # 断言白子串的空地包含(2,3)、(2,1)、(1,2)、(3,2)
        six.assertCountEqual(
            self,
            [Point(2, 3), Point(2, 1), Point(1, 2), Point(3, 2)],
            white_string.liberties)
        # 在(3,2)位置放置黑子
        board.place_stone(Player.black, Point(3, 2))
        # 获取(2,2)位置的白子串
        white_string = board.get_go_string(Point(2, 2))
        # 断言白子串的空地包含(2,3)、(2,1)、(1,2)
        six.assertCountEqual(
            self,
            [Point(2, 3), Point(2, 1), Point(1, 2)],
            white_string.liberties)

    # 测试空三角形
    def test_empty_triangle(self):
        # 创建一个5x5的棋盘
        board = Board(5, 5)
        # 在(1,1)位置放置黑子
        board.place_stone(Player.black, Point(1, 1))
        # 在(1,2)位置放置黑子
        board.place_stone(Player.black, Point(1, 2))
        # 在(2,2)位置放置黑子
        board.place_stone(Player.black, Point(2, 2))
        # 在(2,1)位置放置白子
        board.place_stone(Player.white, Point(2, 1))

        # 获取(1,1)位置的黑子串
        black_string = board.get_go_string(Point(1, 1))
        # 断言黑子串的空地包含(3,2)、(2,3)、(1,3)
        six.assertCountEqual(
            self,
            [Point(3, 2), Point(2, 3), Point(1, 3)],
            black_string.liberties)


class GameTest(unittest.TestCase):
    # 测试新游戏
    def test_new_game(self):
        # 创建一个19x19的新游戏
        start = GameState.new_game(19)
        # 在(16,16)位置放置白子
        next_state = start.apply_move(Move.play(Point(16, 16)))

        # 断言前一个状态为start
        self.assertEqual(start, next_state.previous_state)
        # 断言下一个玩家为白子
        self.assertEqual(Player.white, next_state.next_player)
        # 断言(16,16)位置为白子
        self.assertEqual(Player.black, next_state.board.get(Point(16, 16)))


if __name__ == '__main__':
    unittest.main()
