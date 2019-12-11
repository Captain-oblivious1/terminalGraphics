from PathComponent import *
from ClosedPath import *

class Menu(PathComponent):
    def __init__(self,options,topLeft):

        self.options = options
        self.topLeft = topLeft

        maxLen = 0
        for option in options:
            maxLen = max(len(option[0]),maxLen)

        pathElement = PathElement()
        pathElement.pathType = PathType.CLOSED
        pathElement.startOrientation = Orientation.HORIZONTAL
        pathElement.turns = [topLeft.x,topLeft.y,topLeft.x+maxLen+1,topLeft.y+len(options)+1]
        pathElement.corners = Corners.ROUND

        super().__init__(pathElement,ClosedPath(Orientation.HORIZONTAL))

    def draw(self,context):
        super().draw(context)
        y = self.topLeft.y + 1
        x = self.topLeft.x + 1
        for option in self.options:
            context.addString(x,y,option[0])
            y += 1
