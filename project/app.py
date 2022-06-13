import os
import sys

from app_window import AppWindow
from option_window import OptionWindow
from workspace import Workspace
from collisionspace import Collisionspace
from configspace import Configspace
from multiprocessing import freeze_support


def main():  # Method Declaration the indentation works as '{'

    app_window = AppWindow()
    options = OptionWindow(app_window.root.winfo_id())
    # TODO resize app window for room bmp
    room_name = options.room_name
    robot_name = options.robot_name

    workspace = Workspace(app_window.workspace_page, room_name, robot_name)
    collisionspace = Collisionspace(room_name, robot_name, workspace)
    configspace = Configspace(app_window.configspace_page, robot_name, collisionspace)

    # === ACTIONS ======================================================================================================

    def mouse_callback(event):  # Method for use with the mouse-callback-button.
        workspace.current_position_xy = [event.x, event.y]
        workspace.draw_robot_state(event.x, event.y)
        app_window.paint_background(workspace.is_in_collision(event.x, event.y))

    def move_slider(val):  # shows the robot on the current slider timestamp
        if configspace.solution_pixels_yx:
            point_yx = configspace.solution_pixels_yx[int(val)]
            workspace.draw_robot_state(point_yx[1], point_yx[0])
            app_window.paint_background(workspace.is_in_collision(point_yx[1], point_yx[0]))

    def set_init_action():  # method to get bound to the set_init_button.
        if workspace.current_position_xy:
            workspace.set_init_config(workspace.current_position_xy[0], workspace.current_position_xy[1])
            configspace.set_init_config(workspace.current_position_xy[0], workspace.current_position_xy[1])

    def set_goal_action():  # method to get bound to the setGoalButton
        if workspace.current_position_xy:
            workspace.set_goal_config(workspace.current_position_xy[0], workspace.current_position_xy[1])
            configspace.set_goal_config(workspace.current_position_xy[0], workspace.current_position_xy[1])

    def execute_sprm():
        configspace.execute_sprm()
        slider['from_'] = 0
        slider['to_'] = len(configspace.solution_pixels_yx) - 1

    def execute_rrt():
        configspace.execute_rrt()
        slider['from_'] = 0
        slider['to_'] = len(configspace.solution_pixels_yx) - 1

    def benchmark():
        configspace.execute_benchmark()

    def reset_action():
        workspace.reset()
        configspace.reset()

    def restart_action():
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    # === ACTIONS BINDING ==============================================================================================

    workspace.bind_click_callback(mouse_callback)
    slider = app_window.add_slider(0, move_slider)
    app_window.add_button('Set Init', 1, set_init_action)
    app_window.add_button('Set Goal', 2, set_goal_action)
    app_window.add_button('Execute sPRM', 3, execute_sprm)
    app_window.add_button('Execute RRT', 4, execute_rrt)
    app_window.add_button('Benchmark', 5, benchmark)
    app_window.add_button('Reset', 6, reset_action)
    app_window.add_button('Restart', 7, restart_action)

    # === APP THREAD ===================================================================================================

    app_window.root.mainloop()  # gets a thread for the GUI to have the program start and die with the window.


if __name__ == "__main__":  # main method is defined by __main__ and the if __name__ thing is just python way of
    # saying that the name of the current main is the title of the file.
    freeze_support()
    main()  # runs the method demo in main.
