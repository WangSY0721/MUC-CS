from ..gotypes import Point

__all__ = [
    'is_point_an_eye',
]


def is_point_an_eye(board, point, color):
    # 判断指定位置的点是否为空，如果该点已有棋子（非空），则返回 False
    if board.get(point) is not None:
        return False

    # 遍历该点周围的所有邻居点，检查邻居点的颜色是否是友方棋子
    for neighbor in board.neighbors(point):
        neighbor_color = board.get(neighbor)
        # 如果邻居点的颜色不是当前玩家的颜色，则返回 False
        if neighbor_color != color:
            return False

    # 统计友方控制的角落数
    friendly_corners = 0
    # 统计越界的角落数（即超出棋盘的角落）
    off_board_corners = 0
    # 定义四个角落的坐标，相对于当前点的位置
    corners = [
        Point(point.row - 1, point.col - 1),  # 左上角
        Point(point.row - 1, point.col + 1),  # 右上角
        Point(point.row + 1, point.col - 1),  # 左下角
        Point(point.row + 1, point.col + 1),  # 右下角
    ]

    # 遍历四个角落，判断是否控制这些角落
    for corner in corners:
        # 判断角落是否在棋盘范围内
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            # 如果该角落是友方棋子，则增加友方控制的角落数量
            if corner_color == color:
                friendly_corners += 1
        else:
            # 如果该角落超出棋盘范围，则增加越界角落数量
            off_board_corners += 1

    # 如果有越界角落，判断友方角落和越界角落的总数是否为 4
    if off_board_corners > 0:
        # 如果点在棋盘的边缘或角落，友方角落加越界角落必须为 4
        return off_board_corners + friendly_corners == 4

    # 如果没有越界角落，判断友方角落是否至少有 3 个
    # 如果点位于棋盘的中央，必须控制至少 3 个角落
    return friendly_corners >= 3
