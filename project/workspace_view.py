from tkinter import *

from PIL import ImageTk


class WorkspaceView:
    def __init__(self, app_page, room_greyscale_image, robot_png_image):
        self.__root_frame = app_page
        self.__room_rgba = room_greyscale_image.convert('RGBA')
        self.__robot_rgba = robot_png_image.convert('RGBA')

        self.__current_image = self.__room_rgba.copy()
        self.__background = Label(app_page, image=ImageTk.PhotoImage(self.__current_image))

        self.__style_current_background()

    def __style_current_background(self) -> None:
        tk_image = ImageTk.PhotoImage(self.__current_image)
        self.__background.configure(image=tk_image)  # update image of label
        self.__background.image = tk_image  # set image to draw (garbage collection reasons)
        self.__background.pack(side="bottom", fill="both", expand=YES)  # packing the label to gid layout

    def set_click_callback(self, action_ref) -> None:
        self.__background.bind("<Button-1>", action_ref)

    def reset(self) -> None:
        self.__current_image = self.__room_rgba
        self.__style_current_background()

    def draw_robot(self, x_center, y_center) -> None:
        transformed_x = x_center - round(0.5 * self.__robot_rgba.width)
        transformed_y = y_center - round(0.5 * self.__robot_rgba.height)

        combined_image = self.__current_image.copy()
        combined_image.alpha_composite(self.__robot_rgba.copy(), (transformed_x, transformed_y))
        self.__current_image = combined_image
        self.__style_current_background()
