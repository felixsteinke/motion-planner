# Commenting is done with '#'
# Imports can be done ether general package wise or specific Modules from Package.
import os
import sys
import tkinter  # graphics Lib (not good to use)
from tkinter import *
# for direct access on the Methods they are imported individually->
# https://stackoverflow.com/questions/9439480/from-import-vs-import
from tkinter import ttk
from tkinter.ttk import Notebook

from collisionspace import Collisionspace
from configspace import Configspace
from controller import Controller
from workspace import Workspace

RESOURCE_PATH = '../resources'


def demo():  # Method Declaration the indentation works as '{'
    root = tkinter.Tk()  # Tk is something like the Canvas to put your visual components on.
    root.title("Motion Planning")  # refers to the title of the Window.
    windowHeight = 800
    windowWidth = 800
    posX = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    posY = int(root.winfo_screenheight() / 2 - windowHeight / 2)
    root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, posX, posY))

    names = optionPopup()
    robotName = names[0]
    roomName = names[1]

    mainFrame = Frame(root)
    mainFrame.pack(fill=BOTH, expand=1)

    xScrollbarHolder = Frame(mainFrame)
    xScrollbarHolder.pack(fill=X, side=BOTTOM)

    my_canvas = Canvas(mainFrame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    x_scrollbar = Scrollbar(xScrollbarHolder, orient=HORIZONTAL, command=my_canvas.xview)
    x_scrollbar.pack(side=BOTTOM, fill=X)

    y_scrollbar = Scrollbar(mainFrame, orient=VERTICAL, command=my_canvas.yview)
    y_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(xscrollcommand=x_scrollbar.set)
    my_canvas.configure(yscrollcommand=y_scrollbar.set)
    my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ALL)))
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    universal_height = 1000  # Variable definition

    nb = Notebook(second_frame)  # Tab element in the Window.
    page1 = Frame(nb)  # add Frames to the Notebook.
    page2 = Frame(nb)

    nb.add(page1, text='Workspace')  # Set Text of the Tabs.
    nb.add(page2, text='Configspace')
    nb.grid(row=1, columnspan=80, column=0)  # Set the grid position of the Notebook.

    workspace = Workspace("{}/{}.bmp".format(RESOURCE_PATH, robotName),
                          "{}/{}.bmp".format(RESOURCE_PATH, roomName),
                          "{}/{}.png".format(RESOURCE_PATH, robotName),
                          page1)  # Constructor call from the workspace.py to create the related Object.
    collisionspace = Collisionspace("{}/{}.bmp".format(RESOURCE_PATH, robotName),
                                    "{}/{}.bmp".format(RESOURCE_PATH, roomName),
                                    workspace, page2)
    configspace = Configspace("{}/{}.bmp".format(RESOURCE_PATH, robotName), page2, collisionspace)
    controller = Controller(workspace, configspace, collisionspace)

    workspace.drawAll(workspace.currentPos[0], workspace.currentPos[1])  # Method called from the workspace.drawAll

    def callback(event):  # Method for use with the mouse-callback-button.
        # print ("clicked at", event.x, event.y)
        controller.drawMouseOffSet(event.x, event.y)
        controller.drawCurrentPos()
        if controller.isInCollision():  # if needs no '()' just ':' and indentation.
            second_frame.config(background='red')
            page1.config(background='red')

        else:
            second_frame.config(background='green')

    workspace.label.bind("<Button-1>", callback)  # bind callback method to left-mouse-button to button.

    def moveRobotOnPath(val):  # shows the robot on the current slider timestamp
        if controller.isAllInitialized():  # checks initialization of the config- and workspace.
            controller.setSolutionPathOnCurrentPos(int(val))  # provides the controller with the slider value
            controller.drawCurrentPos()  # controller gets a draw update call.
            if controller.isInCollision():  # collision check collision (till now only returns false)
                second_frame.config(background='red')  # sets the BG to red if collision is detected.
            else:
                second_frame.config(background='green')  # no collision BG = green.

    slider = Scale(second_frame, from_=0, to=200, orient=HORIZONTAL,
                   command=moveRobotOnPath)  # Slider gets styled and bind
    # to method above.
    slider.config(length=600)  # more styling sets pixel length of the slider.

    def set_goal():  # method to get bound to the setGoalButton
        controller.setCurrentPosAsGoal()  # sets the end Position, obviously.
        slider['from_'] = 0  # sets the origin of the time slider.
        slider['to_'] = len(configspace.solutionPath) - 1  # sets the slider upper Limit to the length of the current
        # solution so you can cycle through.

    setGoalButton = Button(second_frame, text='Set Goal', command=set_goal)  # bind method from above to the button.
    setGoalButton.grid(row=0, column=2)  # set the gid position of the button element.

    def restart():
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    setRestartButton = Button(second_frame, text='Restart', command=restart)  # bind method from above to the button.
    setRestartButton.grid(row=0, column=3)

    def set_init():  # method to get bound to the setInitButton.
        controller.setCurrentPosAsInit()  # sets the position of the starting point and draws it.

    setInitButton = Button(second_frame, text='Set Init', command=set_init)  # binding of the button.
    setInitButton.grid(row=0, column=1)  # setting the grid layout position of the button.

    slider.grid(row=0, column=0)  # places the slider according to the layout options configured above.

    root.mainloop()  # gets a thread for the GUI to have the program start and die with the window.


def optionPopup():
    win = tkinter.Toplevel()
    win.wm_title("Window")

    l = tkinter.Label(win, text="Choose your Configuration.")
    l.grid(row=0, column=0)

    optionListRobot = []
    for file in os.listdir('../resources'):
        if file.startswith('robot_') and file.endswith('.bmp'):
            optionListRobot.append(file.replace('.bmp', ''))
    variableRobot = tkinter.StringVar(win)
    variableRobot.set(optionListRobot[0])
    tkinter.OptionMenu(win, variableRobot, *optionListRobot).grid(row=1, column=0)

    optionListRoom = []
    for file in os.listdir('../resources'):
        if file.startswith('room_') and file.endswith('.bmp'):
            optionListRoom.append(file.replace('.bmp', ''))
    variableRoom = tkinter.StringVar(win)
    variableRoom.set(optionListRoom[0])
    tkinter.OptionMenu(win, variableRoom, *optionListRoom).grid(row=2, column=0)

    ttk.Button(win, text="Okay", command=win.destroy).grid(row=3, column=0)

    windowHeight = win.winfo_reqheight()
    windowWidth = win.winfo_reqwidth()
    posX = int(win.winfo_screenwidth() / 2 - windowWidth / 2)
    posY = int(win.winfo_screenheight() / 2 - windowHeight / 2)
    win.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, posX, posY))
    win.attributes('-topmost', True)
    win.wait_window(win)

    return [variableRobot.get(), variableRoom.get()]


if __name__ == "__main__":  # main method is defined by __main__ and the if __name__ thing is just python way of
    # saying that the name of the current main is the title of the file.
    demo()  # runs the method demo in main.
