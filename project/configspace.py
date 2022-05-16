import random
from tkinter import CENTER
from dijkstar import Graph, find_path
from resource_manager import open_image


def distance(point_one, point_two):
    return ((point_one[0] - point_two[0]) ** 2 +
            (point_one[1] - point_two[1]) ** 2) ** 0.5


class Configspace:  # shows the way of the robot the algorithm

    def __init__(self, robot_name, page, collisionspace):
        self.collisionArray = collisionspace.collisionArray
        self.initConfig = -1, -1  # position of the start Image
        self.goalConfig = -1, -1  # position of the goal Image
        self.solutionPath = []  # array of Waypoints
        self.isInitialize = False  # flag for start & endpoint set
        self.page = page  # setting the root of the second page for access on the Canvas.
        self.xExt = 0  # Max x
        self.yExt = 0  # Max y
        self.canvas = page.winfo_children()[0]  # Canvas for 2D graphics.
        robot_image = open_image(robot_name, 'bmp')
        self.theOffsetX = int(robot_image.width / 2)  # haf of the pixel of the robot png.
        self.theOffsetY = int(robot_image.height / 2)
        self.graph = Graph()

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
        self.canvas.create_line(self.theOffsetX, self.theOffsetY, self.theOffsetX, y - self.theOffsetY,
                                fill='red')  # left border
        self.canvas.create_line(self.theOffsetX, self.theOffsetY, x - self.theOffsetX, self.theOffsetY,
                                fill='red')  # upper border
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

    def drawLine(self, start, goal, color):
        self.canvas.create_line(start[1], start[0], goal[1], goal[0], fill=color)

    def setInitialSolutionPath(self):  # fills the self.solution path array with points in a straight line from start
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
        self.setPRMSolutionPath()

    def randomPoint(self):
        x = random.randrange(self.theOffsetX, self.xExt - self.theOffsetX)
        y = random.randrange(self.theOffsetY, self.yExt - self.theOffsetY)
        resultTuple = (y, x)
        return resultTuple

    def checkPathCollision(self, start, goal):
        steps = round(distance(start, goal))
        for i in range(1, steps):
            deltaX = round(i * float(goal[1] - start[1]) / float(steps))
            deltaY = round(i * float(goal[0] - start[0]) / float(steps))
            newX = start[1] + deltaX
            newY = start[0] + deltaY
            if self.collisionArray[newY][newX] == 0:
                return True
        return False

    def addPathToSolution(self, start, goal):
        steps = round(distance(start, goal))
        for i in range(1, steps):
            deltaX = round(i * float(goal[1] - start[1]) / float(steps))
            deltaY = round(i * float(goal[0] - start[0]) / float(steps))
            newX = start[1] + deltaX
            newY = start[0] + deltaY
            self.solutionPath.append((newX, newY))

    def tupleUnderDistance(self, pointList, d):
        result = []
        for i in range(len(pointList) - 1):
            for c in range(i + 1, len(pointList)):
                if distance(pointList[i], pointList[c]) < d:
                    if not self.checkPathCollision(pointList[i], pointList[c]):
                        resultItem = (i, c)
                        result.append(resultItem)
        return result

    def setPRMSolutionPath(self):
        self.graph.add_node(0)
        self.graph.add_node(1)
        pointsList = [(self.initConfig[1], self.initConfig[0]), (self.goalConfig[1], self.goalConfig[0])]
        points = 1000
        for i in range(2, points + 2):
            foundFlag = True
            while foundFlag:
                newPoint = self.randomPoint()
                if self.collisionArray[newPoint[0]][newPoint[1]] > 1:
                    self.graph.add_node(i)
                    pointsList.append(newPoint)
                    foundFlag = False
        for i in pointsList:
            self.drawConfiguration(i[1], i[0], 'blue')
        for t in self.tupleUnderDistance(pointsList, 80):
            self.graph.add_edge(t[0], t[1], round(distance(pointsList[t[0]], pointsList[t[1]])))
            self.graph.add_edge(t[1], t[0], round(distance(pointsList[t[1]], pointsList[t[0]])))
            self.drawLine(pointsList[t[0]], pointsList[t[1]], 'yellow')
        path = find_path(self.graph, 0, 1)
        lastPoint = pointsList[0]
        for n in path.nodes:
            self.drawConfiguration(lastPoint[1], lastPoint[0], 'purple')
            thisPoint = pointsList[n]
            if not n == 0:
                self.drawLine(lastPoint, thisPoint, 'pink')
                self.addPathToSolution(lastPoint, thisPoint)
            lastPoint = thisPoint
        self.drawConfiguration(pointsList[0][1], pointsList[0][0], 'red')
        self.drawConfiguration(pointsList[1][1], pointsList[1][0], 'green')
