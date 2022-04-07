from tkinter import ttk

import numpy as np
from PIL import Image, ImageTk


class Workspace:  # first page of app notebook displays the images of the Workspace and checks for collision
    def __init__(self, robotImagePath, envImagePath, root):  # setting up workspace with the two images

        self.root = root  # notebook page one = root
        self.envImage = Image.open(envImagePath)  # opening the environment picture
        self.envArray = np.array(self.envImage)  # getting the array of color rgb()
        self.envPhoto = ImageTk.PhotoImage(self.envImage)  # converting image to tkinter objet for display

        self.robotImage = Image.open(robotImagePath)  # opening the robot picture
        self.robotArray = np.array(self.robotImage)  # getting the array of color rgb()
        self.robotPhoto = ImageTk.PhotoImage(self.robotImage)  # converting image to tkinter objet for display

        self.label = ttk.Label(root, image=self.envPhoto)  # setting the environment photo as page 1 background

        self.currentPos = (0, 0)  # new Variable for mouse position
        self.isInitialize = False  # initialisation flag variable

    def drawAll(self, xCurrent, yCurrent, xInit=-1, yInit=-1, xGoal=-1, yGoal=-1):  # draw workspace pictures
        # defined parameters work as standard values if parameter is not set at call of method
        self.currentPos = xCurrent, yCurrent  # set currentPos to last clicked position
        imageToDraw = self.envImage.copy()  # add environment image to combined image
        if xInit > -1:  # if start position is set
            imageToDraw.paste(self.robotImage.copy(), (xInit - round(0.5 * self.robotImage.width), yInit - round(
                0.5 * self.robotImage.height)))  # add robot image at start position
        if xGoal > -1:  # if goal position is set
            imageToDraw.paste(self.robotImage.copy(), (xGoal - round(0.5 * self.robotImage.width),
                                                       yGoal - round(0.5 * self.robotImage.height)))
            # add robot image at start position
        imageToDraw.paste(self.robotImage.copy(), (self.currentPos[0] - round(0.5 * self.robotImage.width),
                                                   self.currentPos[1] - round(0.5 * self.robotImage.height)))
        # add  robot image at last position clicked
        photoToDraw = ImageTk.PhotoImage(imageToDraw)  # creating tkinter drawable from combined image
        self.label.configure(image=photoToDraw)  # update image of label
        self.label.image = photoToDraw  # set image to draw (garbage collection reasons)
        self.label.pack(side="bottom", fill="both", expand="yes")  # packing the label to gid layout of page1

    def isInCollision(self, x, y):  # TODO implement solution for collision optical detection.
        return False
