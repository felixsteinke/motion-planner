import os
import sys
from tkinter import *

from collisionspace import Collisionspace
from configspace import Configspace
from controller import Controller
from project.main_frame import MainFrame
from project.option_frame import OptionFrame
from workspace import Workspace


def demo():  # Method Declaration the indentation works as '{'

    main_frame = MainFrame()
    options = OptionFrame()
    workspace = Workspace(options.room_name, options.robot_name, main_frame.notebook_page1)
    collisionspace = Collisionspace(options.room_name, options.robot_name, workspace, main_frame.notebook_page2)
    configspace = Configspace(options.robot_name, main_frame.notebook_page2, collisionspace)
    controller = Controller(workspace, configspace, collisionspace)

    workspace.drawAll(workspace.currentPos[0], workspace.currentPos[1])  # Method called from the workspace.drawAll

    def callback(event):  # Method for use with the mouse-callback-button.
        # print ("clicked at", event.x, event.y)
        controller.drawMouseOffSet(event.x, event.y)
        controller.drawCurrentPos()
        if controller.isInCollision():  # if needs no '()' just ':' and indentation.
            main_frame.canvas_frame.config(background='red')
            main_frame.canvas_frame.config(background='red')

        else:
            main_frame.canvas_frame.config(background='green')

    workspace.label.bind("<Button-1>", callback)  # bind callback method to left-mouse-button to button.

    def moveRobotOnPath(val):  # shows the robot on the current slider timestamp
        if controller.isAllInitialized():  # checks initialization of the config- and workspace.
            controller.setSolutionPathOnCurrentPos(int(val))  # provides the controller with the slider value
            controller.drawCurrentPos()  # controller gets a draw update call.
            if controller.isInCollision():  # collision check collision (till now only returns false)
                main_frame.canvas_frame.config(background='red')  # sets the BG to red if collision is detected.
            else:
                main_frame.canvas_frame.config(background='green')  # no collision BG = green.

    slider = Scale(main_frame.canvas_frame, from_=0, to=200, orient=HORIZONTAL,
                   command=moveRobotOnPath)  # Slider gets styled and bind
    # to method above.
    slider.config(length=600)  # more styling sets pixel length of the slider.

    def set_goal():  # method to get bound to the setGoalButton
        controller.setCurrentPosAsGoal()  # sets the end Position, obviously.
        slider['from_'] = 0  # sets the origin of the time slider.
        slider['to_'] = len(configspace.solutionPath) - 1  # sets the slider upper Limit to the length of the current
        # solution so you can cycle through.

    setGoalButton = Button(main_frame.canvas_frame, text='Set Goal',
                           command=set_goal)  # bind method from above to the button.
    setGoalButton.grid(row=0, column=2)  # set the gid position of the button element.

    def restart():
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    setRestartButton = Button(main_frame.canvas_frame, text='Restart',
                              command=restart)  # bind method from above to the button.
    setRestartButton.grid(row=0, column=3)

    def set_init():  # method to get bound to the setInitButton.
        controller.setCurrentPosAsInit()  # sets the position of the starting point and draws it.

    setInitButton = Button(main_frame.canvas_frame, text='Set Init', command=set_init)  # binding of the button.
    setInitButton.grid(row=0, column=1)  # setting the grid layout position of the button.

    slider.grid(row=0, column=0)  # places the slider according to the layout options configured above.

    main_frame.root.mainloop()  # gets a thread for the GUI to have the program start and die with the window.


if __name__ == "__main__":  # main method is defined by __main__ and the if __name__ thing is just python way of
    # saying that the name of the current main is the title of the file.
    demo()  # runs the method demo in main.
