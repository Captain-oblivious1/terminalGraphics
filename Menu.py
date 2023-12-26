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

        valArray = [topLeft.x,topLeft.y,topLeft.x+maxLen+1,topLeft.y+len(options)+1]
        refArray = []
        for val in valArray:
            refArray.append(ConstReference(val))

        self.path = ClosedPath(Orientation.HORIZONTAL,refArray,True)

        self.rect = Rect(topLeft.x,topLeft.y,maxLen+2,len(options)+2)
        self.selectedOption = None
        self.selectedIndex = -1

    def draw(self,context):
        self.path.draw(context,False)

        y = self.topLeft.y + 1
        x = self.topLeft.x + 1
        for option in self.options:
            context.addString(x,y,option)
            y += 1

    def getRect(self):
        return self.rect

    def getTopLeft(self):
        return self.topLeft

    def getSelectedOption(self):
        return self.selectedOption

    def getSelectedIndex(self):
        return self.selectedIndex

    def clickedOn(self,point):
        print("clicked on menu")
        index = (point-self.topLeft).y - 1
        if index>=0 and index<len(self.options):
            self.selectedOption = self.options[index]
            self.selectedIndex = index
            self.resultFunction(self)

        self.invalidate()
        self.getTopLevelComponent().clearMenu()
