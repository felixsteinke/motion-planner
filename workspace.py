from tkinter import ttk

import numpy as np
from PIL import Image, ImageTk, ImageOps


class Workspace:  # first page of app notebook displays the images of the Workspace and checks for collision
    def __init__(self, robotImagePath, envImagePath, robotPNGPath, root):  # setting up workspace with the two images

        self.root = root  # notebook page one = root
        self.envImage = Image.open(envImagePath)  # opening the environment picture
        self.envImage = ImageOps.grayscale(self.envImage)
        self.envArray = np.array(self.envImage)  # getting the array of color rgb()
        self.envPhoto = ImageTk.PhotoImage(self.envImage)  # converting image to tkinter objet for display

        self.robotImage = Image.open(robotImagePath)  # opening the robot picture
        self.robotImage = ImageOps.grayscale(self.robotImage)
        self.robotArray = np.array(self.robotImage)  # getting the array of color rgb()
        self.robotBorderP = self.analyseSimpleRobot()

        self.robotPhoto = Image.open(robotPNGPath)
        self.robotPhoto = self.robotPhoto.convert('RGBA')

        self.label = ttk.Label(root, image=self.envPhoto)  # setting the environment photo as page 1 background

        self.currentPos = (0, 0)  # new Variable for mouse position
        self.isInitialize = False  # initialisation flag variable

    def drawAll(self, xCurrent, yCurrent, xInit=-1, yInit=-1, xGoal=-1, yGoal=-1):  # draw workspace pictures
        # defined parameters work as standard values if parameter is not set at call of method
        self.currentPos = xCurrent, yCurrent  # set currentPos to last clicked position
        imageToDraw = self.envImage.copy().convert('RGBA')  # add environment image to combined image
        if xInit > -1:  # if start position is set
            imageToDraw.alpha_composite(self.robotPhoto.copy(), (xInit - round(0.5 * self.robotPhoto.width), yInit - round(
                0.5 * self.robotPhoto.height)))  # add robot image at start position
        if xGoal > -1:  # if goal position is set
            imageToDraw.alpha_composite(self.robotPhoto.copy(), (xGoal - round(0.5 * self.robotPhoto.width),
                                                       yGoal - round(0.5 * self.robotPhoto.height)))
            # add robot image at start position
        imageToDraw.alpha_composite(self.robotPhoto.copy(), (self.currentPos[0] - round(0.5 * self.robotPhoto.width),
                                                   self.currentPos[1] - round(0.5 * self.robotPhoto.height)))
        # add  robot image at last position clicked
        photoToDraw = ImageTk.PhotoImage(imageToDraw)  # creating tkinter drawable from combined image
        self.label.configure(image=photoToDraw)  # update image of label
        self.label.image = photoToDraw  # set image to draw (garbage collection reasons)
        self.label.pack(side="bottom", fill="both", expand="yes")  # packing the label to gid layout of page1

    def analyseSimpleRobot(self):  # returning list of all border Pixel of the robot
        coordList = []  # set up the result set
        for robotPX in range(self.robotImage.width):  # traversing the Pixels of the robot
            for robotPY in range(self.robotImage.height):  # ''
                if self.robotArray[robotPY, robotPX] < 30:  # check for dark pixel (Matter)
                    currentCut = np.index_exp[  # creating a cut around the current Pixel
                                 (robotPY if (robotPY == 0) else (robotPY - 1)):
                                 (robotPY + 1 if (robotPY == self.robotImage.height - 1) else (robotPY + 2)),
                                 (robotPX if (robotPX == 0) else (robotPX - 1)):
                                 (robotPX + 1 if (robotPX == self.robotImage.width - 1) else (robotPX + 2))]
                    # not necessary to understand just some conditions for the array borders
                    currentSurrounding = self.robotArray[currentCut]  # actual cutting of the Robot array to get slice
                    currentSurrounding = np.array(currentSurrounding).flatten()  # make array 1D to traverse Pixels easy
                    whitePXFlag = False  # setting up flag for Border Check
                    for i in currentSurrounding:  # actually traversing the neighboring Pixels
                        if i >= 100:  # check for nearly white Pixels around the black one
                            whitePXFlag = True  # white pixel as neighbor
                    if whitePXFlag:  # checking Flag
                        coordList.append((robotPY, robotPX))  # adding the identified border pixel
        return coordList  # returning list of all border Pixel of the robot

    def isInCollision(self, x, y):  # returns true if there was a collision detected
        envSlice = np.index_exp[y - round(self.robotImage.height / 2):(y + round(self.robotImage.width / 2)),
                   x - round(self.robotImage.height / 2):x + round(self.robotImage.height / 2)]
        # configuring a slice from the envArray where there is the robot.
        envRobotSection = self.envArray[envSlice]  # actually slicing the envArray
        collisionFlag = False  # Flag to note if there was anny colliding pixels
        for i in self.robotBorderP:
            if (self.robotArray[i] < 240) and (envRobotSection[i] < 240):
                # if there is a matter Pixel (241-255) at the same Coordinates from both arrays -> collision
                collisionFlag = True  # turn Flag to collision
        return collisionFlag  # return the state of the Flag

    def oldIsInCollision(self, x, y):  # returns true if there was a collision detected
        envSlice = np.index_exp[y - round(self.robotImage.height / 2):(y + round(self.robotImage.width / 2)),
                   x - round(self.robotImage.height / 2):x + round(self.robotImage.height / 2)]
        # configuring a slice from the envArray where there is the robot.
        envRobotSection = self.envArray[envSlice]  # actually slicing the envArray
        collisionFlag = False  # Flag to note if there was anny colliding pixels
        for robotPX in range(self.robotImage.width):  # traversing the Pixels of the robot
            for robotPY in range(self.robotImage.height):  # ''
                if (self.robotArray[robotPY, robotPX] < 240) and (envRobotSection[robotPY, robotPX] < 240):
                    # if there is a matter Pixel (241-255) at the same Coordinates from both arrays -> collision
                    collisionFlag = True  # turn Flag to collision
        return collisionFlag  # return the state of the Flag
