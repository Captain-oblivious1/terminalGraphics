from ClosedPath import *
from Component import *

class Menu(Component):
    def __init__(self,parent,options,topLeft,resultFunction):
        super().__init__(parent)

        self.options = options
        self.topLeft = topLeft
        self.resultFunction = resultFunction

        maxLen = 0
        for option in options:
            maxLen = max(len(option),maxLen)

        self.path = ClosedPath(Orientation.HORIZONTAL,True)
        self.path.appendElbowValue(topLeft.x)
        self.path.appendElbowValue(topLeft.y)
        self.path.appendElbowValue(topLeft.x+maxLen+1)
        self.path.appendElbowValue(topLeft.y+len(options)+1)

        self.rect = Rect(topLeft.x,topLeft.y,maxLen+2,len(options)+2)

    def draw(self,context):
        self.path.draw(context)

        y = self.topLeft.y + 1
        x = self.topLeft.x + 1
        for option in self.options:
            context.addString(x,y,option)
            y += 1

    def getRect(self):
        return self.rect

    def clickedOn(self,point):
        index = (point-self.topLeft).y - 1
        if index>=0 and index<len(self.options):
            self.resultFunction(index)

        self.invalidate()
        self.getTopLevelComponent().clearMenu()
