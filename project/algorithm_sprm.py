import multiprocessing
import time
from itertools import repeat

import dijkstar

import algorithms


class SprmAlgorithm:
    def __init__(self, x_range: [], y_range: [], collision_array_yx):
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
        self.path_length = 0
        self.solution_vertex_array = []  # [index] = [y, x]

    def __append_vertex(self, index: int, vertex: []):
        self.vertex_array.append(vertex)
        self.__edge_graph.add_node(index)

    def __append_edge(self, index_tuple: []):
        vertex0 = self.vertex_array[index_tuple[0]]
        vertex1 = self.vertex_array[index_tuple[1]]
        self.edge_array.append((vertex0, vertex1))
        # bidirectional edge
        distance = round(algorithms.calc_distance(vertex0, vertex1))
        self.__edge_graph.add_edge(index_tuple[0], index_tuple[1], distance)
        self.__edge_graph.add_edge(index_tuple[1], index_tuple[0], distance)

    def __result_interpretation(self, path_info, elapsed_time):
        print('[sPRM] Calculation Time: {}sec'.format(elapsed_time))
        self.calculation_time = elapsed_time
        if path_info:
            self.path_length = path_info.total_cost
            for node_index in path_info.nodes:
                self.solution_vertex_array.append(self.vertex_array[node_index])
            print('[sPRM] Path Nodes: {}'.format(len(self.solution_vertex_array)))
        else:
            print('[sPRM] No path found!')

    def execute(self, c_init: [], c_goal: [], r: int, n: int):
        # setup
        print('[sPRM] Executing: c_init[x={init[1]},y={init[0]}], c_goal[x={goal[1]},y={goal[0]}], r={r}, n={n}'
              .format(init=c_init, goal=c_goal, r=r, n=n))
        start_time = time.time()
        # init configuration
        self.__append_vertex(index=0, vertex=c_init)
        self.__append_vertex(index=1, vertex=c_goal)
        # calculate free samples
        for sample_index in range(2, n + 2):
            while True:
                c_free_sample = algorithms.random_vertex_yx(x_range=self.__x_range, y_range=self.__y_range)
                if algorithms.vertex_without_collision(collision_array_yx=self.__collision_array,
                                                       vertex_yx=c_free_sample):
                    self.__append_vertex(index=sample_index, vertex=c_free_sample)
                    break
        # calculate valid edges through neighbours
        # TODO implement it more like the pseudo code
        # for vertex_index in range(0, len(self.vertex_array)):
        #     neighbour_tuples = neighbour_index_tuples(vertex_index, self.vertex_array, r)
        #     for index_tuple in tuples_without_collision(self.__collision_array, self.vertex_array, neighbour_tuples):
        #         self.__append_edge(index_tuple=index_tuple)
        for point_index_tuple in tuples_under_distance(self.__collision_array, self.vertex_array, r):
            self.__append_edge(index_tuple=point_index_tuple)
        # calculate the shortest path
        try:
            shortest_path = dijkstar.find_path(graph=self.__edge_graph, s=0, d=1)
        except dijkstar.algorithm.NoPathError:
            shortest_path = None
        # teardown
        end_time = time.time()
        self.__result_interpretation(path_info=shortest_path, elapsed_time=end_time - start_time)


def neighbour_index_tuples(current_index: int, vertex_array: [], max_distance: int) -> []:
    neighbour_indices_tuples = []
    # checks all vertices until current index
    for index in range(0, current_index):
        if algorithms.calc_distance(vertex_array[current_index], vertex_array[index]) <= max_distance:
            neighbour_indices_tuples.append((current_index, index))
    # skip current index and checks all vertices after current index without repeated if statement
    for index in range(current_index + 1, len(vertex_array)):
        if algorithms.calc_distance(vertex_array[current_index], vertex_array[index]) <= max_distance:
            neighbour_indices_tuples.append((current_index, index))
    return neighbour_indices_tuples


def tuples_without_collision(collision_array_yx: [], vertex_array_yx: [], neighbour_tuples: []) -> []:
    with multiprocessing.Pool(4) as p:  # 4 threads
        valid_tuples = p.starmap(algorithms.edge_without_collision,  # runnable task
                                 zip(repeat(collision_array_yx),  # task inputs
                                     repeat(vertex_array_yx),
                                     neighbour_tuples))
    return filter(None, valid_tuples)  # exclude None entries


def tuples_under_distance(collision_array_yx, points_yx: [], distance) -> []:
    points_neighbour_tuples = []
    for point_index in range(len(points_yx) - 1):
        for next_point_index in range(point_index + 1, len(points_yx)):
            if algorithms.calc_distance(points_yx[point_index], points_yx[next_point_index]) < distance:
                points_neighbour_tuples.append([point_index, next_point_index])
    with multiprocessing.Pool(4) as p:
        valid_edge = p.starmap(
            algorithms.edge_without_collision,
            zip(repeat(collision_array_yx), repeat(points_yx), points_neighbour_tuples))
    return filter(None, valid_edge)
