import random
import time
from itertools import repeat
from multiprocessing import Pool

from dijkstar import Graph, find_path
from scipy.spatial import KDTree

from collisionspace import Collisionspace
from configspace_view import ConfigspaceView
from utils import open_greyscale_bmp, GREYSCALE_BLACK, greyscale_is_not_black


class Configspace:  # shows the way of the robot the algorithm
    def __init__(self, app_page, robot_name: str, collisionspace: Collisionspace):
        robot_bmp = open_greyscale_bmp(robot_name)
        self.__view = ConfigspaceView(app_page, robot_bmp, collisionspace.collision_image)
        self.__min_x = round(robot_bmp.width / 2)
        self.__max_x = collisionspace.collision_image.width - round(robot_bmp.width / 2)
        self.__min_y = round(robot_bmp.height / 2)
        self.__max_y = collisionspace.collision_image.height - round(robot_bmp.height / 2)

        self.__init_config_yx = []  # position of the start Image
        self.__goal_config_yx = []  # position of the goal Image

        self.__collision_array_yx = collisionspace.collision_array
        self.__edge_graph = Graph()

        self.__algorithm_time = 0
        self.__solution_path_length = 0
        self.solution_pixel_yx = []  # array of Waypoints

    def __append_rrt_algorithm_edge(self, new_index: int, new_vertex: [], start_index: int, start_point: []):
        self.__edge_graph.add_node(new_index)
        # bidirectional edge
        distance = round(calc_distance(new_vertex, start_point))
        self.__edge_graph.add_edge(new_index, start_index, distance)
        self.__edge_graph.add_edge(start_index, new_index, distance)
        # draw on view
        self.__view.draw_line_yx(new_vertex, start_point, 'orange')

    def __append_sprm_algorithm_edge(self, index_tuple: [], vertex_list_yx: []):
        vertex0 = vertex_list_yx[index_tuple[0]]
        vertex1 = vertex_list_yx[index_tuple[1]]
        # bidirectional edge
        distance = round(calc_distance(vertex0, vertex1))
        self.__edge_graph.add_edge(index_tuple[0], index_tuple[1], distance)
        self.__edge_graph.add_edge(index_tuple[1], index_tuple[0], distance)
        self.__view.draw_line_yx(vertex0, vertex1, 'orange')

    def __draw_configuration_state(self):
        self.__view.reset()
        if self.__init_config_yx:
            self.__view.draw_point(self.__init_config_yx[1], self.__init_config_yx[0], 'green')
        if self.__goal_config_yx:
            self.__view.draw_point(self.__goal_config_yx[1], self.__goal_config_yx[0], 'red')

    def __convert_solution_path(self, path, vertex_list_yx) -> None:
        if not path:
            return
        self.__solution_path_length = len(path)
        start_vertex_yx = vertex_list_yx[0]
        self.solution_pixel_yx.append(start_vertex_yx)
        self.__view.draw_point(start_vertex_yx[1], start_vertex_yx[0], 'green')
        for vertex_index in path.nodes:
            if vertex_index == 0:
                continue
            next_vertex_yx = vertex_list_yx[vertex_index]
            self.__view.draw_point(next_vertex_yx[1], next_vertex_yx[0], 'purple')
            self.__view.draw_line_yx(start_vertex_yx, next_vertex_yx, 'red')
            self.solution_pixel_yx.extend(calc_all_points_between_xy(start_vertex_yx, next_vertex_yx))
            start_vertex_yx = next_vertex_yx
        self.__view.draw_point(start_vertex_yx[1], start_vertex_yx[0], 'red')
        self.__print_solution_summary()

    def __print_solution_summary(self):
        print("Solution Summary: Path Length = {} with Algorithm Time = {}"
              .format(self.__solution_path_length, self.__algorithm_time))

    def __reset_solution(self):
        self.solution_pixel_yx = []
        self.__edge_graph = Graph()
        self.__algorithm_time = 0
        self.__solution_path_length = 0
        self.__view.reset()

    def reset(self) -> None:
        self.__init_config_yx = []
        self.__goal_config_yx = []
        self.__reset_solution()
        self.__view.reset()

    def set_init_config(self, x, y):
        self.__init_config_yx = [y, x]
        self.__draw_configuration_state()

    def set_goal_config(self, x, y):
        self.__goal_config_yx = [y, x]
        self.__draw_configuration_state()

    def execute_SPRM_algorithm(self) -> None:
        # input parameter
        distance_r = 90
        point_samples_n = round(self.__collision_array_yx.shape[0] * self.__collision_array_yx.shape[1] / 800)
        print('Executing sPRM: c_init[x={init[1]},y={init[0]}], c_goal[x={goal[1]},y={goal[0]}], r={r}, n={n}'
              .format(init=self.__init_config_yx, goal=self.__goal_config_yx, r=distance_r, n=point_samples_n))
        # reset data
        self.__reset_solution()
        # add configuration to vertex structure
        self.__edge_graph.add_node(0)
        self.__edge_graph.add_node(1)
        vertex_list_yx = [self.__init_config_yx, self.__goal_config_yx]

        # calculate n free samples
        for i in range(2, point_samples_n + 2):
            while True:
                free_sample_yx = random_vertex_yx(self.__min_x, self.__max_x, self.__min_y, self.__max_y)
                if sample_is_valid(self.__collision_array_yx, free_sample_yx):
                    self.__edge_graph.add_node(i)
                    vertex_list_yx.append(free_sample_yx)
                    break

        for point_index_tuple in tuples_under_distance(self.__collision_array_yx, vertex_list_yx, distance_r):
            self.__append_sprm_algorithm_edge(index_tuple=point_index_tuple, vertex_list_yx=vertex_list_yx)

        for i in vertex_list_yx:
            self.__view.draw_point(i[1], i[0], 'blue')
        path = find_path(self.__edge_graph, 0, 1)
        # draw solution
        self.__convert_solution_path(path, vertex_list_yx)

    def execute_RRT_algorithm(self) -> None:
        max_range = 250
        max_time = 10  # 10 seconds
        print('Executing RRT: c_init[x={init[1]},y={init[0]}], c_goal[x={goal[1]},y={goal[0]}], range={r}, time={n}sec'
              .format(init=self.__init_config_yx, goal=self.__goal_config_yx, r=max_range, n=max_time))
        self.__reset_solution()
        self.__edge_graph.add_node(0)
        vertex_list_yx = [self.__init_config_yx]
        path = None
        start_time = time.time()
        while not max_time_elapsed(start_time, max_time):
            rand_vertex = random_vertex_yx(self.__min_x, self.__max_x, self.__min_y, self.__max_y)
            if not sample_is_valid(self.__collision_array_yx, rand_vertex):
                continue
            near_vertex_index = nearest_vertex_yx(vertex_list_yx, rand_vertex)
            near_vertex = vertex_list_yx[near_vertex_index]
            new_vertex = get_vertex_in_range(near_vertex, rand_vertex, max_range)
            new_vertex_index = len(vertex_list_yx)
            # rand_vertex if in range
            if edge_without_collision(self.__collision_array_yx, (near_vertex, new_vertex)):
                vertex_list_yx.append(new_vertex)
                self.__append_rrt_algorithm_edge(
                    new_index=new_vertex_index,
                    new_vertex=new_vertex,
                    start_index=near_vertex_index,
                    start_point=near_vertex)

                if (calc_distance(new_vertex, self.__goal_config_yx) < max_range) \
                        and edge_without_collision(self.__collision_array_yx, [self.__goal_config_yx, new_vertex]):
                    goal_index = len(vertex_list_yx)
                    vertex_list_yx.append(self.__goal_config_yx)
                    self.__append_rrt_algorithm_edge(
                        new_index=goal_index,
                        new_vertex=self.__goal_config_yx,
                        start_index=new_vertex_index,
                        start_point=new_vertex)
                    path = find_path(self.__edge_graph, 0, len(vertex_list_yx) - 1)
                    break
        # draw solution
        for i in vertex_list_yx:
            self.__view.draw_point(i[1], i[0], 'blue')
        self.__convert_solution_path(path, vertex_list_yx)


def nearest_vertex_yx(vertex_list_yx, rand_vertex) -> int:
    kd_tree = KDTree(vertex_list_yx)
    result = kd_tree.query(rand_vertex)
    return result[1]


def get_vertex_in_range(start_vertex_yx, end_vertex_yx, max_range) -> []:
    if calc_distance(start_vertex_yx, end_vertex_yx) <= max_range:
        return end_vertex_yx
    return calc_point_between(start_vertex_yx, end_vertex_yx, 1, max_range)


def max_time_elapsed(start_time, max_time) -> bool:
    elapsed_time = time.time() - start_time
    return elapsed_time > max_time


def sample_is_valid(collision_array_yx, vertex_yx: []):
    return greyscale_is_not_black(collision_array_yx[vertex_yx[0]][vertex_yx[1]])


def random_vertex_yx(min_width: int, max_width: int, min_height: int, max_height: int) -> []:
    x = random.randrange(min_width, max_width)
    y = random.randrange(min_height, max_height)
    return [y, x]


def calc_distance(point1, point2) -> float:
    return ((point1[0] - point2[0]) ** 2 +
            (point1[1] - point2[1]) ** 2) ** 0.5


def tuples_under_distance(collision_array_yx, points_yx: [], distance) -> []:
    points_neighbour_tuples = []
    for point_index in range(len(points_yx) - 1):
        for next_point_index in range(point_index + 1, len(points_yx)):
            if calc_distance(points_yx[point_index], points_yx[next_point_index]) < distance:
                points_neighbour_tuples.append([point_index, next_point_index])
    with Pool(4) as p:
        valid_edge = p.starmap(
            edge_without_collision,
            zip(repeat(collision_array_yx), repeat(points_yx), points_neighbour_tuples))
    return filter(None, valid_edge)


def edge_without_collision(collision_array_yx, points_yx_tuple: [], points_index_tuple: [] = (0, 1)):
    start_yx = points_yx_tuple[points_index_tuple[0]]
    goal_yx = points_yx_tuple[points_index_tuple[1]]
    step_range = round(calc_distance(start_yx, goal_yx))
    for step in range(1, step_range):
        point_yx = calc_point_between(start_yx, goal_yx, step, step_range)
        if collision_array_yx[point_yx[0], point_yx[1]] == GREYSCALE_BLACK:
            return None
    return points_index_tuple


def calc_point_between(start_yx, goal_yx, step, step_range) -> []:
    delta_x = round(step * float(goal_yx[1] - start_yx[1]) / float(step_range))
    delta_y = round(step * float(goal_yx[0] - start_yx[0]) / float(step_range))
    new_x = start_yx[1] + delta_x
    new_y = start_yx[0] + delta_y
    return [new_y, new_x]


def calc_all_points_between_xy(start_yx, goal_yx):
    result = []
    step_range = round(calc_distance(start_yx, goal_yx))
    for step in range(1, step_range):
        result.append(calc_point_between(start_yx, goal_yx, step, step_range))
    return result
