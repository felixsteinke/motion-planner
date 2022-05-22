import random

from utils import GREYSCALE_BLACK, is_not_black


def calc_distance(point1, point2) -> float:
    return ((point1[0] - point2[0]) ** 2 +
            (point1[1] - point2[1]) ** 2) ** 0.5


def random_vertex_yx(x_range: [], y_range: []) -> []:  # = [y, x]
    return [
        random.randrange(y_range[0], y_range[1]),
        random.randrange(x_range[0], x_range[1])
    ]


def vertex_without_collision(collision_array_yx: [], vertex_yx: []) -> bool:
    return is_not_black(greyscale_value=collision_array_yx[vertex_yx[0]][vertex_yx[1]])


def edge_without_collision(collision_array_yx, vertex_array: [], index_tuple: [] = (0, 1)):
    start_yx = vertex_array[index_tuple[0]]
    goal_yx = vertex_array[index_tuple[1]]
    max_distance = round(calc_distance(start_yx, goal_yx))
    for partial_distance in range(1, max_distance):
        point_yx = calc_point_between(start_yx, goal_yx, partial_distance, max_distance)
        if collision_array_yx[point_yx[0], point_yx[1]] == GREYSCALE_BLACK:
            return None
    return index_tuple


def calc_point_between(start_yx, goal_yx, start_to_new_distance, start_to_goal_distance: float) -> []:
    delta_x = round(start_to_new_distance * float(goal_yx[1] - start_yx[1]) / start_to_goal_distance)
    delta_y = round(start_to_new_distance * float(goal_yx[0] - start_yx[0]) / start_to_goal_distance)
    new_x = start_yx[1] + delta_x
    new_y = start_yx[0] + delta_y
    return [new_y, new_x]
