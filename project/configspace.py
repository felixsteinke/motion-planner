import random
from itertools import repeat
from multiprocessing import Pool
from tkinter import *

from PIL import ImageTk
from dijkstar import Graph, find_path
from utils import open_greyscale_bmp
from collisionspace import Collisionspace


class Configspace:  # shows the way of the robot the algorithm

    def __init__(self, app_page, robot_name: str, collisionspace: Collisionspace):
        robot_bmp = open_greyscale_bmp(robot_name)
        real_max_width = collisionspace.collision_image.width
        real_max_height = collisionspace.collision_image.height
        self.min_width = robot_bmp.width
        self.max_width = real_max_width - robot_bmp.width
        self.min_height = robot_bmp.height
        self.max_height = real_max_height - robot_bmp.height
        self.collision_array = collisionspace.collision_array
        self.__calculator = ConfigspaceCalculator(real_max_width, real_max_height, robot_bmp)
        self.__view = ConfigspaceView(app_page, real_max_width, real_max_height, robot_bmp,
                                      collisionspace.collision_image)

        self.__init_config_xy = -1, -1  # position of the start Image
        self.__goal_config_xy = -1, -1  # position of the goal Image

        self.solutionPath = []  # array of Waypoints
        self.graph = Graph()

    def set_init_config(self, x, y):
        self.__init_config_xy = [x, y]

    def set_goal_config(self, x, y):
        self.__goal_config_xy = [x, y]

    def execute_SPRM_algorithm(self) -> None:
        self.graph.add_node(0)
        self.graph.add_node(1)
        points_list = [(self.__init_config_xy[1], self.__init_config_xy[0]),
                       (self.__goal_config_xy[1], self.__goal_config_xy[0])]
        points = 1000
        for i in range(2, points + 2):
            found_flag = True
            while found_flag:
                new_point = random_point_yx(self.min_width, self.max_width, self.min_height, self.max_height)
                if self.collision_array[new_point[0]][new_point[1]] > 1:
                    self.graph.add_node(i)
                    points_list.append(new_point)
                    found_flag = False
        for i in points_list:
            self.__view.draw_dot(i[1], i[0], 'blue')
        for point_tuple in tuples_under_distance(self.collision_array, points_list, 80):
            self.graph.add_edge(point_tuple[0], point_tuple[1],
                                round(calc_distance(points_list[point_tuple[0]], points_list[point_tuple[1]])))
            self.graph.add_edge(point_tuple[1], point_tuple[0],
                                round(calc_distance(points_list[point_tuple[1]], points_list[point_tuple[0]])))
            self.__view.draw_line(points_list[point_tuple[0]], points_list[point_tuple[1]], 'yellow')
        path = find_path(self.graph, 0, 1)
        last_point = points_list[0]
        self.__view.draw_path(path.nodes)
        self.__view.draw_dot(points_list[0][1], points_list[0][0], 'red')
        self.__view.draw_dot(points_list[1][1], points_list[1][0], 'green')


class ConfigspaceView:
    def __init__(self, frame, max_width: int, max_height: int, robot_bmp: Image, collision_image: Image):
        self.root_frame = frame
        self.canvas = Canvas(frame)  # Canvas for 2D graphics.
        self.robot_bmp = robot_bmp
        self.__style_canvas(collision_image)

    def __style_canvas(self, collision_image):
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.config(bd=0, width=collision_image.width, height=collision_image.height)  # bd = Border just
        collision_photo = ImageTk.PhotoImage(collision_image)
        self.canvas.create_image(0, 0, image=collision_photo, anchor=NW)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # placing the canvas on the second page
        self.__draw_border(collision_image.width, collision_image.height, self.robot_bmp)

    def __draw_border(self, max_x: int, max_y: int, robot_image):
        # Open: remove offset, canvas.config offset buggy (NOT MY COMMENT)
        # self.canvas.delete("all")  # deletes all drawings from the canvas
        offset_x = int(robot_image.width / 2)  # haf of the pixel of the robot png.
        offset_y = int(robot_image.height / 2)

        top_left_xy = [offset_x, offset_y]
        top_right_xy = [max_x - offset_x, offset_y]
        bottom_left_xy = [offset_x, max_y - offset_y]
        bottom_right_xy = [max_x - offset_x, max_y - offset_y]

        self.draw_line(top_left_xy, top_right_xy, 'red')
        self.draw_line(top_right_xy, bottom_right_xy, 'red')
        self.draw_line(bottom_right_xy, bottom_left_xy, 'red')
        self.draw_line(bottom_left_xy, top_left_xy, 'red')

    def __draw_line(self, start_x, start_y, goal_x, goal_y, color):
        self.canvas.create_line(start_x, start_y, goal_x, goal_y, fill=color)

    def draw_dot(self, center_x, center_y, color):
        radius = 5  # radius of the colored dot
        self.canvas.create_oval(center_x - radius,
                                center_y - radius,
                                center_x + radius,
                                center_y + radius,
                                fill=color)  # draw color

    def draw_path(self, points: []):
        for i in range(1, len(points)):  # iterate over points from solution-path
            start_point = points[i - 1]  # point for the start of the line at loop cycle i
            goal_point = points[i]  # point for the end of the line at loop cycle i
            self.draw_dot(start_point[0], start_point[1], 'purple')
            self.draw_line(start_point, goal_point, 'pink')

    def draw_line(self, start_point: [], goal_point: [], color):
        self.__draw_line(start_point[0], start_point[1], goal_point[0], goal_point[1], color)


class ConfigspaceCalculator:
    def __init__(self, max_width: int, max_height: int, robot_bmp):
        self.min_width = robot_bmp.width
        self.max_width = max_width - robot_bmp.width
        self.min_height = robot_bmp.height
        self.max_height = max_height - robot_bmp.height


def random_point_yx(min_width, max_width, min_height, max_height) -> []:
    x = random.randrange(min_width, max_width)
    y = random.randrange(min_height, max_height)
    return [y, x]


def calc_distance(point_1yx, point_2yx) -> float:
    return ((point_1yx[0] - point_2yx[0]) ** 2 + (point_1yx[1] - point_2yx[1]) ** 2) ** 0.5


def tuples_under_distance(collision_array, points: [], distance) -> []:
    indices_under_distance = []
    for point_index in range(len(points) - 1):
        for next_point_index in range(point_index + 1, len(points)):
            if calc_distance(points[point_index], points[next_point_index]) < distance:
                indices_under_distance.append([point_index, next_point_index])
    with Pool(4) as p:
        collision_free = p.starmap(
            check_path_collision_free,
            zip(repeat(collision_array), repeat(points), indices_under_distance))
    return filter(None, collision_free)


def check_path_collision_free(collision_array, points: [], index_tuple: []):
    start = points[index_tuple[0]]
    goal = points[index_tuple[1]]
    step_range = round(calc_distance(start, goal))
    for step in range(1, step_range):
        point_between = calc_point_between_xy(start, goal, step, step_range)
        if collision_array[point_between[1]][point_between[0]] == 0:
            return None
    return [index_tuple[0], index_tuple[1]]


def calc_point_between_xy(start_yx, goal_yx, step, step_range) -> []:
    delta_x = round(step * float(goal_yx[1] - start_yx[1]) / float(step_range))
    delta_y = round(step * float(goal_yx[0] - start_yx[0]) / float(step_range))
    new_x = start_yx[1] + delta_x
    new_y = start_yx[0] + delta_y
    return [new_x, new_y]
