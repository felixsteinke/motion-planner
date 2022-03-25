from tkinter import ttk, Canvas, BOTH, CENTER, RAISED

class Configspace:

    def off(self,x):
      return x+self.theOffset

    def __init__(self,root):
        self.initConfig = -1, -1
        self.goalConfig = -1, -1
        self.solutionPath = []
        self.isInitialize = False
        self.root = root
        self.xExt = 0
        self.yExt = 0
        self.canvas = Canvas(self.root)
        self.theOffset = 24
      
    def setDimensions(self,x,y):      
      self.xExt=x
      self.yExt=y
      off = self.theOffset
      self.canvas.config(bd=0, height=y+2*self.theOffset, width=x+2*self.theOffset)  
      self.drawSpace()   
      self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
      # self.canvas.pack(fill=BOTH, expand=1)

    def drawSpace(self):
         #Open: remove offset, canvas.config offset buggy
      self.canvas.delete("all")
      y = self.yExt
      x = self.xExt
      self.canvas.create_line(self.off(0), self.off(0), self.off(0), self.off(y))
      self.canvas.create_line(self.off(0), self.off(0), self.off(x), self.off(0))
      self.canvas.create_line(self.off(x), self.off(y), self.off(x), self.off(0))
      self.canvas.create_line(self.off(x), self.off(y), self.off(0), self.off(y))

      if len(self.solutionPath)>0: self.drawSolutionPath()
      if self.initConfig[0]>-1: self.drawConfiguration(self.initConfig[0],self.initConfig[1],'green')
      if self.goalConfig[0]>-1: self.drawConfiguration(self.goalConfig[0],self.goalConfig[1],'red')

    def drawConfiguration(self,x,y,color):
      r =5
      self.canvas.create_oval(self.off(x-r),self.off(y-r),self.off(x+r),self.off(y+r),fill=color)

    def drawSolutionPath(self):
      for i in range(1,len(self.solutionPath)):
        c1 = self.solutionPath[i-1]
        c2 = self.solutionPath[i]
        self.canvas.create_line(self.off(c1[0]),self.off(c1[1]),self.off(c2[0]),self.off(c2[1]),fill='purple1')


    def setIntialSolutionPath(self):
        resolution = max(abs(
            self.initConfig[0]-self.goalConfig[0]), abs(self.goalConfig[1]-self.goalConfig[1]))

        self.solutionPath.append(self.initConfig)
        for i in range(1,resolution):
            deltaX = round(i*float(self.goalConfig[0]-self.initConfig[0])/float(resolution))
            deltaY = round(i*float(self.goalConfig[1]-self.initConfig[1])/float(resolution))
            newX = self.initConfig[0] + deltaX
            newY = self.initConfig[1] + deltaY
            self.solutionPath.append((newX, newY))
        self.solutionPath.append(self.goalConfig)


