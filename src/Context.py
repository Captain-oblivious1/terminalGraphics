from Rect import *
from Stroke import *
from Model import *
from Util import *

# The following is so that I can more easily do more advanced drawing.
#
# So like this:    │        Not this:    │
#               ┌──┴──┐               ┌─────┐
#             ──┤ box ├──           ──│ box │──
#               └──┬──┘               └─────┘
#                  │                     │
#

# 4D array for all possible box chars
# boxArray [left][right][top][bottom]
# None:      " "   " "   " "   " "
# Thin:      "╴"   "╶"   "╵"   "╷"
# Thick:     "╸"   "╺"   "╹"   "╻"
boxArray = [  
  [ [ [ " ", "╷", "╻"], [ "╵", "│", "╽"], [ "╹", "╿", "┃"] ],
    [ [ "╶", "┌", "┎"], [ "└", "├", "┟"], [ "┖", "┞", "┠"] ],
    [ [ "╺", "┍", "┏"], [ "┕", "┝", "┢"], [ "┗", "┡", "┣"] ] ],
  [ [ [ "╴", "┐", "┒"], [ "┘", "┤", "┧"], [ "┚", "┦", "┨"] ],
    [ [ "─", "┬", "┰"], [ "┴", "┼", "╁"], [ "┸", "╀", "╂"] ],
    [ [ "╼", "┮", "┲"], [ "┶", "┾", "╆"], [ "┺", "╄", "╊"] ] ],
  [ [ [ "╸", "┑", "┓"], [ "┙", "┥", "┧"], [ "┛", "┩", "┫"] ],
    [ [ "╾", "┭", "┱"], [ "┵", "┽", "╅"], [ "┹", "╃", "╉"] ],
    [ [ "━", "┯", "┳"], [ "┷", "┿", "╈"], [ "┻", "╇", "╋"] ] ] ]

# I made up a scheme that allows me to create box characters by 
# or-ing and and-ing other characters.  I assign each character a
# value based an integer that has "pixels" activated.  The follow
# indicates what bits represent what pixel.
#    ┌──┬──┬──┐      All box characters can be created by bitwise
#    │21│20│19│      or-ing any of the following:
# ┌──┼──┼──┼──┼──┐   " " = 0x0
# │18│17│16│15│14│   "╴" = 0x1C00
# ├──┼──┼──┼──┼──┤   "╸" = 0x39CE0
# │13│12│11│10│ 9│   "╶" = 0x700
# ├──┼──┼──┼──┼──┤   "╺" = 0xE738
# │ 8│ 7│ 6│ 5│ 4│   "╵" = 0x88400
# └──┼──┼──┼──┼──┘   "╹" = 0x1DCE00
#    │ 3│ 2│ 1│      "╷" = 0x422
#    └──┴──┴──┘      "╻" = 0xE77
# (I blew off the double line versions because there are no
# Unicode characters that mix and match them.  For example
# I can simulate or-ing "│" with "━" by using the "┿" char.
# But there is no equivalent for the or of "║" and "━". Only
# "║" and "─" (which is "╫").  I think thicker lines is more
# useful than double lines.  Double lines look too DOSy.

charToHexMap = {}
hexToCharMap = {}

def intializeMaps():
    leftArray =   [ 0x0, 0x1C00,  0x39CE0  ]
    rightArray =  [ 0x0, 0x700,   0xE738   ]
    topArray =    [ 0x0, 0x88400, 0x1DCE00 ]
    bottomArray = [ 0x0, 0x422,   0xE77    ]

    for left in range(3):
        for right in range(3):
            for top in range(3):
                for bottom in range(3):
                    value = leftArray[left] | rightArray[right] | topArray[top] | bottomArray[bottom]
                    char = boxArray[left][right][top][bottom]
                    charToHexMap[char] = value
                    hexToCharMap[value] = char

    # treat dashed lines like solid for the purpose of or/and. (chars don't exist for that)
    charToHexMap['╌'] = charToHexMap['─'] 
    charToHexMap['╍'] = charToHexMap['━'] 
    charToHexMap['╎'] = charToHexMap['│'] 
    charToHexMap['╏'] = charToHexMap['┃'] 

    # insert half blocks into charToHexMap for masking stuff (don't put in hexToCharMap)
    charToHexMap["▀"]=0x1FFF00
    charToHexMap["▄"]=0x1FFF
    charToHexMap["▌"]=0x1B9CE6
    charToHexMap["▐"]=0xCE33B

    charToHexMap["▘"]=0x1B9C00
    charToHexMap["▝"]=0xCE700
    charToHexMap["▖"]=0x1CE6
    charToHexMap["▗"]=0x73B

    charToHexMap["▙"]=0x1B9FFF
    charToHexMap["▛"]=0x1FFFE6
    charToHexMap["▜"]=0x1FFF3B
    charToHexMap["▟"]=0xCFFFF

intializeMaps()

def charToHex(char):
    if char in charToHexMap:
        return charToHexMap[char]
    else:
        return 0

def hexToChar(hex):
    if hex in hexToCharMap:
        return hexToCharMap[hex]
    else: # find closest match
        # If this is slow, do more fancy bit-wise math
        minDiff = 64
        minChar = None
        for key,value in hexToCharMap.items():
            count = bin(hex ^ key).count("1")
            if count<minDiff:
                minDiff = count
                minChar = value
        return minChar

def orChars(char1,char2):
    #if char1=='╌' and char2=='╎' or \
    #   char2=='╌' and char1=='╎':
    #print("char1="+char1+" char2="+char2+" hex1="+str(charToHex(char1))+" hex2="+str(charToHex(char2))+" result="+str(charToHex(char1) | charToHex(char2))+" char='"+hexToChar( charToHex(char1) | charToHex(char2) ))
    return hexToChar( charToHex(char1) | charToHex(char2) )

def andChars(char1,char2):
    #if char1=='╌' and char2=='╎' or \
    #   char2=='╌' and char1=='╎':
    #print("char1="+char1+" char2="+char2+" hex1="+str(charToHex(char1))+" hex2="+str(charToHex(char2))+" result="+str(charToHex(char1) & charToHex(char2))+" char='"+hexToChar( charToHex(char1) & charToHex(char2) ))
    return hexToChar( charToHex(char1) & charToHex(char2) )

class Context:
    def __init__(self):
        self.invalidatedRect = Rect()

    def clearWindow(self):
        raise Exception("Called abstract method")

    def readChar(self,x,y):
        raise Exception("Called abstract method")

    def getMaxXy(self):
        raise Exception("Called abstract method")

    def _writeString(self,x,y,text,bold=False,reverse=False):
        raise Exception("Called abstract method")

    def writeString(self,x,y,text,bold=False,reverse=False):
        maxX, maxY = self.getMaxXy()
        #print("trying to write   '"+text+"' at x="+str(x)+" y="+str(y)+" maxX="+str(maxX)+" maxY="+str(maxY))
        
        # Check if row is even on the screen
        if y<0 or y>=maxY:
            return

        # Trim off left if bleeds off left side
        if x<0:
            text = text[-x:]
            x=0

        debugText=text
        # Trim off right if bleeds off of right side
        textLen = len(text)
        right = x+textLen
        if right>maxX:
            trim = -(right-maxX+1)
            text = text[:trim]

        if text=='':
            return

        self._writeString(x,y,text,bold,reverse)

    def writeJustifiedText(self,x,y,text,justification,bold=False,reverse=False,boundingRect=None):
        executeLambdaForJustifiedText(x,y,text,justification, lambda x,y,text : self.writeString(x,y,text) )

    def invalidateRect(self,rect=None):
        if rect is None:
            maxX,maxY = self.getMaxXy()
            #rect = Rect(0,0,maxX+1,maxY+1)
            rect = Rect(0,0,maxX,maxY)
        self.invalidatedRect.unionWith(rect)

    def validateAll(self):
        self.invalidatedRect = Rect()

    def getInvalidatedRect(self):
        return self.invalidatedRect

    def clearRect(self,rect=None):
        if rect == None:
            self.clearWindow()
        elif not rect.isNullRect() :
            for i in range(0,rect.width()):
                for j in range(0,rect.height()):
                    self.writeString(rect.x()+i,rect.y()+j," ")

    def orChar(self,x,y,char,isBold=False):
        if self.invalidatedRect.isInsidePoint(Point(x,y)):
            #charOrd = ord(char)
            #if (charOrd>=0x2500 and charOrd<=0x254b) or (charOrd>=0x2574 and charOrd<=0x257f):
            existing = self.readChar(x,y)
            if existing!=' ' and char in charToHexMap:
                #if is a box char
                writeMe = orChars(existing,char)
            else:
                writeMe = char
            self.writeString(x,y,writeMe,isBold)

    def andChar(self,x,y,char,isBold=False):
        if self.invalidatedRect.isInsidePoint(Point(x,y)):
            if char!="█":
                existing = self.readChar(x,y)
                writeMe = andChars(existing,char)
                self.writeString(x,y,writeMe,isBold)

    verticalLines = [ ['│', '╎'],
                      ['┃', '╏'] ]

    def drawVerticalLine(self,x,fro,to,thickness,style,isBold):
    #def drawVerticalLine(self,x,fro=0,to=None,isBold=False):
        maxY = max(fro,to)
        minY = min(fro,to)
        ch = Context.verticalLines[int(thickness)][int(style)]
        for i in range(minY,maxY+1):
            self.orChar(x,i,ch,isBold)

    horizontalLines = [ ['─', '╌'],
                        ['━', '╍'] ]

    def drawHorizontalLine(self,y,fro,to,thickness,style,isBold):
    #def drawHorizontalLine(self,y,fro=0,to=None,isBold=False):
        maxX = max(fro,to)
        minX = min(fro,to)
        ch = Context.horizontalLines[int(thickness)][int(style)]
        for i in range(minX,maxX+1):
            self.orChar(i,y,ch,isBold)

    def drawFilledBox(self,rect,selected):
        l = rect.l
        r = rect.r
        t = rect.t
        b = rect.b
        self.andChar(l,t,'▛',selected)
        self.andChar(r,t,'▜',selected)
        self.andChar(l,b,'▙',selected)
        self.andChar(r,b,'▟',selected)
        for i in range(l+1,r):
            self.andChar(i,t,'▀',selected)
            self.andChar(i,b,'▄',selected)
        for i in range(t+1,b):
            self.andChar(l,i,'▌',selected)
            self.andChar(r,i,'▐',selected)
        for i in range(t+1,b):
            for j in range(l+1,r):
                self.andChar(j,i,' ',selected) 
        self.orChar(l,t,'┌',selected)
        self.orChar(r,t,'┐',selected)
        self.orChar(l,b,'└',selected)
        self.orChar(r,b,'┘',selected)
        self.drawHorizontalLine(t,l+1,r-1,Thickness.THIN,Style.SOLID,selected)
        self.drawHorizontalLine(b,l+1,r-1,Thickness.THIN,Style.SOLID,selected)
        self.drawVerticalLine(l,t+1,b-1,Thickness.THIN,Style.SOLID,selected)
        self.drawVerticalLine(r,t+1,b-1,Thickness.THIN,Style.SOLID,selected)

