from ClosedPath import *
from Component import *

class Menu(Component):
    def __init__(self,parent,options,topLeft):
        super().__init__(parent)

        self.options = options
        self.topLeft = topLeft

        maxLen = 0
        for option in options:
            maxLen = max(len(option[0]),maxLen)

        self.path = ClosedPath(Orientation.HORIZONTAL,True)
        self.path.appendElbowValue(topLeft.x)
        self.path.appendElbowValue(topLeft.y)
        self.path.appendElbowValue(topLeft.x+maxLen+1)
        self.path.appendElbowValue(topLeft.y+len(options)+1)

    def draw(self,context):
        self.path.draw(context)

        y = self.topLeft.y + 1
        x = self.topLeft.x + 1
        for option in self.options:
            context.addString(x,y,option[0])
            y += 1
