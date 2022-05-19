import numpy as np
from numpy.core.records import ndarray
import hashlib
from tqdm.tk import trange
from resource_manager import *
from workspace import Workspace


class Collisionspace:

    def __init__(self, room_name: str, robot_name: str, workspace: Workspace):
        self.__workspace = workspace
        robot_image = open_image(robot_name, 'bmp')
        self.__robot_offset_x = round(robot_image.width / 2)  # haf of the pixel of the robot png.
        self.__robot_offset_y = round(robot_image.height / 2)
        self.robot_array = get_robot_array(robot_name)

        room_image = open_greyscale_bmp(room_name)
        self.__max_x = room_image.width  # Max x
        self.__max_y = room_image.height  # Max y

        current_hash_digest = hashlib.md5(robot_image.tobytes() + room_image.tobytes()).hexdigest()
        self.__init_collision_data(current_hash_digest)

    def __init_collision_data(self, hash_digest: str):
        if collision_image_exists(hash_digest):
            self.collision_image = open_collision_image(hash_digest)
            self.collision_array = np.array(self.collision_image)
        else:
            self.collision_array = self.__calculate_new_array()
            self.collision_image = Image.fromarray(self.collision_array)
            store_collision_image(hash_digest, self.collision_array)

    def __calculate_new_array(self) -> ndarray:
        print("Calculating new collision image please be patient.")
        collision_array = self.__get_black_room_array()
        for y in trange(self.__robot_offset_y, self.__max_y - self.__robot_offset_y):
            for x in range(self.__robot_offset_x, self.__max_x - self.__robot_offset_x):
                if not self.__workspace.is_in_collision(x, y):
                    collision_array[y][x] = 255  # add robot image at x,y position if there is collision
        return collision_array

    def __get_black_room_array(self) -> ndarray:
        return np.zeros(self.__max_y * self.__max_x).reshape(self.__max_y, self.__max_x)


def get_robot_array(robot_name: str) -> ndarray:
    robot_image = open_greyscale_bmp(robot_name)
    robot_array = np.array(robot_image).flatten()
    for i in robot_array:
        if i < 240:
            robot_array[i] = 0
        else:
            robot_array[i] = 255
    return robot_array.reshape(robot_image.height, robot_image.width)
