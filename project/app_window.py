from tkinter import *
from tkinter.ttk import Notebook


class AppWindow:
    def __init__(self):
        self.root = self.__configure_root()
        self.__canvas = self.__open_canvas_frame()
        nb = Notebook(self.__canvas)  # Tab element in the Window.
        self.workspace_page = Frame(nb)  # add Frames to the Notebook.
        self.configspace_page = Frame(nb)
        nb.add(self.workspace_page, text='Workspace')  # Set Text of the Tabs.
        nb.add(self.configspace_page, text='Configspace')
        nb.grid(row=1, columnspan=80, column=0)  # Set the grid position of the Notebook.

    def paint_background(self, red: bool):
        if red:  # if needs no '()' just ':' and indentation.
            self.__canvas.config(background='red')  # sets the BG to red if collision is detected.
        else:
            self.__canvas.config(background='green')  # no collision BG = green.

    def add_slider(self, column: int, action_ref) -> Scale:
        slider = Scale(self.__canvas, from_=0, to=200, orient=HORIZONTAL, command=action_ref)
        slider.config(length=600)  # more styling sets pixel length of the slider.
        slider.grid(row=0, column=column)  # places the slider according to the layout options configured above.
        return slider

    def add_button(self, text: str, column: int, action_ref):
        set_restart_button = Button(self.__canvas, text=text, command=action_ref)
        set_restart_button.grid(row=0, column=column)

    def __open_canvas_frame(self) -> Frame:
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=1)

        scrollbar_frame = Frame(main_frame)
        scrollbar_frame.pack(fill=X, side=BOTTOM)

        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        x_scrollbar = Scrollbar(scrollbar_frame, orient=HORIZONTAL, command=canvas.xview)
        x_scrollbar.pack(side=BOTTOM, fill=X)
        y_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        y_scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(xscrollcommand=x_scrollbar.set)
        canvas.configure(yscrollcommand=y_scrollbar.set)
        canvas.configure()
        canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox(ALL)))
        canvas_frame = Frame(canvas)
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw")
        return canvas_frame

    def __configure_root(self) -> Tk:
        root = Tk()  # Tk is something like the Canvas to put your visual components on.
        root.title("Motion Planning")  # refers to the title of the Window.
        root.geometry(self.__root_geometry(root.winfo_screenwidth(), root.winfo_screenheight()))
        return root

    @staticmethod
    def __root_geometry(screen_width: int, screen_height: int) -> str:
        window_width = 1020
        window_height = 800
        pos_x = int(screen_width / 2 - window_width / 2)
        pos_y = int(screen_height / 2 - window_height / 2)
        return "{}x{}+{}+{}".format(window_width, window_height, pos_x, pos_y)
