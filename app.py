import tkinter 
from tkinter import ttk, RIGHT, Canvas, BOTH, Scale, HORIZONTAL
from workspace import Workspace 
from configspace import Configspace
from controller import  Controller
from PIL import ImageTk, Image
import os
from utils import setBackgroundColor


def demo():
    root = tkinter.Tk()
    root.title("Motion Planning")
    universal_height = 1000

    nb = ttk.Notebook(root)
    page1 = ttk.Frame(nb, width= 1080,height = universal_height)
    page2 = ttk.Frame(nb,width = 1080,height = universal_height)

    nb.add(page1, text='Workspace')
    nb.add(page2, text='Configspace')
    nb.grid(column=0)
 
    workspace = Workspace("./resources/robot_BW_small.bmp", "./resources/Room_BW_small.bmp", page1)
    configspace = Configspace(page2)
    controller = Controller(workspace,configspace)


    workspace.drawAll(workspace.currentPos[0],workspace.currentPos[1])
    def callback(event):
        # print ("clicked at", event.x, event.y)
        controller.drawMouseOffSet(event.x, event.y)
        if controller.isInCollision(): setBackgroundColor(page1,"red")
        else: setBackgroundColor(page1,"green")

    workspace.label.bind("<Button-1>", callback)

    def moveRobotOnPath(val):
        if controller.isAllInitialized():
            controller.setSolutionPathOnCurrentPos(int(val))
            controller.drawCurrentPos()
            if controller.isInCollision(): setBackgroundColor(page1,"red")
            else: setBackgroundColor(page1,"green")

    slider = Scale(page1, from_=0, to=200, orient=HORIZONTAL, command=moveRobotOnPath)
    slider.config(length=600)
    
    def set_goal():
        controller.setCurrentPosAsGoal()
        slider['from_'] = 0
        slider['to_'] = len(configspace.solutionPath)-1

    setGoalButton = ttk.Button(page1, text = 'Set Goal',command = set_goal)
    setGoalButton.pack(side=tkinter.RIGHT)

    def set_init():
        controller.setCurrentPosAsInit()
    setInitButton = ttk.Button(page1, text = 'Set Init',command = set_init)
    setInitButton.pack(side=tkinter.RIGHT)

    slider.pack()

    root.mainloop()


if __name__ == "__main__":
    demo()
