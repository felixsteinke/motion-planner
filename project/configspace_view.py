from tkinter import *
from typing import NamedTuple

from PIL import ImageTk


class ConfigspaceView:
    def __init__(self, app_page, robot_image, collision_image):
        self.__root_frame = app_page
        self.__canvas = Canvas(app_page)  # Canvas for 2D graphics.

        self.__robot_image = robot_image
        self.__collision_image = collision_image

        self.__style_canvas()

    def __style_canvas(self):
        tk_image = ImageTk.PhotoImage(self.__collision_image)
        self.__canvas.config(bd=0, width=self.__collision_image.width, height=self.__collision_image.height)
        self.__canvas.create_image(0, 0, image=tk_image, anchor=NW)
        self.__canvas.image = tk_image  # set image to draw (garbage collection reasons)
        self.__canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.__draw_border()

    def __draw_border(self):
        offset_x = int(self.__robot_image.width / 2)  # haf of the pixel of the robot png.
        offset_y = int(self.__robot_image.height / 2)

        top_left_xy = [offset_x, offset_y]
        top_right_xy = [self.__collision_image.width - offset_x, offset_y]
        bottom_left_xy = [offset_x, self.__collision_image.height - offset_y]
        bottom_right_xy = [self.__collision_image.width - offset_x, self.__collision_image.height - offset_y]

        self.draw_line_xy(top_left_xy, top_right_xy, 'red')
        self.draw_line_xy(top_right_xy, bottom_right_xy, 'red')
        self.draw_line_xy(bottom_right_xy, bottom_left_xy, 'red')
        self.draw_line_xy(bottom_left_xy, top_left_xy, 'red')

    def reset(self):
        tk_image = ImageTk.PhotoImage(self.__collision_image)
        self.__canvas.create_image(0, 0, image=tk_image, anchor=NW)
        self.__canvas.image = tk_image
        self.__draw_border()

    def draw_point(self, center_x, center_y, color) -> None:
        radius = 5
        self.__canvas.create_oval(center_x - radius,
                                  center_y - radius,
                                  center_x + radius,
                                  center_y + radius,
                                  fill=color)

    def draw_line_xy(self, start_point: [], goal_point: [], color) -> None:
        self.__canvas.create_line(start_point[0], start_point[1], goal_point[0], goal_point[1], fill=color)

    def draw_line_yx(self, start_point: [], goal_point: [], color) -> None:
        self.__canvas.create_line(start_point[1], start_point[0], goal_point[1], goal_point[0], fill=color)
