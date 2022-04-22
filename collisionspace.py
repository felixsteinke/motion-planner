import tkinter

import numpy as np
import os
from PIL import Image, ImageTk, ImageOps


class Collisionspace:

    def __init__(self, robotImagePath, roomImagePath, workspace, root):
        self.root = root  # setting the root of the second page for access on the Canvas.

        self.workspace = workspace

        self.robotImage = Image.open(robotImagePath)
        robotImage = ImageOps.grayscale(self.robotImage)
        self.robotImage = self.robotImage.convert('RGBA')
        self.robotOffsetX = round(robotImage.width / 2)  # haf of the pixel of the robot png.
        self.robotOffsetY = round(robotImage.height / 2)
        self.storagePath = './resources/collision'

        self.roomImage = Image.open(roomImagePath)
        roomImage = ImageOps.grayscale(self.roomImage)
        self.imageToDisplay = ImageTk.PhotoImage(self.roomImage)
        self.label = tkinter.Label(root, image=self.imageToDisplay)
        self.roomArray = np.array(roomImage)

        self.currentArrayHash = hash(bytes(self.roomArray))

        self.MaxX = roomImage.width  # Max x
        self.MaxY = roomImage.height  # Max y

        self.bigDrawingBusiness()

    def bigDrawingBusiness(self):
        if self.load():
            self.imageToDisplay = self.load()
        else:
            self.imageToDisplay = self.calculateNewImage()
            #  self.store() Todo make work
        self.imageToDisplay = ImageTk.PhotoImage(self.imageToDisplay)
        self.label.configure(image=self.imageToDisplay)  # update image of label
        self.label.image = self.imageToDisplay  # set image to draw (garbage collection reasons)
        self.label.pack(side="bottom", fill="both", expand="yes")

    def calculateNewImage(self):
        print("calculating new collision image please be patient.")
        result = self.roomImage.copy().convert('RGBA')  # add environment image to combined image
        for y in range(self.robotOffsetY, self.MaxY - self.robotOffsetY):
            if (y % 10) == 0: print(
                "finished percentage: %s" % (((y - self.robotOffsetY) / (self.MaxY - (2 * self.robotOffsetY))) * 100))
            for x in range(self.robotOffsetX, self.MaxX - self.robotOffsetX):
                if self.workspace.isInRawCollision(x, y):  # if start position is set
                    result.alpha_composite(self.robotImage.copy(),
                                           (x - round(0.5 * self.robotImage.width),
                                            y - round(0.5 * self.robotImage.height)))
                    # add robot image at x,y position if there is collision
        return result

    def store(self):
        s = self.currentArrayHash
        if not self.checkForExistingHash():
            # todo fix this conversion issue
            ImageTk.getimage(self.imageToDisplay).save(self.storagePath + "/%s.png" % s)

    def load(self) -> Image:
        if self.checkForExistingHash():
            return Image.open(self.storagePath + "/%s.png" % self.currentArrayHash)

    def checkForExistingHash(self):
        foundFlag = False
        for file in os.listdir(self.storagePath):
            if file.startswith(str(self.currentArrayHash)):
                foundFlag = True
        return foundFlag
