import numpy as np
from numpy.core.records import ndarray
import hashlib
from tqdm.tk import trange
from utils import *
from workspace import Workspace


class Collisionspace:

    def __init__(self, room_name: str, robot_name: str, workspace: Workspace):
        self.__workspace = workspace
        self.__robot_image = open_image(robot_name, 'bmp')
        self.__room_image = open_greyscale_bmp(room_name)

        self.robot_array = robot_array_black_white(robot_name)  # TODO unused

        current_hash_digest = hashlib.md5(self.__robot_image.tobytes() + self.__room_image.tobytes()).hexdigest()
        if collision_image_exists(current_hash_digest):
            self.collision_image = open_collision_image(current_hash_digest)
            self.collision_array = np.array(self.collision_image)
        else:
            self.collision_array = self.__calculate_new_collision_array()
            self.collision_image = Image.fromarray(self.collision_array)
            store_collision_image(current_hash_digest, self.collision_array)

    def __calculate_new_collision_array(self) -> ndarray:
        print("Calculating new collision array please be patient.")
        max_x = self.__room_image.width
        max_y = self.__room_image.height
        offset_x = round(self.__robot_image.width / 2)
        offset_y = round(self.__robot_image.height / 2)

        collision_array = array_black(max_y, max_x)
        for y in trange(offset_y, max_y - offset_y):
            for x in range(offset_x, max_x - offset_x):
                if not self.__workspace.is_in_collision(x, y):
                    collision_array[y][x] = GREYSCALE_WHITE
        return collision_array


def array_black(max_y, max_x) -> ndarray:
    return np.zeros(max_y * max_x).reshape(max_y, max_x)


def robot_array_black_white(robot_name: str) -> ndarray:
    robot_image = open_greyscale_bmp(robot_name)
    robot_array = np.array(robot_image).flatten()
    for value in robot_array:
        if greyscale_not_white(value):
            robot_array[value] = GREYSCALE_BLACK
        else:
            robot_array[value] = GREYSCALE_WHITE
    return robot_array.reshape(robot_image.height, robot_image.width)
