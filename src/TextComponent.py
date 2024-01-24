from Component import *

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
        self.editLocation = None

    def getRect(self):
        rect = Rect()
        for row in range(len(self.lineInfo)):
            rect.unionWith(self._rectForRow(row))
        return rect

    def draw(self,context):
        #highlight = self.isSelected() or self.editLocation is not None
        index = 0
        for row in range(len(self.lineInfo)):
            lineInfo = self.lineInfo[row]
            start = self._startForRow(row)
            x = start.x
            for ch in lineInfo.text:
                highlight = self.editLocation is not None and self.editLocation==index
                context.writeString(x,start.y,ch,highlight)
                x += 1
                index += 1 
            if index==self.editLocation:
                context.writeString(x,start.y,' ',True)
            index += 1 # for \n

    # Default is for entier rectangle to be true
    def isOnMe(self,point):
        for row in range(len(self.lineInfo)):
            if self._rectForRow(row).isInsidePoint(point):
                return True
        return False

    def move(self,fromPoint,offset,context):
        self.element.location += offset

    def showContextMenu(self,point,context):
        if self.editLocation is not None:
            options = ["stop editing"]
        else:
            options = ["edit"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        if menu.getSelectedOption()=="edit":
            self.editLocation = 0
        else:
            self.editLocation = None
        editor = self.getEditor()
        if self.editLocation is not None:
            editor.addKeyListener(self)
            #self._changeText('')
        else:
            self._stopEditing()

    def keyEvent(self,event):
        self.invalidate()
        try:
            if event>=0 and event<=255:
                if(event==27):
                    self._stopEditing()
                else:
                    oldText = self.element.text
                    self._changeText( oldText[0:self.editLocation]+chr(event)+oldText[self.editLocation:] )
                    self.editLocation += 1
                return True
            else:
                if event==263: # Backspace
                    oldText = self.element.text
                    self._changeText( oldText[0:self.editLocation-1] + oldText[self.editLocation:] )
                    self.editLocation -= 1
                    return True
                elif event==258: # down
                    row,col = self._rowAndColForCharPosition( self.editLocation )
                    #print("before row="+str(row)+" col="+str(col))
                    if row<len(self.lineInfo):
                        self.editLocation = self._positionForRowAndCol(row+1,col)
                elif event==259: # up
                    row,col = self._rowAndColForCharPosition( self.editLocation )
                    if row>0:
                        self.editLocation = self._positionForRowAndCol(row-1,col)
                elif event==260: # left
                    if self.editLocation>0:
                        self.editLocation -= 1
                elif event==261: # right
                    if self.editLocation<len(self.element.text):
                        self.editLocation += 1
                else:
                    return False
            r,c = self._rowAndColForCharPosition(self.editLocation)
            #print("after  row="+str(r)+" col="+str(c))
        finally:
            self.invalidate()

    def _changeText(self,text):
        self.invalidate()
        self.element.text = text
        self._updateLineInfo()
        self.invalidate()

    def _stopEditing(self):
        self.getEditor().removeKeyListener(self)
        self.editLocation = None
        self.invalidate()

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

    def _startForRow(self,row): #zero based
        location = self.element.location
        x = location.x+self._offsetForRow(row)
        y = location.y+row
        return Point(x,y)

    def _offsetForRow(self,row):
        justification = self.element.justification
        if justification==Justification.LEFT:
            return 0
        elif justification==Justification.RIGHT:
            return self.maxLength-self.lineInfo[row].length
        else:
            return int(-self.lineInfo[row].length/2)

    def _rectForRow(self,row):
        start = self._startForRow(row)
        return Rect(start.x,start.y,self.lineInfo[row].length+1,1)

    def _rowAndColForCharPosition(self,pos):
        #debugPos=pos
        row = 0
        for line in self.lineInfo:
            if pos <= line.length:
                offset = self._offsetForRow(row)
                col = pos + offset
                #print("_rowAndColForCharPosition("+str(debugPos)+")="+str(row)+","+str(col))
                return row,col
            else:
                pos -= line.length + 1
                row += 1
        return None

    def _positionForRowAndCol(self,row,col):
        pos = 0
        for i in range(row):
            pos += self.lineInfo[i].length + 1 # 1 for the \n
        left = self._offsetForRow(row)
        right = left + self.lineInfo[row].length# - 1
        if col<left:
            col = left
        elif col>=right:
            col = right
        pos += col - left
        #print("_positionForRowAndCol("+str(row)+","+str(col)+")="+str(pos))
        return pos

    class LineInfo:
        def __init__(self,text,length):
            self.text = text
            self.length = length
