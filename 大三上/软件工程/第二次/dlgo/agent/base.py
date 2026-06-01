__all__ = [
    'Agent',  # 公开Agent类，供外部使用
]


# tag::agent[]
class Agent():
    """围棋机器人接口类，用于定义围棋游戏中的决策行为。"""

    def select_move(self, game_state):
        """
        选择下一步的棋步。
        该方法需要根据当前的游戏状态作出决策。

        参数:
        game_state (object): 当前的游戏状态，包含棋盘信息和其他相关数据。

        返回:
        raise NotImplementedError(): 必须在子类中实现此方法。
        """
        raise NotImplementedError()

    # end::agent[]

    def diagnostics(self):
        """
        返回诊断信息，供调试和测试使用。

        返回:
        dict: 诊断信息的字典，默认为空字典。
        """
        return {}
