import sys
import curses
from Model import *
from curses import wrapper

class Context:
    def __init__(self,window):
        self.window = window

    def addString(self,x,y,text):
        self.window.addstr(y,x,text)

    def readChar(self,x,y):
        return chr(self.window.inch(y,x))
        #return self.window.inch(y,x)

    def fillChar(self,x,y,width,height,char):
        for i in range(0,width):
            for j in range(0,height):
                self.addString(x+i,y+j,char)

    def drawVerticalLine(self,x):
        maxY,_ = self.window.getmaxyx()
        for i in range(0,maxY-1):
            self.addString(x,i,"│")


class Component:
    def __init__(self, element):
        self.element = element

class TextBoxComponent(Component):
    topMap = {"│":"┴"}
    bottomMap = {"│":"┬"}
    def __init__(self,textBoxElement):
        Component.__init__(self,textBoxElement)

    def _drawBorderChar(self,context,x,y,mapping,default):
        existing = context.readChar(x,y)
        if existing in mapping:
            char = mapping[existing]
        else:
            char = default
        context.addString(x,y,char)

    def draw(self,context):
        x = self.element.x
        y = self.element.y
        width = self.element.width
        height = self.element.height
        height -= 1
        width -= 1
        bottom = y+height
        right = x+width

        for i in range(1,width):
            self._drawBorderChar(context,x+i,y,TextBoxComponent.topMap,"─")
            #context.addString(x+i,y,"─")
            self._drawBorderChar(context,x+i,bottom,TextBoxComponent.bottomMap,"─")
            #context.addString(x+i,bottom,"─")

        for i in range(1,height):
            context.addString(x,y+i,"│")
            context.addString(right,y+i,"│")

        context.addString(x,y,"┌")
        context.addString(right,y,"┐")
        context.addString(x,bottom,"└")
        context.addString(right,bottom,"┘")

        context.addString(x,y,"┌")
        context.fillChar(x+1,y+1,width-1,height-1," ")

        width -= 1
        row = y+1
        for line in self.element.lines:
            lineLength = len(line.text)
            if line.justification == Justification.LEFT:
                col = x + 1
            elif line.justification == Justification.CENTER:
                col = x + int(width/2-lineLength/2) + 1
            elif line.justification == Justification.RIGHT:
                col = x + width - lineLength + 1

            context.addString(col,row,line.text)
            row += 1

        #print("readChar='" + str(context.readChar(x,y)) + "'")

class Editor:
    def __init__(self):
        pass

    def run(self):
        screen = curses.initscr()
        curses.curs_set(0)
        screen.clear()

        context = Context(screen)

        context.drawVerticalLine(25)
        textBoxElement = testTextBox()
        textBoxElement.x = 20
        textBoxElement.y = 10
        textBoxComponent = TextBoxComponent(textBoxElement)
        textBoxComponent.draw(context)
        screen.refresh()

        screen.getch()
        #curses.napms(2000)

        curses.endwin()

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])
    def get_text(self,beg=0,end=-1):
        return '\n'.join(self.text.split('\n')[beg:end])

def myMain(stdscr):
    mystdout = StdOutWrapper()
    sys.stdout = mystdout
    sys.stderr = mystdout

    try:
        editor = Editor() 
        editor.run()

    finally:

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdout.write(mystdout.get_text())
        sys.stdout.write("\n")


wrapper(myMain)
