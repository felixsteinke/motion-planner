from algorithm_rrt import RrtAlgorithm
from algorithm_sprm import SprmAlgorithm
from collisionspace import Collisionspace
from configspace_view import ConfigspaceView
from project import algorithms
from utils import open_greyscale_bmp
from benchmark_data import BenchmarkData


class Configspace:  # shows the way of the robot the algorithm
    def __init__(self, app_page, robot_name: str, collisionspace: Collisionspace):
        robot_bmp = open_greyscale_bmp(robot_name)
        self.__view = ConfigspaceView(app_page, robot_bmp, collisionspace.collision_image)
        self.__min_x = round(robot_bmp.width / 2)
        self.__max_x = collisionspace.collision_image.width - round(robot_bmp.width / 2)
        self.__min_y = round(robot_bmp.height / 2)
        self.__max_y = collisionspace.collision_image.height - round(robot_bmp.height / 2)
        self.__collision_array_yx = collisionspace.collision_array

        self.__init_config_yx = []  # position of the start Image
        self.__goal_config_yx = []  # position of the goal Image

        self.solution_pixels_yx = []  # array of Waypoints

    def __draw_configuration_state(self):
        self.__view.reset()
        if self.__init_config_yx:
            self.__view.draw_point(self.__init_config_yx[1], self.__init_config_yx[0], 'green')
        if self.__goal_config_yx:
            self.__view.draw_point(self.__goal_config_yx[1], self.__goal_config_yx[0], 'red')

    def __draw_solution(self, vertex_samples: [], edge_samples: [], solution_path: []):
        # draw all vertex samples
        for vertex_yx in vertex_samples:
            self.__view.draw_point(vertex_yx[1], vertex_yx[0], 'blue')
        # draw all edge samples
        for edge_yx in edge_samples:
            self.__view.draw_line_yx(edge_yx[0], edge_yx[1], 'blue')
        # draw init config
        if solution_path:
            start_vertex_yx = solution_path[0]
            self.__view.draw_point(start_vertex_yx[1], start_vertex_yx[0], 'green')
            # draw path
            for i in range(1, len(solution_path) - 1):
                end_vertex_yx = solution_path[i]
                self.__view.draw_point(end_vertex_yx[1], end_vertex_yx[0], 'yellow')
                self.__view.draw_line_yx(start_vertex_yx, end_vertex_yx, 'red')
                start_vertex_yx = end_vertex_yx
            # draw goal config
            goal_vertex_yx = solution_path[len(solution_path) - 1]
            self.__view.draw_point(goal_vertex_yx[1], goal_vertex_yx[0], 'red')
            self.__view.draw_line_yx(start_vertex_yx, goal_vertex_yx, 'red')

    def __convert_solution_path(self, solution_vertex_array_yx: []) -> None:
        if solution_vertex_array_yx:
            start_vertex_yx = solution_vertex_array_yx[0]
            self.solution_pixels_yx.append(start_vertex_yx)
            for vertex_index in range(1, len(solution_vertex_array_yx)):
                next_vertex_yx = solution_vertex_array_yx[vertex_index]
                self.solution_pixels_yx.extend(calc_all_points_between_xy(start_vertex_yx, next_vertex_yx))
                start_vertex_yx = next_vertex_yx

    def __reset_solution(self):
        self.solution_pixels_yx = []
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

    def execute_sprm(self) -> None:
        self.__reset_solution()
        distance = 90
        samples = round(self.__collision_array_yx.shape[0] * self.__collision_array_yx.shape[1] / 800)
        sprm = SprmAlgorithm(x_range=[self.__min_x, self.__max_x], y_range=[self.__min_y, self.__max_y],
                             collision_array_yx=self.__collision_array_yx)
        sprm.execute(c_init=self.__init_config_yx, c_goal=self.__goal_config_yx, r=distance, n=samples)
        self.__draw_solution(vertex_samples=sprm.vertex_array, edge_samples=sprm.edge_array,
                             solution_path=sprm.solution_vertex_array)
        self.__convert_solution_path(sprm.solution_vertex_array)

    def execute_rrt(self) -> None:
        self.__reset_solution()
        max_range = 90
        max_time = 100  # 10 seconds
        rrt = RrtAlgorithm(x_range=[self.__min_x, self.__max_x], y_range=[self.__min_y, self.__max_y],
                           collision_array_yx=self.__collision_array_yx)
        rrt.execute(c_init=self.__init_config_yx, c_goal=self.__goal_config_yx,
                    max_range=max_range, max_time=max_time)
        self.__draw_solution(vertex_samples=rrt.vertex_array, edge_samples=rrt.edge_array,
                             solution_path=rrt.solution_vertex_array)
        self.__convert_solution_path(rrt.solution_vertex_array)

    def execute_benchmark(self) -> None:
        # Setup
        benchmark_runs = 10
        print('[BENCHMARK] Executing {} runs.'.format(benchmark_runs))
        # sPRM
        sprm_distance = 90
        sprm_samples = round(self.__collision_array_yx.shape[0] * self.__collision_array_yx.shape[1] / 800)
        sprm_metrics = BenchmarkData(name='sPRM', runs=benchmark_runs)
        for i in range(0, benchmark_runs):
            sprm = SprmAlgorithm(x_range=[self.__min_x, self.__max_x], y_range=[self.__min_y, self.__max_y],
                                 collision_array_yx=self.__collision_array_yx)
            sprm.execute(c_init=self.__init_config_yx, c_goal=self.__goal_config_yx,
                         r=sprm_distance, n=sprm_samples)
            sprm_metrics.add_run_data(vertex_array=sprm.vertex_array, edge_array=sprm.edge_array,
                                      calc_time=sprm.calculation_time, solution_array=sprm.solution_vertex_array,
                                      solution_length=sprm.path_length)
        # RRT
        rrt_max_range = 90
        rrt_max_time = 100  # 10 seconds
        rrt_metrics = BenchmarkData(name='RRT', runs=benchmark_runs)
        for i in range(0, benchmark_runs):
            rrt = RrtAlgorithm(x_range=[self.__min_x, self.__max_x], y_range=[self.__min_y, self.__max_y],
                               collision_array_yx=self.__collision_array_yx)
            rrt.execute(c_init=self.__init_config_yx, c_goal=self.__goal_config_yx,
                        max_range=rrt_max_range, max_time=rrt_max_time)
            rrt_metrics.add_run_data(vertex_array=rrt.vertex_array, edge_array=rrt.edge_array,
                                     calc_time=rrt.calculation_time, solution_array=rrt.solution_vertex_array,
                                     solution_length=rrt.path_length)
        # BENCHMARK
        sprm_result = sprm_metrics.get_result()
        rrt_result = rrt_metrics.get_result()
        print(sprm_result)
        print(rrt_result)


def calc_all_points_between_xy(start_yx, goal_yx):
    result = []
    step_range = round(algorithms.calc_distance(start_yx, goal_yx))
    for step in range(1, step_range):
        result.append(algorithms.calc_point_between(start_yx, goal_yx, step, step_range))
    return result
