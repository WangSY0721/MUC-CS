import copy
from dlgo.gotypes import Player, Point
from dlgo.scoring import compute_game_result
from dlgo import zobrist

# 定义Board、GameState、Move三个类
__all__ = [
    'Board',
    'GameState',
    'Move',
]


# 定义非法移动错误类
class IllegalMoveError(Exception):
    pass


class GoString:
    def __init__(self, color, stones, liberties):
        # 初始化GoString类，传入颜色、石子和自由度
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    def without_liberty(self, point):
        # 返回一个新的GoString对象，该对象在自由度中移除了传入的点
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point):
        # 返回一个新的GoString对象，该对象在自由度中添加了传入的点
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    def merged_with(self, string):
        # 返回一个新的GoString对象，该对象包含两个GoString对象中的所有石子
        assert string.color == self.color
        combined_stones = self.stones | string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        # 返回自由度的数量
        return len(self.liberties)

    def __eq__(self, other):
        # 判断两个GoString对象是否相等
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties

    def __deepcopy__(self, memodict={}):
        # 深度复制GoString对象
        return GoString(self.color, self.stones, copy.deepcopy(self.liberties))


class Board:
    def __init__(self, num_rows, num_cols):
        # 初始化棋盘，设置行数和列数
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}  # 棋盘上的格子
        self._hash = zobrist.EMPTY_BOARD  # 棋盘的哈希值

    def place_stone(self, player, point):
        # 在棋盘上放置一枚棋子
        assert self.is_on_grid(point)
        if self._grid.get(point) is not None:
            print('Illegal play on %s' % str(point))
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
                # 如果邻居为空，则增加一个空位
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                # 如果邻居颜色相同，则增加一个邻居
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                # 如果邻居颜色不同，则增加一个对手的邻居
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        # 创建一个新的棋子字符串
        new_string = GoString(player, [point], liberties)
        new_string = GoString(player, [point], liberties)

        # 合并相邻的棋子字符串
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        # 将新的棋子字符串添加到棋盘上
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string

        # 更新棋盘的哈希值
        self._hash ^= zobrist.HASH_CODE[point, player]

        # 处理对手的棋子字符串
        for other_color_string in adjacent_opposite_color:
            replacement = other_color_string.without_liberty(point)
            if replacement.num_liberties:
                self._replace_string(other_color_string.without_liberty(point))
            else:
                self._remove_string(other_color_string)


    def _replace_string(self, new_string):
        # 替换棋子字符串
        for point in new_string.stones:
            self._grid[point] = new_string

    def _remove_string(self, string):
        # 移除棋子字符串
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.with_liberty(point))
            self._grid[point] = None

            self._hash ^= zobrist.HASH_CODE[point, string.color]


    def is_on_grid(self, point):
        # 判断一个点是否在棋盘上
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get(self, point):
        string = self._grid.get(point)
        # 获取指定点的棋子
        if string is None:
            return None
        # 如果该点为空，则返回None
        return string.color

    def get_go_string(self, point):
        string = self._grid.get(point)
        # 获取指定点的棋子
        if string is None:
            return None
        # 如果该点为空，则返回None
        return string

    def __eq__(self, other):
        # 判断两个棋盘是否相等
        return isinstance(other, Board) and \
            self.num_rows == other.num_rows and \
            self.num_cols == other.num_cols and \
            self._hash() == other._hash()

    def __deepcopy__(self, memodict={}):
        # 深度复制棋盘
        copied = Board(self.num_rows, self.num_cols)

        copied._grid = copy.copy(self._grid)
        copied._hash = self._hash
        return copied


    def zobrist_hash(self):
        # 返回棋盘的哈希值
        return self._hash


class Move:
    def __init__(self, point=None, is_pass=False, is_resign=False):
        # 断言point、is_pass、is_resign中只有一个为True
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        # 如果point不为None，则is_play为True
        self.is_play = (self.point is not None)
        # 如果is_pass为True，则is_pass为True
        self.is_pass = is_pass
        # 如果is_resign为True，则is_resign为True
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        # 返回一个在棋盘上放置石头的动作
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        # 返回一个跳过的动作
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        # 返回一个认输的动作
        return Move(is_resign=True)

    def __str__(self):
        # 如果is_pass为True，则返回'pass'
        if self.is_pass:
            return 'pass'
        # 如果is_resign为True，则返回'resign'
        if self.is_resign:
            return 'resign'
        # 否则返回棋子的坐标
        return '(r %d, c %d)' % (self.point.row, self.point.col)


class GameState:
    def __init__(self, board, next_player, previous, move):
        # 初始化游戏状态
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        # 如果前一个状态为空，则将前一个状态集合设置为空集合
        if self.previous_state is None:
            self.previous_states = frozenset()
        # 否则，将前一个状态集合设置为前一个状态的前一个状态集合和前一个状态的下一个玩家和棋盘的zobrist哈希值的集合的并集
        else:
            self.previous_states = frozenset(
                previous.previous_states |
                {(previous.next_player, previous.board.zobrist_hash())})
        self.last_move = move

    def apply_move(self, move):
        # 应用移动
        if move.is_play:
            # 如果移动是下棋，则复制当前棋盘，并在移动的位置下棋
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            # 否则，将下一个棋盘设置为当前棋盘
            next_board = self.board
        # 返回一个新的游戏状态，下一个棋盘为下一个棋盘，下一个玩家为当前玩家的对手，前一个状态为当前状态，移动为移动
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        # 创建一个新的游戏
        if isinstance(board_size, int):
            # 如果board_size是整数，则将其转换为元组
            board_size = (board_size, board_size)
        # 创建一个新的棋盘
        board = Board(*board_size)
        # 返回一个新的游戏状态，棋盘为新的棋盘，下一个玩家为黑棋，前一个状态为空，移动为空
        return GameState(board, Player.black, None, None)

    def is_move_self_capture(self, player, move):
        # 判断移动是否是自杀
        if not move.is_play:
            # 如果移动不是下棋，则返回False
            return False
        # 复制当前棋盘
        next_board = copy.deepcopy(self.board)
        # 在移动的位置下棋
        next_board.place_stone(player, move.point)
        # 获取移动位置的围棋字符串
        new_string = next_board.get_go_string(move.point)
        # 如果围棋字符串的气数为0，则返回True，否则返回False
        return new_string.num_liberties == 0

    @property
    def situation(self):
        # 返回当前局势，即下一个玩家和棋盘
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        # 判断移动是否违反ko规则
        if not move.is_play:
            # 如果移动不是下棋，则返回False
            return False
        # 复制当前棋盘
        next_board = copy.deepcopy(self.board)
        # 在移动的位置下棋
        next_board.place_stone(player, move.point)
        # 获取下一个局势，即下一个玩家的对手和下一个棋盘的zobrist哈希值
        next_situation = (player.other, next_board.zobrist_hash())
        # 如果下一个局势在当前状态的前一个状态集合中，则返回True，否则返回False
        return next_situation in self.previous_states

    def is_valid_move(self, move):
        # 判断移动是否合法
        if self.is_over():
            # 如果游戏已经结束，则返回False
            return False
        if move.is_pass or move.is_resign:
            # 如果移动是过手或认输，则返回True
            return True
        # 如果移动的位置已经有棋子，或者移动是自杀，或者移动违反ko规则，则返回False，否则返回True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))

    def is_over(self):
        # 判断游戏是否结束
        if self.last_move is None:
            # 如果最后一个移动为空，则返回False
            return False
        if self.last_move.is_resign:
            # 如果最后一个移动是认输，则返回True
            return True
        # 获取倒数第二个移动
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            # 如果倒数第二个移动为空，则返回False
            return False
        # 如果最后一个移动和倒数第二个移动都是过手，则返回True，否则返回False
        return self.last_move.is_pass and second_last_move.is_pass

    def legal_moves(self):
        # 获取所有合法的移动
        moves = []
        # 遍历棋盘的每个位置
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                # 创建一个下棋的移动
                move = Move.play(Point(row, col))
                # 如果移动合法，则将其添加到移动列表中
                if self.is_valid_move(move):
                    moves.append(move)
        # 添加过手和认输的移动
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves

    def winner(self):
        # 获取游戏赢家
        if not self.is_over():
            # 如果游戏没有结束，则返回None
            return None
        if self.last_move.is_resign:
            # 如果最后一个移动是认输，则返回下一个玩家
            return self.next_player
        # 计算游戏结果
        game_result = compute_game_result(self)
        # 返回游戏结果的赢家
        return game_result.winner
