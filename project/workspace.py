from resource_manager import open_image, open_greyscale_bmp
from tkinter import *
from PIL import ImageTk
import numpy as np


class Workspace:
    def __init__(self, app_page, room_name, robot_name):
        room_bmp = open_greyscale_bmp(room_name)
        robot_bmp = open_greyscale_bmp(robot_name)
        robot_png = open_image(robot_name, 'png')
        self.__calculator = WorkspaceCalculator(room_bmp, robot_bmp)
        self.__view = WorkspaceView(app_page, room_bmp, robot_bmp, robot_png)
        self.__init_config_xy = []
        self.__goal_config_xy = []
        self.current_position_xy = []

    def bind_click_callback(self, action_ref):
        self.__view.set_callback(action_ref)

    def is_in_collision(self, x, y) -> bool:
        return self.__calculator.is_robot_in_collision(x, y)

    def reset(self):
        self.__init_config_xy = []
        self.__goal_config_xy = []
        self.__view.reset()

    def set_init_config(self, x, y):
        self.__init_config_xy = [x, y]

    def set_goal_config(self, x, y):
        self.__goal_config_xy = [x, y]

    def draw_robot(self, x, y):
        self.__view.reset()
        if self.__init_config_xy:
            self.__view.draw_robot(self.__init_config_xy[0], self.__init_config_xy[1])
        if self.__goal_config_xy:
            self.__view.draw_robot(self.__goal_config_xy[0], self.__goal_config_xy[1])
        self.__view.draw_robot(x, y)


class WorkspaceView:
    def __init__(self, frame, room_bmp_image, robot_bmp_image, robot_png_image):
        self.__root_frame = frame
        self.__room_bmp = room_bmp_image
        self.__room_rgba = room_bmp_image.convert('RGBA')
        self.__robot_bmp = robot_bmp_image
        self.__robot_rgba = robot_png_image.convert('RGBA')
        self.__background = Label(frame, image=ImageTk.PhotoImage(self.__room_rgba))  # setting the photo as background
        self.__style_background(self.__room_rgba)

    def __style_background(self, image: Image):
        tk_image = ImageTk.PhotoImage(image)
        self.__background.configure(image=tk_image)  # update image of label
        self.__background.image = tk_image  # set image to draw (garbage collection reasons)
        self.__background.pack(side="bottom", fill="both", expand=YES)  # packing the label to gid layout of page1

    def set_callback(self, action_ref):
        self.__background.bind("<Button-1>", action_ref)

    def reset(self):
        self.__style_background(self.__room_rgba)

    def draw_robot(self, x_center, y_center):
        transformed_x = x_center - round(0.5 * self.__robot_rgba.width)
        transformed_y = y_center - round(0.5 * self.__robot_rgba.height)

        combined_image = self.__room_rgba.copy()
        combined_image.alpha_composite(self.__robot_rgba.copy(), (transformed_x, transformed_y))
        self.__style_background(combined_image)


class WorkspaceCalculator:
    def __init__(self, room_greyscale_image, robot_greyscale_image):
        self.__room_array_yx = np.array(room_greyscale_image)
        self.__robot_image = robot_greyscale_image
        self.__robot_array_yx = np.array(robot_greyscale_image)  # getting the array of color rgb()
        self.__robot_border_array_yx = self.__analyze_robot_border()

    def __analyze_robot_border(self) -> []:  # returning list of all border Pixel of the robot
        border_pixels_yx = []  # set up the result set
        for robot_px in range(self.__robot_image.width):  # traversing the Pixels of the robot
            for robot_py in range(self.__robot_image.height):
                if pixel_is_dark(self.__robot_array_yx[robot_py, robot_px]):
                    robot_area = self.__robot_array_yx[self.__robot_slice(robot_px, robot_py)]
                    neighbor_pixels = np.array(robot_area).flatten()  # make array 1D to traverse Pixels easy
                    for rgb_pixel in neighbor_pixels:
                        if pixel_is_white(rgb_pixel):
                            border_pixels_yx.append((robot_py, robot_px))
                            break
        return border_pixels_yx

    def __robot_slice(self, point_x: int, point_y: int):
        # not necessary to understand just some conditions for the array borders
        return np.index_exp[
               (point_y if (point_y == 0) else (point_y - 1)):
               (point_y + 1 if (point_y == self.__robot_image.height - 1) else (point_y + 2)),
               (point_x if (point_x == 0) else (point_x - 1)):
               (point_x + 1 if (point_x == self.__robot_image.width - 1) else (point_x + 2))]

    def __room_slice(self, center_x: int, center_y: int):
        return np.index_exp[
               center_y - round(self.__robot_image.height / 2): (center_y + round(self.__robot_image.width / 2)),
               center_x - round(self.__robot_image.height / 2): center_x + round(self.__robot_image.height / 2)]

    def is_robot_in_collision(self, x: int, y: int) -> bool:
        room_area = self.__room_array_yx[self.__room_slice(x, y)]
        for point_yx in self.__robot_border_array_yx:
            if pixel_is_black(self.__robot_array_yx[point_yx]) and pixel_is_black(room_area[point_yx]):
                return True
        return False


def pixel_is_black(rgb_item: int) -> bool:
    return rgb_item < 240  # matt pixel (241-255)


def pixel_is_dark(rgb_item: int) -> bool:
    return rgb_item < 30


def pixel_is_white(rgb_item: int) -> bool:
    return rgb_item >= 100
