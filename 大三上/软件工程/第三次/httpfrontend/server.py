# import sys
# import os
#
# # 将项目根目录添加到 sys.path
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(PROJECT_ROOT)
#
# import os
#
# from flask import Flask
# from flask import jsonify
# from flask import request
#
# from dlgo import agent
# from dlgo import goboard_fast as goboard
# from dlgo.utils import coords_from_point
# from dlgo.utils import point_from_coords
#
# __all__ = [
#     'get_web_app',
# ]
#
#
# def get_web_app(bot_map):
#     """Create a flask application for serving bot moves.
#
#     The bot_map maps from URL path fragments to Agent instances.
#
#     The /static path will return some static content (including the
#     jgoboard JS).
#
#     Clients can get the post move by POSTing json to
#     /select-move/<bot name>
#
#     Example:
#
#     >>> myagent = agent.naive.RandomBot()
#     >>> web_app = get_web_app({'random': myagent})
#     >>> web_app.run()
#
#     Returns: Flask application instance
#     """
#     here = os.path.dirname(__file__)
#     static_path = os.path.join(here, 'static')
#     app = Flask(__name__, static_folder=static_path, static_url_path='/static')
#
#     @app.route('/select-move/<bot_name>', methods=['POST'])
#     def select_move(bot_name):
#         content = request.json
#         board_size = content['board_size']
#         game_state = goboard.GameState.new_game(board_size)
#         # Replay the game up to this point.
#         for move in content['moves']:
#             if move == 'pass':
#                 next_move = goboard.Move.pass_turn()
#             elif move == 'resign':
#                 next_move = goboard.Move.resign()
#             else:
#                 next_move = goboard.Move.play(point_from_coords(move))
#             game_state = game_state.apply_move(next_move)
#         bot_agent = bot_map[bot_name]
#         bot_move = bot_agent.select_move(game_state)
#         if bot_move.is_pass:
#             bot_move_str = 'pass'
#         elif bot_move.is_resign:
#             bot_move_str = 'resign'
#         else:
#             bot_move_str = coords_from_point(bot_move.point)
#         return jsonify({
#             'bot_move': bot_move_str,
#             'diagnostics': bot_agent.diagnostics()
#         })
#
#     return app
#
#
# if __name__ == '__main__':
#     import h5py
#     from dlgo.encoders.oneplane import OnePlaneEncoder
#     from keras.models import load_model
#     from dlgo.agent.predict import DeepLearningAgent
#
#     # 模型文件路径
#     model_path = 'D:/王世屹/大学/计算机/软件工程/第三次/models/small_model_epoch_300.h5'
#
#     # 加载模型权重（直接加载整个文件）
#     print(f"Loading model from {model_path}...")
#     try:
#         model = load_model(model_path)  # 加载完整的 Keras 模型
#         print("Model loaded successfully.")
#     except Exception as e:
#         print(f"Error loading model: {e}")
#         raise
#
#     # 手动提供编码器信息
#     board_size = 19  # 棋盘大小是 19x19
#     encoder = OnePlaneEncoder((board_size, board_size))
#
#     # 创建 DeepLearningAgent
#     predict_agent = DeepLearningAgent(model, encoder)
#     print("Agent created successfully.")
#
#     # 定义路由映射
#     bot_map = {
#         'predict': predict_agent
#     }
#
#     # 创建 Flask 应用
#     app = get_web_app(bot_map)
#
#     # 启动服务
#     print("Starting Flask app...")
#     app.run(host='0.0.0.0', port=5000, debug=True)
#
#
#


import sys
import os
from flask import Flask, jsonify, request
from dlgo import agent
from dlgo import goboard_fast as goboard
from dlgo.utils import coords_from_point
from dlgo.utils import point_from_coords

# 将项目根目录添加到 sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

__all__ = [
    'get_web_app',
]


def get_web_app(bot_map):
    """Create a flask application for serving bot moves.

    The bot_map maps from URL path fragments to Agent instances.

    The /static path will return some static content (including the
    jgoboard JS).

    Clients can get the post move by POSTing json to
    /select-move/<bot name>

    Example:

    >>> myagent = agent.naive.RandomBot()
    >>> web_app = get_web_app({'random': myagent})
    >>> web_app.run()

    Returns: Flask application instance
    """
    here = os.path.dirname(__file__)
    static_path = os.path.join(here, 'static')
    app = Flask(__name__, static_folder=static_path, static_url_path='/static')

    @app.route('/select-move/<bot_name>', methods=['POST'])
    def select_move(bot_name):
        print(f"Received bot_name: {bot_name}")  # 打印 bot_name 以调试

        # 请求的数据
        content = request.json
        board_size = content['board_size']
        game_state = goboard.GameState.new_game(board_size)

        # 重播游戏直到当前步骤
        for move in content['moves']:
            if move == 'pass':
                next_move = goboard.Move.pass_turn()
            elif move == 'resign':
                next_move = goboard.Move.resign()
            else:
                next_move = goboard.Move.play(point_from_coords(move))
            game_state = game_state.apply_move(next_move)

        # 检查 bot_name 是否在 bot_map 中
        if bot_name in bot_map:
            bot_agent = bot_map[bot_name]
            bot_move = bot_agent.select_move(game_state)

            # 处理 bot 的动作
            if bot_move.is_pass:
                bot_move_str = 'pass'
            elif bot_move.is_resign:
                bot_move_str = 'resign'
            else:
                bot_move_str = coords_from_point(bot_move.point)

            return jsonify({
                'bot_move': bot_move_str,
                'diagnostics': bot_agent.diagnostics()
            })
        else:
            return jsonify({"error": f"Bot '{bot_name}' not found"}), 400  # 如果 bot_name 不在字典中，返回错误

    return app


if __name__ == '__main__':
    import h5py
    from dlgo.encoders.oneplane import OnePlaneEncoder
    from keras.models import load_model
    from dlgo.agent.predict import DeepLearningAgent

    # 模型文件路径
    model_path = 'D:/王世屹/大学/计算机/软件工程/第三次/models/small_model_epoch_300.h5'

    # 加载模型权重（直接加载整个文件）
    print(f"Loading model from {model_path}...")
    try:
        model = load_model(model_path)  # 加载完整的 Keras 模型
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

    # 手动提供编码器信息
    board_size = 19  # 棋盘大小是 19x19
    encoder = OnePlaneEncoder((board_size, board_size))

    # 创建 DeepLearningAgent
    predict_agent = DeepLearningAgent(model, encoder)
    print("Agent created successfully.")

    # 定义路由映射
    bot_map = {
        'predict': predict_agent  # 在字典中添加 'predict' 键，指向 DeepLearningAgent
    }

    # 打印 bot_map，确保它包含 'predict' 键
    print(f"bot_map: {bot_map}")

    # 创建 Flask 应用
    app = get_web_app(bot_map)

    # 启动服务
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
