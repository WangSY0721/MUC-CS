from ..gotypes import Point

__all__ = [
    'is_point_an_eye',
]


def is_point_an_eye(board, point, color):
    # 判断指定位置的点是否为空，如果该点已有棋子（非空），则不是眼，直接返回 False
    if board.get(point) is not None:
        return False

        # 遍历该点周围的所有邻居点
    for neighbor in point.neighbors():
        # 如果邻居点在棋盘上，则判断邻居点的颜色是否与当前颜色一致
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            # 如果邻居点的颜色不是当前玩家的颜色，则该点无法构成眼，返回 False
            if neighbor_color != color:
                return False

                # 初始化友方角落的数量为 0
    friendly_corners = 0
    # 初始化越界角落的数量为 0
    off_board_corners = 0
    # 定义四个角落位置，相对当前点的偏移量
    corners = [
        Point(point.row - 1, point.col - 1),  # 左上角
        Point(point.row - 1, point.col + 1),  # 右上角
        Point(point.row + 1, point.col - 1),  # 左下角
        Point(point.row + 1, point.col + 1),  # 右下角
    ]
    # 遍历四个角落位置
    for corner in corners:
        # 判断角落是否在棋盘范围内
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            # 如果角落是友方棋子，则增加友方角落的计数
            if corner_color == color:
                friendly_corners += 1
        else:
            # 如果角落超出棋盘范围，则增加越界角落的计数
            off_board_corners += 1

            # 如果有越界角落，判断友方角落和越界角落的总数是否为 4
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4  # 只要有越界角落，友方角落加越界角落必须为 4
    # 如果没有越界角落，判断友方角落是否至少有 3 个
    return friendly_corners >= 3  # 没有越界角落时，友方角落必须至少有 3 个
