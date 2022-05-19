from resource_manager import open_image, open_greyscale_bmp
from workspace_calc import WorkspaceCalculator
from workspace_view import WorkspaceView


class Workspace:
    def __init__(self, app_page, room_name, robot_name):
        room_bmp = open_greyscale_bmp(room_name)
        robot_bmp = open_greyscale_bmp(robot_name)
        robot_png = open_image(robot_name, 'png')
        self.__calculator = WorkspaceCalculator(room_bmp, robot_bmp)
        self.__view = WorkspaceView(app_page, room_bmp, robot_png)
        self.__init_config_xy = []
        self.__goal_config_xy = []
        self.current_position_xy = []

    def bind_click_callback(self, action_ref):
        self.__view.set_click_callback(action_ref)

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

    def draw_robot_state(self, x, y):
        self.__view.reset()
        if self.__init_config_xy:
            self.__view.draw_robot(self.__init_config_xy[0], self.__init_config_xy[1])
        if self.__goal_config_xy:
            self.__view.draw_robot(self.__goal_config_xy[0], self.__goal_config_xy[1])
        self.__view.draw_robot(x, y)
