from tkinter import CENTER
from PIL import Image


class Configspace:  # shows the way of the robot the algorithm

    def __init__(self, robotImagePath, root):
        self.initConfig = -1, -1  # position of the start Image
        self.goalConfig = -1, -1  # position of the goal Image
        self.solutionPath = []  # array of Waypoints
        self.isInitialize = False  # flag for start & endpoint set
        self.root = root  # setting the root of the second page for access on the Canvas.
        self.xExt = 0  # Max x
        self.yExt = 0  # Max y
        self.canvas = root.winfo_children()[0]  # Canvas for 2D graphics.
        self.theOffsetX = int(Image.open(robotImagePath).width/2)  # haf of the pixel of the robot png.
        self.theOffsetY = int(Image.open(robotImagePath).height/2)

    def setDimensions(self, x, y):  # of the canvas
        self.xExt = x  # set Max x
        self.yExt = y  # set Max Y
        self.canvas.config(bd=0, height=y, width=x)  # bd = Border just
        # setting up the canvas dimensions + offset 2 times so the center of the set Robot is always inside.
        self.drawSpace()  # actually drawing the canvas with borders and solution path
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # placing the canvas on the second page
        # self.canvas.pack(fill=BOTH, expand=1) (NOT MY COMMENT)

    def drawSpace(self):
        # Open: remove offset, canvas.config offset buggy (NOT MY COMMENT)
        # self.canvas.delete("all")  # deletes all drawings from the canvas
        y = self.yExt  # set local y to Max y of the
        x = self.xExt  # set local x to Max x of the
        self.canvas.create_line(self.theOffsetX, self.theOffsetY, self.theOffsetX, y - self.theOffsetY, fill='red')  # left border
        self.canvas.create_line(self.theOffsetX, self.theOffsetY, x - self.theOffsetX, self.theOffsetY, fill='red')  # upper border
        self.canvas.create_line(x - self.theOffsetX, y - self.theOffsetY, x - self.theOffsetX, self.theOffsetY,
                                fill='red')  # right
        self.canvas.create_line(x - self.theOffsetX, y - self.theOffsetY, self.theOffsetX, y - self.theOffsetY,
                                fill='red')  # lower

        if len(self.solutionPath) > 0: self.drawSolutionPath()  # if the Solution Path is calculated draw it.
        if self.initConfig[0] > -1: self.drawConfiguration(self.initConfig[0], self.initConfig[1], 'green')  # if the
        # start Point is set draw it in green color.
        if self.goalConfig[0] > -1: self.drawConfiguration(self.goalConfig[0], self.goalConfig[1], 'red')  # if the
        # goal Point is set draw it in red color.

    def drawConfiguration(self, x, y, color):  # draws a dot on the Canvas (used above for the start and goal)
        r = 5  # radius of the colored dot
        self.canvas.create_oval(x - r,
                                y - r,
                                x + r,
                                y + r,
                                fill=color)  # draw color

    def drawSolutionPath(self):  # Draws a line connecting all the points from the solution-path
        for i in range(1, len(self.solutionPath)):  # iterate over points from solution-path
            c1 = self.solutionPath[i - 1]  # c1 is the point for the start of the line at loop cycle i
            c2 = self.solutionPath[i]  # c2 is the point for the end of the line at loop cycle i
            self.canvas.create_line(c1[0], c1[1],
                                    c2[0], c2[1], fill='purple1')
            # draws line from c1 to c2 in purple color

    def setIntialSolutionPath(self):  # fills the self.solutionpath array with points in a straight line from start
        # to goal points
        resolution = max(abs(
            self.initConfig[0] - self.goalConfig[0]), abs(self.goalConfig[1] - self.goalConfig[1]))  # calculating
        # the distance between start and goal in x and y and taking the higher value.

        self.solutionPath.append(self.initConfig)  # adding the start point to the solution path
        for i in range(1, resolution):
            deltaX = round(i * float(self.goalConfig[0] - self.initConfig[0]) / float(resolution))  # calculating the
            # distance to go in x direction for a straight connection of start and goal
            deltaY = round(i * float(self.goalConfig[1] - self.initConfig[1]) / float(resolution))  # calculating the
            # distance to go in y direction for a straight connection of start and goal
            newX = self.initConfig[0] + deltaX  # calculating new coords with origin and current delta at time i
            newY = self.initConfig[1] + deltaY  # ''
            self.solutionPath.append((newX, newY))  # add new Point to the solution path
        self.solutionPath.append(self.goalConfig)  # add goal to the solution path
