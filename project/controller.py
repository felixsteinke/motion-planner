class Controller:
    def __init__(self, workspace, configspace, collisionspace):
        self.workspace = workspace  # init class reference of workspace page
        self.configspace = configspace  # init class reference of configspace page
        self.configspace.setDimensions(self.workspace.envArray.shape[1], self.workspace.envArray.shape[0])
        # set dimensions of the configspace Canvas

    def setCurrentPosAsInit(self):  # setting up start position in configspace with data from workspace gets called
        # on Button in app.py
        self.configspace.initConfig = (self.workspace.currentPos[0], self.workspace.currentPos[1])
        self.configspace.drawSpace()

    def setCurrentPosAsGoal(self):  # setting up goal position in configspace with data from workspace gets called
        # on Button in app.py
        self.configspace.goalConfig = (self.workspace.currentPos[0], self.workspace.currentPos[1])
        # self.configspace.setInitialSolutionPath()  # pathfinding-algorithm call
        self.configspace.setPRMSolutionPath()
        self.configspace.isInitialize = True  # set start position flag
        self.workspace.isInitialize = True  # set goal position flag
        self.configspace.drawSpace()  # draws the updated path in configspace

    def drawMouseOffSet(self, mouseX, mouseY):  # send draw update to workspace with last clicked position
        self.workspace.drawAll(mouseX,
                               mouseY,
                               self.configspace.initConfig[0], self.configspace.initConfig[1],
                               self.configspace.goalConfig[0], self.configspace.goalConfig[1])

    def drawCurrentPos(self):   # send draw update to workspace with current time-slider position in solution path
        self.workspace.drawAll(self.workspace.currentPos[0], self.workspace.currentPos[1],
                               self.configspace.initConfig[0], self.configspace.initConfig[1],
                               self.configspace.goalConfig[0], self.configspace.goalConfig[1])

    def isInCollision(self, x=None, y=None):  # checks if the workspace reports a collision for the current mouse pos
        if x is None: x = self.workspace.currentPos[0]  # set variables if not provided at method call
        if y is None: y = self.workspace.currentPos[1]  # ''
        return self.workspace.isInCollision(x, y)  # checks for optical collision in workspace

    def isRawCollision(self, x=None, y=None):  # checks if the workspace reports a collision for the current mouse pos
        return self.workspace.isInRawCollision(x, y)  # checks for optical collision in workspace

    def isAllInitialized(self):  # checks the initialisation of the config- and workspace
        return self.configspace.isInitialize and self.workspace.isInitialize

    def setSolutionPathOnCurrentPos(self, index):  # updates the current pos Variable in workspace to be the one on
        # the timestamp of the slider in the solution path
        self.workspace.currentPos = self.configspace.solutionPath[index]