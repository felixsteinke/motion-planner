import tkinter

import numpy as np
import os
import hashlib
from tqdm import tqdm
from PIL import Image, ImageTk, ImageOps


class Collisionspace:

    def __init__(self, robotImagePath, roomImagePath, workspace, root):
        self.label = tkinter.Label(root)
        self.root = root  # setting the root of the second page for access on the Canvas.

        self.workspace = workspace

        self.robotImage = Image.open(robotImagePath)
        robotImage = ImageOps.grayscale(self.robotImage)
        self.robotArray = np.array(robotImage).flatten()
        for i in self.robotArray:
            if i < 240:
                self.robotArray[i] = 0
            else:
                self.robotArray[i] = 255
        self.robotArray = self.robotArray.reshape(robotImage.height, robotImage.width)
        self.robotOffsetX = round(robotImage.width / 2)  # haf of the pixel of the robot png.
        self.robotOffsetY = round(robotImage.height / 2)

        self.storagePath = './resources/collision'

        self.roomImage = Image.open(roomImagePath)
        self.roomImage = ImageOps.grayscale(self.roomImage)
        self.roomArray = np.array(self.roomImage)
        self.currentArrayHash = hashlib.md5(self.robotImage.tobytes() + self.roomImage.tobytes()).hexdigest()

        self.MaxX = self.roomImage.width  # Max x
        self.MaxY = self.roomImage.height  # Max y

        self.collisionArray = np.zeros(self.MaxY * self.MaxX).reshape(self.MaxY, self.MaxX)

        self.imageToDisplay = Image.fromarray(self.collisionArray)

        self.bigDrawingBusiness()

    def bigDrawingBusiness(self):
        if self.checkForExistingHash():
            self.imageToDisplay = self.load()
        else:
            self.imageToDisplay = self.calculateNewImage()
            self.store()
        self.imageToDisplay = ImageTk.PhotoImage(self.imageToDisplay)
        self.label.configure(image=self.imageToDisplay)  # update image of label
        self.label.image = self.imageToDisplay  # set image to draw (garbage collection reasons)
        self.label.pack(side="bottom", fill="both", expand="yes")

    def calculateNewImage(self):
        print("calculating new collision image please be patient.")
        for y in tqdm(range(self.robotOffsetY, self.MaxY - self.robotOffsetY)):
            for x in range(self.robotOffsetX, self.MaxX - self.robotOffsetX):
                if not self.workspace.isInCollision(x, y):
                    self.collisionArray[y][x] = 255
                    # add robot image at x,y position if there is collision
        return Image.fromarray(self.collisionArray)

    def store(self):
        s = self.currentArrayHash
        if not self.checkForExistingHash():
            # todo fix this conversion issue
            Image.fromarray(self.collisionArray).convert("L").save(self.storagePath + "/%s.bmp" % s)

    def load(self) -> Image:
        if self.checkForExistingHash():
            return Image.open(self.storagePath + "/%s.bmp" % self.currentArrayHash)

    def checkForExistingHash(self):
        foundFlag = False
        for file in os.listdir(self.storagePath):
            if file.startswith(str(self.currentArrayHash)):
                foundFlag = True
        return foundFlag
