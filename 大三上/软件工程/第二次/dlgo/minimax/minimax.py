import enum
import random

from dlgo.agent import Agent

__all__ = [
    'MinimaxAgent',
]


# 定义游戏结果枚举类
class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3


# 反转游戏结果
def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw


# 计算游戏状态的最佳结果
def best_result(game_state):
    if game_state.is_over():
        # 游戏已经结束
        if game_state.winner() == game_state.next_player:
            # 我们赢了！
            return GameResult.win
        elif game_state.winner() is None:
            # 平局
            return GameResult.draw
        else:
            # 对手赢了。
            return GameResult.loss

    best_result_so_far = GameResult.loss
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)     
        opponent_best_result = best_result(next_state)         
        our_result = reverse_game_result(opponent_best_result) 
        if our_result.value > best_result_so_far.value:        
            best_result_so_far = our_result
    return best_result_so_far



class MinimaxAgent(Agent):
    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []
        # 遍历所有合法移动
        for possible_move in game_state.legal_moves():
            # 计算如果我们选择这个移动的游戏状态
            next_state = game_state.apply_move(possible_move)
            # 由于对手先走，找出他们最佳的可能结果
            opponent_best_outcome = best_result(next_state)
            # 我们的最佳结果是对手的相反结果
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            # 将这个移动添加到适当的列表中
            if our_best_outcome == GameResult.win:
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.draw:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)
        if winning_moves:
            return random.choice(winning_moves)
        if draw_moves:
            return random.choice(draw_moves)
        return random.choice(losing_moves)