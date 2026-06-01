import copy
from dlgo.gotypes import Player, Point
from dlgo.scoring import compute_game_result
from dlgo import zobrist
from dlgo.utils import MoveAge

__all__ = [
    'Board',
    'GameState',
    'Move',
]

# 定义两个空字典，用于存储邻居和角落的表格
neighbor_tables = {}
corner_tables = {}


# 初始化邻居表格
def init_neighbor_table(dim):
    # 获取行数和列数
    rows, cols = dim
    # 创建一个新的空字典
    new_table = {}
    # 遍历每一行
    for r in range(1, rows + 1):
        # 遍历每一列
        for c in range(1, cols + 1):
            # 创建一个点对象
            p = Point(row=r, col=c)
            # 获取该点的所有邻居
            full_neighbors = p.neighbors()
            # 过滤出在范围内的邻居
            true_neighbors = [
                n for n in full_neighbors
                if 1 <= n.row <= rows and 1 <= n.col <= cols]
            # 将该点的邻居存入字典
            new_table[p] = true_neighbors
    # 将字典存入全局字典
    neighbor_tables[dim] = new_table


# 初始化角落表格
def init_corner_table(dim):
    # 获取行数和列数
    rows, cols = dim
    # 创建一个新的空字典
    new_table = {}
    # 遍历每一行
    for r in range(1, rows + 1):
        # 遍历每一列
        for c in range(1, cols + 1):
            # 创建一个点对象
            p = Point(row=r, col=c)
            # 获取该点的所有角落
            full_corners = [
                Point(row=p.row - 1, col=p.col - 1),
                Point(row=p.row - 1, col=p.col + 1),
                Point(row=p.row + 1, col=p.col - 1),
                Point(row=p.row + 1, col=p.col + 1),
            ]
            # 过滤出在范围内的角落
            true_corners = [
                n for n in full_corners
                if 1 <= n.row <= rows and 1 <= n.col <= cols]
            # 将该点的角落存入字典
            new_table[p] = true_corners
    # 将字典存入全局字典
    corner_tables[dim] = new_table


# 定义一个异常类，用于表示非法移动
class IllegalMoveError(Exception):
    pass


class GoString():
    # 初始化GoString类，传入颜色、棋子、自由度
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    # 去除自由度
    def without_liberty(self, point):
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

    # 添加自由度
    def with_liberty(self, point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    # 合并两个GoString
    def merged_with(self, string):
        assert string.color == self.color
        combined_stones = self.stones | string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | string.liberties) - combined_stones)

    # 获取自由度数量
    @property
    def num_liberties(self):
        return len(self.liberties)

    # 判断两个GoString是否相等
    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties

    # 深度复制
    def __deepcopy__(self, memodict={}):
        return GoString(self.color, self.stones, copy.deepcopy(self.liberties))


class Board():
    def __init__(self, num_rows, num_cols):
        # 初始化棋盘，设置行数和列数
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}  # 棋盘格子
        self._hash = zobrist.EMPTY_BOARD  # 初始化哈希值

        global neighbor_tables
        dim = (num_rows, num_cols)
        # 初始化邻居表和角落表
        if dim not in neighbor_tables:
            init_neighbor_table(dim)
        if dim not in corner_tables:
            init_corner_table(dim)
        self.neighbor_table = neighbor_tables[dim]
        self.corner_table = corner_tables[dim]
        self.move_ages = MoveAge(self)


    def neighbors(self, point):
        # 获取某个点的邻居
        return self.neighbor_table[point]

    def corners(self, point):
        # 获取某个点的角落
        return self.corner_table[point]

    def place_stone(self, player, point):
        # 在某个点放置棋子
        assert self.is_on_grid(point)
        # 检查该点是否已经有棋子
        if self._grid.get(point) is not None:
            print('Illegal play on %s' % str(point))
        assert self._grid.get(point) is None
        # 初始化相邻棋子列表
        adjacent_same_color = []
        adjacent_opposite_color = []
        # 初始化空位列表
        liberties = []
        # 增加所有棋子的步数
        self.move_ages.increment_all()
        # 增加该点的步数
        self.move_ages.add(point)
        # 遍历该点的相邻点
        for neighbor in self.neighbor_table[point]:
            # 获取相邻点的棋子
            neighbor_string = self._grid.get(neighbor)
            # 如果相邻点没有棋子，则将该点加入空位列表
            if neighbor_string is None:
                liberties.append(neighbor)
            # 如果相邻点的棋子颜色与当前玩家相同，则将该棋子加入相邻棋子列表
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            # 如果相邻点的棋子颜色与当前玩家不同，则将该棋子加入相邻棋子列表
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        # 创建新的棋子字符串
        new_string = GoString(player, [point], liberties)
        # 合并相邻的相同颜色的棋子字符串
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        # 将新的棋子字符串加入棋盘
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        # 更新哈希值
        self._hash ^= zobrist.HASH_CODE[point, None]
        self._hash ^= zobrist.HASH_CODE[point, player]

        # 遍历相邻的相反颜色的棋子字符串
        for other_color_string in adjacent_opposite_color:
            # 移除该棋子字符串的空位
            replacement = other_color_string.without_liberty(point)
            # 如果移除空位后仍有空位，则替换该棋子字符串
            if replacement.num_liberties:
                self._replace_string(other_color_string.without_liberty(point))
            # 如果移除空位后没有空位，则移除该棋子字符串
            else:
                self._remove_string(other_color_string)

    def _replace_string(self, new_string):
        # 替换字符串
        for point in new_string.stones:
            self._grid[point] = new_string

    def _remove_string(self, string):
        # 移除字符串
        for point in string.stones:
            self.move_ages.reset_age(point)
            # 遍历字符串中的每个棋子
            for neighbor in self.neighbor_table[point]:
                neighbor_string = self._grid.get(neighbor)
                # 获取邻居棋子所在的字符串
                if neighbor_string is None:
                    continue
                # 如果邻居棋子所在的字符串为空，则跳过
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.with_liberty(point))
                # 如果邻居棋子所在的字符串不是当前字符串，则替换邻居棋子所在的字符串
            self._grid[point] = None
            # 将当前棋子所在的字符串置为空
            self._hash ^= zobrist.HASH_CODE[point, string.color]
            # 更新哈希值，移除当前棋子所在的字符串
            self._hash ^= zobrist.HASH_CODE[point, None]

    def is_self_capture(self, player, point):
        # 判断是否自吃
        friendly_strings = []
        for neighbor in self.neighbor_table[point]:
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                return False
            elif neighbor_string.color == player:
                friendly_strings.append(neighbor_string)
            else:
                if neighbor_string.num_liberties == 1:
                    return False
        if all(neighbor.num_liberties == 1 for neighbor in friendly_strings):
            return True
        return False

    def will_capture(self, player, point):
        # 判断是否吃子
        for neighbor in self.neighbor_table[point]:
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                continue
            elif neighbor_string.color == player:
                continue
            else:
                if neighbor_string.num_liberties == 1:
                    return True
        return False

    def is_on_grid(self, point):
        # 判断点是否在棋盘上
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get(self, point):
        # 获取某个点的颜色
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point):
        # 获取某个点的字符串
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    def __eq__(self, other):
        # 判断两个棋盘是否相等
        return isinstance(other, Board) and \
            self.num_rows == other.num_rows and \
            self.num_cols == other.num_cols and \
            self._hash() == other._hash()

    def __deepcopy__(self, memodict={}):
        # 深度拷贝棋盘
        copied = Board(self.num_rows, self.num_cols)
        copied._grid = copy.copy(self._grid)
        copied._hash = self._hash
        return copied

    def zobrist_hash(self):
        # 获取棋盘的哈希值
        return self._hash


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

    # 返回Move对象的字符串表示
    def __str__(self):
        if self.is_pass:
            return 'pass'
        if self.is_resign:
            return 'resign'
        return '(r %d, c %d)' % (self.point.row, self.point.col)

    # 返回Move对象的哈希值
    def __hash__(self):
        return hash((
            self.is_play,
            self.is_pass,
            self.is_resign,
            self.point))

    # 判断两个Move对象是否相等
    def  __eq__(self, other):
        return (
            self.is_play,
            self.is_pass,
            self.is_resign,
            self.point) == (
            other.is_play,
            other.is_pass,
            other.is_resign,
            other.point)


class GameState():
    # 初始化游戏状态
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        # 如果previous为None，则previous_states为空集合
        if previous is None:
            self.previous_states = frozenset()
        else:
            # 否则，previous_states为previous的previous_states加上(previous.next_player, previous.board.zobrist_hash())
            self.previous_states = frozenset(
                previous.previous_states |
                {(previous.next_player, previous.board.zobrist_hash())})
        self.last_move = move

    # 应用移动
    def apply_move(self, move):
        if move.is_play:
            # 如果移动是下棋，则复制当前棋盘，并在移动位置下棋
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            # 否则，next_board为当前棋盘
            next_board = self.board
        # 返回新的游戏状态
        return GameState(next_board, self.next_player.other, self, move)

    # 创建新的游戏
    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    # 判断移动是否导致自吃
    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        return self.board.is_self_capture(player, move.point)

    # 获取当前局面
    @property
    def situation(self):
        return (self.next_player, self.board)

    # 判断移动是否违反KO规则
    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False
        if not self.board.will_capture(player, move.point):
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states

    # 判断移动是否合法
    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))

    # 判断游戏是否结束
    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    # 获取合法移动
    def legal_moves(self):
        if self.is_over():
            return []
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves

    # 获取赢家
    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        game_result = compute_game_result(self)
        return game_result.winner
