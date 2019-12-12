import curses
from Rect import *

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
#    ┌──┰──┬──┐      All box characters can be created by bitwise
#    │21┃20│19│      or-ing any of the following:
# ┌──┼──╂──┼──┼──┐   " " = 0x0
# │18│17┃16│15│14│   "╴" = 0x1C00
# ├──╁──╀──┼──┼──┤   "╸" = 0x39CE0
# │13┃12│11│10│ 9│   "╶" = 0x700
# ┟──╀──┼──┼──╁──┤   "╺" = 0xE738
# ┃ 8│ 7│ 6│ 5┃ 4│   "╵" = 0x88400
# ┖──┼──┼──┼──╂──┘   "╹" = 0x1DCE00
#    │ 3│ 2│ 1┃      "╷" = 0x422
#    └──┴──┴──┚      "╻" = 0xE77
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

    # insert half blocks into charToHexMap for masking stuff (don't put in hextToCharMap)
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
    return hexToChar( charToHex(char1) | charToHex(char2) )

def andChars(char1,char2):
    return hexToChar( charToHex(char1) & charToHex(char2) )

class Context:
    def __init__(self,window):
        self.window = window
        self.invalidatedRect = Rect()

    def addString(self,x,y,text,bold=False,reverse=False):
        if bold or reverse:
            pair = curses.color_pair(1)
            if bold:
                pair |= curses.A_BOLD
            if reverse:
                pair |= curses.A_REVERSE
            self.window.addstr(y,x,text,pair)
        else:
            self.window.addstr(y,x,text)

    def readChar(self,x,y):
        return chr(0xFFFF & self.window.inch(y,x))

    def clearRect(self,rect=None):
        if rect == None:
            self.window.clear()
        elif not rect.isNullRect() :
            for i in range(0,rect.width()):
                for j in range(0,rect.height()):
                    self.addString(rect.x()+i,rect.y()+j," ")

    def orChar(self,x,y,char,isBold=False):
        charOrd = ord(char)
        if (charOrd>=0x2500 and charOrd<=0x254b) or (charOrd>=0x2574 and charOrd<=0x257f):
            #if is a box char
            existing = self.readChar(x,y)
            writeMe = orChars(existing,char)
        else:
            writeMe = char
        self.addString(x,y,writeMe,isBold)

    def andChar(self,x,y,char,isBold=False):
        if char!="█":
            existing = self.readChar(x,y)
            writeMe = andChars(existing,char)
            self.addString(x,y,writeMe,isBold)

    def drawVerticalLine(self,x,fro=0,to=None,isBold=False):
        if to==None:
            to,_ = self.window.getmaxyx()
            to -= 1
        maxY = max(fro,to)
        minY = min(fro,to)
        for i in range(minY,maxY+1):
            self.orChar(x,i,"│",isBold)

    def drawHorizontalLine(self,y,fro=0,to=None,isBold=False):
        if to==None:
            _,to = self.window.getmaxyx()
            to -= 1
        maxX = max(fro,to)
        minX = min(fro,to)
        for i in range(minX,maxX+1):
            self.orChar(i,y,"─",isBold)

    def invalidateComponent(self,component):
        self.invalidateRect(component.getRect())
        if "invalidateMe" in dir(component):
            component.invalidateMe(self)

    def invalidateRect(self,rect):
        self.invalidatedRect.unionWith(rect)

    def validateAll(self):
        self.invalidatedRect = Rect()

    def getInvalidatedRect(self):
        return self.invalidatedRect

    def allInvalidatedComponents(self):
        return self.invalidatedComponents

    def showMenu(self,options,point):
        menu = Menu(options,point)
        menu.draw(self)



