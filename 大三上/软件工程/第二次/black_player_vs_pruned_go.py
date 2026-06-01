""" 剪枝算法, 玩家下黑子 """
from six.moves import input

from dlgo import goboard_fast as goboard
from dlgo import gotypes
from dlgo import minimax
from dlgo.utils import print_board, print_move, point_from_coords

# 定义棋盘大小
BOARD_SIZE = 5


# 计算黑白棋子数量差
def capture_diff(game_state):
    black_stones = 0
    white_stones = 0
    # 遍历棋盘
    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            p = gotypes.Point(r, c)
            color = game_state.board.get(p)
            # 统计黑子和白子的数量
            if color == gotypes.Player.black:
                black_stones += 1
            elif color == gotypes.Player.white:
                white_stones += 1
    # 计算黑白棋子数量差
    diff = black_stones - white_stones
    # 如果轮到黑子下，返回差值，否则返回相反数
    if game_state.next_player == gotypes.Player.black:
        return diff
    return -1 * diff


# 主函数
def main():
    # 创建新游戏
    game = goboard.GameState.new_game(BOARD_SIZE)
    # 创建AI
    bot = minimax.AlphaBetaAgent(3, capture_diff)

    # 游戏未结束，继续循环
    while not game.is_over():
        # 打印棋盘
        print_board(game.board)
        # 如果轮到白子下，等待用户输入
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        # 否则，AI选择下一步
        else:
            move = bot.select_move(game)
        # 打印下一步
        print_move(game.next_player, move)
        # 应用下一步
        game = game.apply_move(move)


if __name__ == '__main__':
    main()
