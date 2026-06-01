import random
from .base import Agent
from .helpers import is_point_an_eye
from ..goboard import Move
from ..gotypes import Point

__all__ = ['RandomBot']


class RandomBot(Agent):
    # 选择一个随机有效的落子位置，确保不会破坏自己的眼形
    def select_move(self, game_state):
        """选择一个随机有效的落子位置，并且不会破坏我们的眼形。"""
        candidates = []  # 用于存储所有有效的候选落子点

        # 遍历棋盘的每一行和每一列，检查每个位置是否可以作为有效的落子点
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)  # 创建当前棋盘位置的点
                # 检查该位置是否是一个有效的落子位置，且不会破坏眼形
                if game_state.is_valid_move(Move.play(candidate)) and \
                        not is_point_an_eye(game_state.board, candidate, game_state.next_player):
                    candidates.append(candidate)  # 将符合条件的点加入候选列表

        # 如果没有找到有效的候选落子点，返回跳过当前回合的操作
        if not candidates:
            return Move.pass_turn()

        # 从候选落子点中随机选择一个进行落子
        return Move.play(random.choice(candidates))
