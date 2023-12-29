from Component import *

from Util import *
from Rect import *
from Menu import *
from Model import *

class TextComponent(Component):
    def __init__(self,parent,element):
        super().__init__(parent)
        self.element = element
        self.lineInfo = []
        self.maxLength = None
        self._updateLineInfo()

    def getRect(self):
        rect = Rect()
        for line in range(len(self.lineInfo)):
            rect.unionWith(self._rectForLine(line))
        return rect

    def draw(self,context):
        selected = self.isSelected()
        for line in range(len(self.lineInfo)):
            lineInfo = self.lineInfo[line]
            start = self._startForLine(line)
            context.addString(start.x,start.y,lineInfo.text,selected)

    # Default is for entier rectangle to be true
    def isOnMe(self,point):
        for line in range(len(self.lineInfo)):
            if self._rectForLine(line).isInsidePoint(point):
                return True
        return False

    def move(self,fromPoint,offset,context):
        self.element.location += offset
    def showContextMenu(self,point,context):
        options = ["stop editing","","split","join"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        print("Chose menu option '"+menu.getSelectedOption()+"'")

    def _updateLineInfo(self):
        self.lineInfo = []
        maxLength = 0
        line = ""
        length = 0
        for ch in self.element.text:
            if ch=='\n':
                self.lineInfo.append(TextComponent.LineInfo(line,length))
                if length>maxLength:
                    maxLength = length
                line = ""
                length = 0
            else:
                line += ch
                length += 1
        self.lineInfo.append(TextComponent.LineInfo(line,length))
        if length>maxLength:
            maxLength = length
        self.maxLength = maxLength

    def _startForLine(self,line): #zero based
        location = self.element.location
        justification = self.element.justification
        y = location.y+line
        if justification==Justification.LEFT:
            return Point(location.x,y)
        elif justification==Justification.RIGHT:
            return Point(location.x+self.maxLength-self.lineInfo[line].length,y)
        else:
            return Point(int(location.x-self.lineInfo[line].length/2),y)

    def _rectForLine(self,line):
        start = self._startForLine(line)
        return Rect(start.x,start.y,self.lineInfo[line].length,1)

    class LineInfo:
        def __init__(self,text,length):
            self.text = text
            self.length = length
