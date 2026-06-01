import numpy as np
import copy
from dlgo.gotypes import Player
from dlgo.gotypes import Point
from dlgo.scoring import compute_game_result

__all__ = [
    'Board',
    'GameState',
    'Move',
]


class IllegalMoveError(Exception):
    pass


class GoString():
    # 初始化GoString类，传入颜色、棋子、空位
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    # 移除空位
    def remove_liberty(self, point):
        self.liberties.remove(point)

    # 添加空位
    def add_liberty(self, point):
        self.liberties.add(point)

    # 合并两个GoString
    def merged_with(self, go_string):
        # 断言两个GoString的颜色相同
        assert go_string.color == self.color
        # 合并棋子
        combined_stones = self.stones | go_string.stones
        # 返回合并后的GoString
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones)

    # 获取空位的数量
    @property
    def num_liberties(self):
        return len(self.liberties)

    # 判断两个GoString是否相等
    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties


class Board():
    # 初始化棋盘，设置行数和列数，并创建一个空字典用于存储棋盘上的棋子
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}




    # 在棋盘上放置棋子，判断棋子是否在棋盘上，并判断棋子是否已经存在
    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        # 遍历棋子的邻居
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                # 如果邻居为空，则将邻居加入空位列表
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                # 如果邻居颜色与当前玩家相同，则将邻居加入相同颜色列表
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                # 如果邻居颜色与当前玩家不同，则将邻居加入不同颜色列表
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        # 创建新的棋子字符串
        new_string = GoString(player, [point], liberties)

        # 遍历相同颜色的棋子字符串，合并
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        # 将新的棋子字符串加入棋盘
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        # 遍历不同颜色的棋子字符串，移除空位
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        # 遍历不同颜色的棋子字符串，如果空位为0，则移除棋子字符串
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    # 移除棋子字符串
    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None

    # 判断棋子是否在棋盘上
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    # 获取棋子颜色
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    # 获取棋子字符串
    def get_go_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string


    # 判断两个棋盘是否相等
    def __eq__(self, other):
        return isinstance(other, Board) and \
            self.num_rows == other.num_rows and \
            self.num_cols == other.num_cols and \
            self._grid == other._grid


class Move():
    # 初始化Move类，point为棋子位置，is_pass为是否过手，is_resign为是否认输
    def __init__(self, point=None, is_pass=False, is_resign=False):
        # 断言point、is_pass、is_resign中只能有一个为True
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        # 如果point不为None，则is_play为True
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    # 类方法，用于创建一个play类型的Move对象
    @classmethod
    def play(cls, point):
        return Move(point=point)

    # 类方法，用于创建一个pass类型的Move对象
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    # 类方法，用于创建一个resign类型的Move对象
    @classmethod
    def resign(cls):
        return Move(is_resign=True)


class GameState():
    def __init__(self, board, next_player, previous, move):
        # 初始化游戏状态，包括棋盘、下一个玩家、前一个状态和最后一步棋
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):  # <1>
        # 应用一步棋，返回新的游戏状态
        if move.is_play:
            # 如果是落子，则复制当前棋盘，并在新棋盘上落子
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            # 如果不是落子，则直接使用当前棋盘
            next_board = self.board
        # 返回新的游戏状态，下一个玩家是当前玩家的对手，前一个状态是当前状态，最后一步棋是当前棋
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        # 创建一个新的游戏状态，棋盘大小为board_size
        if isinstance(board_size, int):
            # 如果board_size是整数，则将其转换为元组
            board_size = (board_size, board_size)
        board = Board(*board_size)
        # 返回新的游戏状态，下一个玩家是黑子，前一个状态和最后一步棋为空
        return GameState(board, Player.black, None, None)

    def is_move_self_capture(self, player, move):
        # 判断当前玩家是否自吃
        if not move.is_play:
            # 如果不是落子，则直接返回False
            return False
        next_board = copy.deepcopy(self.board)
        # 复制当前棋盘，并在新棋盘上落子
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        # 如果新棋盘上该点的气为0，则返回True，否则返回False
        return new_string.num_liberties == 0

    @property
    def situation(self):
        # 返回当前局势，包括下一个玩家和棋盘
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        # 判断当前玩家是否违反KO规则
        if not move.is_play:
            # 如果不是落子，则直接返回False
            return False
        next_board = copy.deepcopy(self.board)
        # 复制当前棋盘，并在新棋盘上落子
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        # 计算新局势
        past_state = self.previous_state
        # 遍历前一个状态
        while past_state is not None:
            # 如果前一个状态与当前局势相同，则返回True，否则继续遍历
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
        # 如果遍历完所有前一个状态都没有找到相同的局势，则返回False
        return False

    def is_valid_move(self, move):
        # 判断当前棋是否合法
        if self.is_over():
            # 如果游戏已经结束，则返回False
            return False
        if move.is_pass or move.is_resign:
            # 如果是PASS或RESIGN，则返回True
            return True
        # 如果不是PASS或RESIGN，则判断是否自吃或违反KO规则
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))

    def is_over(self):
        # 判断游戏是否结束
        if self.last_move is None:
            # 如果最后一步棋为空，则返回False
            return False
        if self.last_move.is_resign:
            # 如果最后一步棋是RESIGN，则返回True
            return True
        second_last_move = self.previous_state.last_move
        # 获取倒数第二步棋
        if second_last_move is None:
            # 如果倒数第二步棋为空，则返回False
            return False
        # 如果最后一步棋和倒数第二步棋都是PASS，则返回True，否则返回False
        return self.last_move.is_pass and second_last_move.is_pass

    def legal_moves(self):
        # 获取所有合法的棋
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                # 遍历棋盘上的所有点，生成落子棋
                if self.is_valid_move(move):
                    # 如果落子棋合法，则添加到合法棋列表中
                    moves.append(move)
        moves.append(Move.pass_turn())
        moves.append(Move.resign())
        # 添加PASS和RESIGN棋
        return moves

    def winner(self):
        # 获取游戏赢家
        if not self.is_over():
            # 如果游戏没有结束，则返回None
            return None
        if self.last_move.is_resign:
            # 如果最后一步棋是RESIGN，则返回下一个玩家
            return self.next_player
        game_result = compute_game_result(self)
        # 计算游戏结果，返回赢家
        return game_result.winner
