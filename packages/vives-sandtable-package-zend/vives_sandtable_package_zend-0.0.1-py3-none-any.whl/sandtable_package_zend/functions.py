from cmath import cos, pi, sin, sqrt
import numpy as np
import matplotlib.pyplot as plt

class Functions:
    def __init__(self):
        self._xFunction = []
        self._yFunction = []

        self._n = np.linspace(0, 2*np.pi,100)

        self.defaultOffsetX = 100
        self.defaultOffsetY = 100
        self.defaultOffsetMin = 0
        self.defaultOffsetMax = 200
        self.defaultRoundDown = 3
        self.defaultMultiplier = 5
        self.defaultGrowth = 1.1

        self._strX = []
        self._strY = []
        self._intX = []
        self._intY =[]

    def parser(self):
        x = np.around(self._xFunction, self.defaultRoundDown) * self.defaultMultiplier + self.defaultOffsetX
        y = np.around(self._yFunction, self.defaultRoundDown) * self.defaultMultiplier + self.defaultOffsetY
        self._intX = x.astype(int)
        self._intY = y.astype(int)
        self._strX = self._intX.astype(str)
        self._strY = self._intY.astype(str)

    def drawStar(self, amount, angle = 0):
        self.drawPolygon(amount, angle)

    def drawCoil(self, amount):
        n = np.linspace(0, 2*np.pi, amount * 50)
        self._xFunction = [(np.cos((amount + 1)*n) - np.cos(n)) / amount]
        self._yFunction = [(np.sin((amount + 1)*n) - np.sin(n)) / amount]
        self.parser()

    def drawPolygon(self, amount = 3, angle = 0):
        angle = (angle * np.pi / 180)
        n = np.linspace(angle, 2*np.pi + angle, amount + 1)
        self._xFunction = [np.cos(n)]
        self._yFunction = [np.sin(n)]
        self.parser()

    def spiral(self):
        n = np.linspace(0, 4* np.pi, 50)
        self._xFunction = [ np.sqrt(n/20)*(np.cos(n))/10]
        self._yFunction = [ np.sqrt(n/20)*(np.sin(n))/10]
        n = np.linspace(4* np.pi, 8* np.pi, 250)
        self._xFunction = [ np.sqrt(n/20)*(np.cos(n))/10]
        self._yFunction = [ np.sqrt(n/20)*(np.sin(n))/10]
    
        self.parser()

    def clearFunction(self):
        return 0

    def plotFigure(self):
        plt.scatter(self._intX, self._intY)
        plt.show()

    def getX(self):
        return self._x
    def getY(self):
        return self._y



test = Functions()
test.drawPolygon(4)
test.plotFigure()

test.drawPolygon(4, 45)
test.plotFigure()
