from Model import *
from Point import *

class TextEditor():
    def __init__(self,text,justification,listener):
        self.text = text
        self.justification = justification
        self.listener = listener
        self.lineInfo = []
        self.maxLength = None
        self._updateLineInfo()
        self.editLocation = 0

    def keyEvent(self,event):
        if event>=0 and event<=255 and event!=8:
            if(event==27): # ESC
                self._stopEditing()
            else:
                self._charTyped(event)
        else:
            if event==263 or event==8: # Backspace
                self._backspace()
            elif event==330: # del
                self._del()
            elif event==258: # down
                self._down()
            elif event==259: # up
                self._up()
            elif event==260: # left
                self._left()
            elif event==261: # right
                self._right()
            else:
                return False
        return True

    def cursorOffset(self):
        row,col = self.rowAndColForCharPosition(self.editLocation)
        return Point(col,row)

    def _backspace(self):
        if self.editLocation>0:
            oldText = self.text
            self.listener.invalidate()
            self._changeText( oldText[0:self.editLocation-1] + oldText[self.editLocation:] )
            self.editLocation -= 1
            self.listener.invalidate()

    def _del(self):
        oldText = self.text
        self.listener.invalidate()
        self._changeText( oldText[0:self.editLocation] + oldText[self.editLocation+1:] )
        self.listener.invalidate()

    def _down(self):
        self.listener.invalidate()
        row,col = self.rowAndColForCharPosition( self.editLocation )
        if row<len(self.lineInfo)-1:
            self.editLocation = self.positionForRowAndCol(row+1,col)
        self.listener.invalidate()

    def _up(self):
        self.listener.invalidate()
        row,col = self.rowAndColForCharPosition( self.editLocation )
        if row>0:
            self.editLocation = self.positionForRowAndCol(row-1,col)
        self.listener.invalidate()

    def _left(self):
        self.listener.invalidate()
        if self.editLocation>0:
            self.editLocation -= 1
        self.listener.invalidate()

    def _right(self):
        self.listener.invalidate()
        if self.editLocation<len(self.text):
            self.editLocation += 1
        self.listener.invalidate()

    def _charTyped(self,event):
        self.listener.invalidate()
        oldText = self.text
        self._changeText( oldText[0:self.editLocation]+chr(event)+oldText[self.editLocation:] )
        self.editLocation += 1
        self.listener.invalidate()

    def _changeText(self,text):
        self.text = text
        self._updateLineInfo()
        self.listener.changeText(text)

    def _stopEditing(self):
        self.listener.stopEditing()

    def _updateLineInfo(self):
        self.lineInfo = []
        maxLength = 0
        line = ""
        length = 0
        for ch in self.text:
            if ch=='\n':
                self.lineInfo.append(TextEditor.LineInfo(line,length))
                if length>maxLength:
                    maxLength = length
                line = ""
                length = 0
            else:
                line += ch
                length += 1
        self.lineInfo.append(TextEditor.LineInfo(line,length))
        if length>maxLength:
            maxLength = length
        self.maxLength = maxLength

    def _offsetForRow(self,row):
        justification = self.justification
        if justification==Justification.LEFT:
            return 0
        elif justification==Justification.RIGHT:
            return self.maxLength-self.lineInfo[row].length
        else:
            return int(-self.lineInfo[row].length/2)

    def rowAndColForCharPosition(self,pos):
        #debugPos=pos
        row = 0
        for line in self.lineInfo:
            if pos <= line.length:
                offset = self._offsetForRow(row)
                col = pos + offset
                return row,col
            else:
                pos -= line.length + 1
                row += 1
        return None

    def positionForRowAndCol(self,row,col):
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
        return pos

    class LineInfo:
        def __init__(self,text,length):
            self.text = text
            self.length = length

