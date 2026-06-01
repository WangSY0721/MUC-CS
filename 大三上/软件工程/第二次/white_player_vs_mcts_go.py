""" MCTS算法, 玩家下白子 """
from six.moves import input

from dlgo import goboard_fast as goboard
from dlgo import gotypes
from dlgo import mcts
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
    # 创建MCTS智能体
    bot = mcts.MCTSAgent(500, temperature=1.4)

    # 游戏未结束时循环
    while not game.is_over():
        # 打印棋盘
        print_board(game.board)
        # 如果轮到黑子下，等待用户输入
        if game.next_player == gotypes.Player.white:
            human_move = input('-- ')
            # 将用户输入的坐标转换为棋子位置
            point = point_from_coords(human_move.strip())
            # 创建用户下棋的Move对象
            move = goboard.Move.play(point)
        # 否则，让智能体选择下棋
        else:
            move = bot.select_move(game)
        # 打印下棋信息
        print_move(game.next_player, move)
        # 应用下棋
        game = game.apply_move(move)


if __name__ == '__main__':
    main()
