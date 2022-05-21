import time

import dijkstar
from scipy.spatial import KDTree

import algorithms


class RrtAlgorithm:
    def __init__(self, x_range: [], y_range: [], collision_array_yx: []):
        # requirements
        self.__x_range = x_range  # = [x_min, x_max]
        self.__y_range = y_range  # = [y_min, y_max]
        self.__collision_array = collision_array_yx  # [y][x] = 0 to 255
        self.__edge_graph = dijkstar.Graph()  # for calculations
        # result
        self.vertex_array = []  # [index] = [y, x]
        self.edge_array = []  # [index] = [(y,x), (y,x)]
        # solution
        self.calculation_time = 0
        self.solution_vertex_array = []  # [index] = [y, x]

    def __append_vertex(self, index: int, vertex: []):
        self.vertex_array.append(vertex)
        self.__edge_graph.add_node(index)

    def __append_vertex_and_edge(self, new_index: int, new_vertex: [], near_index: int, near_vertex):
        self.__append_vertex(index=new_index, vertex=new_vertex)
        self.edge_array.append((new_vertex, near_vertex))
        # bidirectional edge
        distance = round(algorithms.calc_distance(new_vertex, near_vertex))
        self.__edge_graph.add_edge(new_index, near_index, distance)
        self.__edge_graph.add_edge(near_index, new_index, distance)

    def __result_interpretation(self, path_info, elapsed_time):
        print('[RRT] Calculation Time: {}sec'.format(elapsed_time))
        self.calculation_time = elapsed_time
        if path_info:
            for node_index in path_info.nodes:
                self.solution_vertex_array.append(self.vertex_array[node_index])
            print('[RRT] Path Nodes: {}'.format(len(self.solution_vertex_array)))

    def execute(self, c_init: [], c_goal: [], max_range: int, max_time: int):
        print('[RRT] c_init[x={init[1]},y={init[0]}], c_goal[x={goal[1]},y={goal[0]}], range={r}, time={t}sec'
              .format(init=c_init, goal=c_goal, r=max_range, t=max_time))
        start_time = time.time()
        # add init config
        c_new = c_init
        new_vertex_index = len(self.vertex_array)
        self.__append_vertex(index=new_vertex_index, vertex=c_new)

        while not max_time_elapsed(start_time, max_time):
            # check if goal reached
            if goal_reached(self.__collision_array, c_new, c_goal, max_range):
                goal_vertex_index = len(self.vertex_array)
                self.__append_vertex_and_edge(new_index=goal_vertex_index, new_vertex=c_goal,
                                              near_index=new_vertex_index, near_vertex=c_new)
                try:
                    shortest_path = dijkstar.find_path(graph=self.__edge_graph, s=0, d=goal_vertex_index)
                except dijkstar.algorithm.NoPathError:
                    shortest_path = None
                end_time = time.time()
                self.__result_interpretation(path_info=shortest_path, elapsed_time=end_time - start_time)
                break
            # new temporary random point
            c_rand = algorithms.random_vertex_yx(x_range=self.__x_range, y_range=self.__y_range)
            if not algorithms.vertex_without_collision(collision_array_yx=self.__collision_array, vertex_yx=c_rand):
                continue
            # new point from nearest neighbour
            near_vertex_index = nearest_vertex_index(vertex_array_yx=self.vertex_array, vertex_yx=c_rand)
            c_near = self.vertex_array[near_vertex_index]
            c_new = vertex_in_range(start_vertex_yx=c_near, end_vertex_yx=c_rand, max_range=max_range)
            new_vertex_index = len(self.vertex_array)
            if algorithms.edge_without_collision(self.__collision_array, (c_near, c_new)):
                self.__append_vertex_and_edge(new_index=new_vertex_index, new_vertex=c_new,
                                              near_index=near_vertex_index, near_vertex=c_near)


def max_time_elapsed(start_time, max_time) -> bool:
    return time.time() - start_time > max_time


def goal_reached(collision_array_yx: [], c_new: [], c_goal: [], max_range: int) -> bool:
    return (algorithms.calc_distance(c_new, c_goal) < max_range) \
           and algorithms.edge_without_collision(collision_array_yx, [c_new, c_goal])


def nearest_vertex_index(vertex_array_yx, vertex_yx) -> int:
    kd_tree = KDTree(vertex_array_yx)
    result = kd_tree.query(vertex_yx)
    return result[1]


def vertex_in_range(start_vertex_yx, end_vertex_yx, max_range) -> []:
    start_to_end_distance = algorithms.calc_distance(start_vertex_yx, end_vertex_yx)
    if start_to_end_distance <= max_range:
        return end_vertex_yx
    return algorithms.calc_point_between(start_vertex_yx, end_vertex_yx, max_range, start_to_end_distance)
