import random

from dlgo.agent import Agent
from dlgo.gotypes import Player

__all__ = [
    'AlphaBetaAgent',
]

# 定义最大和最小分数
MAX_SCORE = 999999
MIN_SCORE = -999999



# 定义alpha_beta_result函数，用于计算游戏状态下的最佳结果
def alpha_beta_result(game_state, max_depth, best_black, best_white, eval_fn):
    # 如果游戏结束，返回最大或最小分数
    if game_state.is_over():                                  
        if game_state.winner() == game_state.next_player:     
            return MAX_SCORE                                  
        else:                                                 
            return MIN_SCORE                                  

    # 如果最大深度为0，返回评估函数的结果
    if max_depth == 0:                                        
        return eval_fn(game_state)                            

    # 初始化最佳分数
    best_so_far = MIN_SCORE
    # 遍历所有合法的移动
    for candidate_move in game_state.legal_moves():           
        # 计算选择该移动后的游戏状态
        next_state = game_state.apply_move(candidate_move)    
        # 计算对手的最佳结果
        opponent_best_result = alpha_beta_result(             
            next_state, max_depth - 1,                        
            best_black, best_white,                           
            eval_fn)                                          
        # 计算我们的结果
        our_result = -1 * opponent_best_result                

        # 如果我们的结果比最佳分数高，更新最佳分数
        if our_result > best_so_far:                          
            best_so_far = our_result                          

        # 如果当前玩家是白色，更新最佳白色分数
        if game_state.next_player == Player.white:
            if best_so_far > best_white:                      
                best_white = best_so_far                      
            # 计算黑色玩家的结果
            outcome_for_black = -1 * best_so_far              
            # 如果黑色玩家的结果比最佳黑色分数低，返回最佳分数
            if outcome_for_black < best_black:                
                return best_so_far                            

        # 如果当前玩家是黑色，更新最佳黑色分数
        elif game_state.next_player == Player.black:
            if best_so_far > best_black:                      
                best_black = best_so_far                      
            # 计算白色玩家的结果
            outcome_for_white = -1 * best_so_far              
            # 如果白色玩家的结果比最佳白色分数低，返回最佳分数
            if outcome_for_white < best_white:                
                return best_so_far                            

    # 返回最佳分数
    return best_so_far



# 定义AlphaBetaAgent类，继承自Agent类
class AlphaBetaAgent(Agent):
    # 初始化函数，传入最大深度和评估函数
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    # 选择移动函数
    def select_move(self, game_state):
        # 初始化最佳移动列表和最佳分数
        best_moves = []
        best_score = None
        best_black = MIN_SCORE
        best_white = MIN_SCORE
        # 遍历所有合法的移动
        for possible_move in game_state.legal_moves():
            # 计算选择该移动后的游戏状态
            next_state = game_state.apply_move(possible_move)
            # 计算对手的最佳结果
            opponent_best_outcome = alpha_beta_result(
                next_state, self.max_depth,
                best_black, best_white,
                self.eval_fn)
            # 计算我们的结果
            our_best_outcome = -1 * opponent_best_outcome
            # 如果我们的结果比最佳分数高，更新最佳移动列表和最佳分数
            if (not best_moves) or our_best_outcome > best_score:
                # 这是最优的移动
                best_moves = [possible_move]
                best_score = our_best_outcome
                # 如果当前玩家是黑色，更新最佳黑色分数
                if game_state.next_player == Player.black:
                    best_black = best_score
                # 如果当前玩家是白色，更新最佳白色分数
                elif game_state.next_player == Player.white:
                    best_white = best_score
            # 如果我们的结果与最佳分数相同，将移动添加到最佳移动列表中
            elif our_best_outcome == best_score:
                # 这是最优的移动
                best_moves.append(possible_move)
        # 随机选择最佳移动列表中的一个移动
        return random.choice(best_moves)