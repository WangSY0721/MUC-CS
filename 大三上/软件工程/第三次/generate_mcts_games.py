# 功能：用MCT算法生成棋局
# 6-5 用于生成蒙特卡洛树搜索棋局编码数据的模块的导入语句
import argparse
import numpy as np

from dlgo.encoders import get_encoder_by_name
from dlgo import goboard_fast as goboard
from dlgo import mcts
from dlgo.utils import print_board, print_move



# 生成游戏数据的函数
# 6-6 为本章生成MCT棋局
def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []  # <1>boards变量存储编码后的棋盘状态，moves变量存放编码后的落子动作

    encoder = get_encoder_by_name('oneplane', board_size)  # <2>用给定的棋盘尺寸，按名称初始化一个OnePlaneEncoder实例

    game = goboard.GameState.new_game(board_size)  # <3>一个尺寸为board_size的新棋局被实例化好了

    bot = mcts.MCTSAgent(rounds, temperature)  # <4>指定推演回合数和温度参数，创建一个蒙特卡洛树搜索代理作为我们的机器人

    num_moves = 0
    while not game.is_over():
        print_board(game.board)
        move = bot.select_move(game)  # <5>机器人选择下一步动作
        if move.is_play:
            boards.append(encoder.encode(game))  # <6>把编码的棋盘状态添加到boards数组中

            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            moves.append(move_one_hot)  # <7>把下一步动作进行独热编码，并添加到moves数组中

        print_move(game.next_player, move)
        game = game.apply_move(move)  # <8>之后把机器人的下一步动作执行到棋盘上
        num_moves += 1
        if num_moves > max_moves:  # <9>继续下一步动作，直至达到最大动作数量限制
            break

    return np.array(boards), np.array(moves)



# 定义一个main方法来运行几盘棋
# 为本章生成MCTS棋局的主函数
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', '-b', type=int, default=9)
    parser.add_argument('--rounds', '-r', type=int, default=1000)
    parser.add_argument('--temperature', '-t', type=float, default=0.8)
    parser.add_argument('--max-moves', '-m', type=int, default=60,
                        help='Max moves per game.')
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--board-out')
    parser.add_argument('--move-out')

    args = parser.parse_args()  # <1>这个应用允许用命令行参数进行自定义设置
    xs = []
    ys = []

    for i in range(args.num_games):
        print('Generating game %d/%d...' % (i + 1, args.num_games))
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)  # <2>根据给定棋局数量来生成相应的棋局数据
        xs.append(x)
        ys.append(y)

    x = np.concatenate(xs)  # <3>当所有棋局都生成之后，为棋局添加相应的特征与标签
    y = np.concatenate(ys)

    np.save(args.board_out, x)  # <4>根据命令行参数所指定的选项，将特征与标签数据存放到不同的文件中
    np.save(args.move_out, y)


if __name__ == '__main__':
    main()

