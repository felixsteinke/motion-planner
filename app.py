# Commenting is done with '#'
# Imports can be done ether general package wise or specific Modules from Package.
import tkinter  # graphics Lib (not good to use)
from tkinter import ttk, Scale, HORIZONTAL  # for direct access on the Methods they are imported individually->
# https://stackoverflow.com/questions/9439480/from-import-vs-import

from configspace import Configspace
from controller import Controller
from utils import setBackgroundColor
from workspace import Workspace


def demo():  # Method Declaration the indentation works as '{'
    root = tkinter.Tk()  # Tk is something like the Canvas to put your visual components on.
    root.title("Motion Planning")  # refers to the title of the Window.
    universal_height = 1000  # Variable definition

    nb = ttk.Notebook(root)  # Tab element in the Window.
    page1 = ttk.Frame(nb, width=1080, height=universal_height)  # add Frames to the Notebook.
    page2 = ttk.Frame(nb, width=1080, height=universal_height)

    nb.add(page1, text='Workspace')  # Set Text of the Tabs.
    nb.add(page2, text='Configspace')
    nb.grid(column=0)  # Set the grid position of the Notebook.

    workspace = Workspace("./resources/robot_BW_small.bmp", "./resources/Room_BW_small.bmp", "./resources"
            "/robot_BW_small.png", page1)  # Constructor call from the workspace.py to create the related Object.
    configspace = Configspace(page2)
    controller = Controller(workspace, configspace)

    workspace.drawAll(workspace.currentPos[0], workspace.currentPos[1])  # Method called from the workspace.drawAll

    # Method

    def callback(event):  # Method for use with the mouse-callback-button.
        # print ("clicked at", event.x, event.y)
        controller.drawMouseOffSet(event.x, event.y)
        controller.drawCurrentPos()
        if controller.isInCollision():  # if needs no '()' just ':' and indentation.
            setBackgroundColor(page1, "red")
        else:
            setBackgroundColor(page1, "green")

    workspace.label.bind("<Button-1>", callback)  # bind callback method to left-mouse-button to button.

    def moveRobotOnPath(val):  # shows the robot on the current slider timestamp
        if controller.isAllInitialized():  # checks initialization of the config- and workspace.
            controller.setSolutionPathOnCurrentPos(int(val))  # provides the controller with the slider value
            controller.drawCurrentPos()  # controller gets a draw update call.
            if controller.isInCollision():  # collision check collision (till now only returns false)
                setBackgroundColor(page1, "red")  # sets the BG to red if collision is detected.
            else:
                setBackgroundColor(page1, "green")  # no collision BG = green.

    slider = Scale(page1, from_=0, to=200, orient=HORIZONTAL, command=moveRobotOnPath)  # Slider gets styled and bind
    # to method above.
    slider.config(length=600)  # more styling sets pixel length of the slider.

    def set_goal():  # method to get bound to the setGoalButton
        controller.setCurrentPosAsGoal()  # sets the end Position, obviously.
        slider['from_'] = 0  # sets the origin of the time slider.
        slider['to_'] = len(configspace.solutionPath) - 1  # sets the slider upper Limit to the length of the current
        # solution so you can cycle through.

    setGoalButton = ttk.Button(page1, text='Set Goal', command=set_goal)  # bind method from above to the button.
    setGoalButton.pack(side=tkinter.RIGHT)  # set the gid position of the button element.

    def set_init():  # method to get bound to the setInitButton.
        controller.setCurrentPosAsInit()  # sets the position of the starting point and draws it.

    setInitButton = ttk.Button(page1, text='Set Init', command=set_init)  # binding of the button.
    setInitButton.pack(side=tkinter.RIGHT)  # setting the grid layout position of the button.

    slider.pack()  # places the slider according to the layout options configured above.

    root.mainloop()  # gets a thread for the GUI to have the program start and die with the window.


if __name__ == "__main__":  # main method is defined by __main__ and the if __name__ thing is just python way of
    # saying that the name of the current main is the title of the file.
    demo()  # runs the method demo in main.
