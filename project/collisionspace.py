import tkinter
from tkinter import NW

import numpy as np
import os
import hashlib
from tqdm.tk import trange
from PIL import Image, ImageTk, ImageOps
from resource_manager import *


class Collisionspace:

    def __init__(self, robotImagePath, roomImagePath, workspace, root):
        self.canvas = tkinter.Canvas(root)
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
        if hash_exists(self.currentArrayHash):
            self.imageToDisplay = load_hash_image(self.currentArrayHash)
            self.collisionArray = np.array(self.imageToDisplay)
        else:
            self.imageToDisplay = self.calculateNewImage()
            store_hash_image(self.currentArrayHash, self.collisionArray)
        self.canvas.config(bd=0, height=self.MaxY, width=self.MaxX)
        self.imageToDisplay = ImageTk.PhotoImage(self.imageToDisplay)
        self.canvas.create_image(0, 0, image=self.imageToDisplay, anchor=NW)

    def calculateNewImage(self):
        print("calculating new collision image please be patient.")
        for y in trange(self.robotOffsetY, self.MaxY - self.robotOffsetY):
            for x in range(self.robotOffsetX, self.MaxX - self.robotOffsetX):
                if not self.workspace.isInCollision(x, y):
                    self.collisionArray[y][x] = 255
                    # add robot image at x,y position if there is collision
        return Image.fromarray(self.collisionArray)
