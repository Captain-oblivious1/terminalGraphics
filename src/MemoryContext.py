import sys
from Context import *

class MemoryContext(Context):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.buffer = None
        self.smallestRect = None
        self.clearWindow()

    def _writeString(self,x,y,text,bold=False,reverse=False):
        textLen = len(text)
        self._checkBounds(x,y,textLen)
        for i in range(len(text)):
            ch = text[i]
            self.buffer[y][x+i] = ch
            if ch!=' ':
                self.smallestRect.includePoint(Point(x+i,y))

    def clearWindow(self):
        self.buffer = []
        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append(' ')
            self.buffer.append( line )
        self.smallestRect = Rect()

    def readChar(self,x,y):
        self._checkBounds(x,y)
        return self.buffer[y][x]

    def getMaxXy(self):
        return self.width-1,self.height-1

    def print(self,prefix="",shrinkToSize=True):
        self.writeToStream(sys.stdout,prefix,shrinkToSize)

    def writeToStream(self,stream,prefix="",shrinkToSize=True):
        if not shrinkToSize:
            rect = Rect(0,0,self.width,self.height)
        else:
            rect = self.smallestRect

        for y in range(rect.t,rect.b):
            line = self.buffer[y]
            print(prefix,end='',file=stream)
            for end in reversed(range(rect.l,rect.r)):
                if  line[end]!=' ':
                    break
            for x in range(rect.l,end+1):
                print(line[x],end='',file=stream)
            print(file=stream)
                
    def _checkBounds(self,x,y,len=1):
        if x<0 or y<0 or y>=self.height or x+len-1>=self.width:
            raise Exception("readChar invoked with parameters out of bounds")
