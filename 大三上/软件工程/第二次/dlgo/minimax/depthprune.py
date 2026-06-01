import random

from dlgo.agent import Agent
from dlgo.scoring import GameResult

__all__ = [
    'DepthPrunedAgent',
]

# 定义最大和最小分数
MAX_SCORE = 999999
MIN_SCORE = -999999


# 反转游戏结果
def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw


# 递归函数，计算游戏状态的最佳结果
def best_result(game_state, max_depth, eval_fn):
    # 如果游戏结束，返回最大或最小分数
    if game_state.is_over():                              
        if game_state.winner() == game_state.next_player: 
            return MAX_SCORE                              
        else:                                             
            return MIN_SCORE                              

    # 如果最大深度为0，返回评估函数的结果
    if max_depth == 0:                                    
        return eval_fn(game_state)                        

    # 初始化最佳结果为最小分数
    best_so_far = MIN_SCORE
    # 遍历所有合法的移动
    for candidate_move in game_state.legal_moves():       
        # 计算选择该移动后的游戏状态
        next_state = game_state.apply_move(candidate_move)
        # 计算对手的最佳结果
        opponent_best_result = best_result(               
            next_state, max_depth - 1, eval_fn)           
        # 计算我们的结果
        our_result = -1 * opponent_best_result            
        # 如果我们的结果比最佳结果好，更新最佳结果
        if our_result > best_so_far:                      
            best_so_far = our_result                      

    # 返回最佳结果
    return best_so_far


# 深度剪枝代理类
class DepthPrunedAgent(Agent):
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    # 选择移动
    def select_move(self, game_state):
        best_moves = []
        best_score = None
        # 遍历所有合法的移动
        for possible_move in game_state.legal_moves():
            # 计算选择该移动后的游戏状态
            next_state = game_state.apply_move(possible_move)
            # 计算对手的最佳结果
            opponent_best_outcome = best_result(next_state, self.max_depth, self.eval_fn)
            # 计算我们的结果
            our_best_outcome = -1 * opponent_best_outcome
            # 如果我们的结果比最佳结果好，更新最佳结果和最佳移动
            if (not best_moves) or our_best_outcome > best_score:
                # 这是最优的移动
                best_moves = [possible_move]
                best_score = our_best_outcome
            elif our_best_outcome == best_score:
                # 这和之前的最佳移动一样好
                best_moves.append(possible_move)
        # 随机选择一个最佳移动
        return random.choice(best_moves)
