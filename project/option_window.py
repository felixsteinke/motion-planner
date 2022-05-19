from tkinter import *  # graphics Lib (not good to use)
from utils import list_resource_files


class OptionWindow:
    def __init__(self):
        selected_options = self.__open_popup()
        self.robot_name = selected_options[0]
        self.room_name = selected_options[1]

    def __open_popup(self):
        window = Toplevel()
        window.wm_title("Calculation Options")
        window.grid_columnconfigure(0, weight=1)

        label = Label(window, text="Choose your Configuration.")
        label.grid(row=0, column=0, sticky='nsew')

        robot_selector = self.__configure_selector(window, row=1, options=list_resource_files('robot_', '.bmp'))
        room_selector = self.__configure_selector(window, row=2, options=list_resource_files('room_', '.bmp'))
        Button(window, text="Okay", command=window.destroy).grid(row=3, column=0, sticky='nsew')

        window.geometry(self.__frame_geometry(window.winfo_screenwidth(), window.winfo_screenheight()))
        window.attributes('-topmost', True)
        window.wait_window(window)
        return [robot_selector.get(), room_selector.get()]

    @staticmethod
    def __configure_selector(window: Toplevel, row: int, options: []) -> StringVar:
        selector = StringVar(window)
        selector.set(options[0])
        OptionMenu(window, selector, *options).grid(row=row, column=0, sticky='nsew')
        return selector

    @staticmethod
    def __frame_geometry(screen_width: int, screen_height: int) -> str:
        window_width = 280
        window_height = 120
        pos_x = int(screen_width / 2 - window_width / 2)
        pos_y = int(screen_height / 2 - window_height / 2)
        return "{}x{}+{}+{}".format(window_width, window_height, pos_x, pos_y)
