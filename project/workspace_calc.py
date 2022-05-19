import numpy as np
from numpy.lib import index_tricks


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

    def __robot_slice(self, point_x: int, point_y: int) -> index_tricks:
        # not necessary to understand just some conditions for the array borders
        return np.index_exp[
               (point_y if (point_y == 0) else (point_y - 1)):
               (point_y + 1 if (point_y == self.__robot_image.height - 1) else (point_y + 2)),
               (point_x if (point_x == 0) else (point_x - 1)):
               (point_x + 1 if (point_x == self.__robot_image.width - 1) else (point_x + 2))]

    def __room_slice(self, center_x: int, center_y: int) -> index_tricks:
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
