from Component import *

from Rect import *
from Menu import *
from Model import *
from Util import *
from TextEditor import *

class TextComponent(Component):
    def __init__(self,parent,element):
        super().__init__(parent)
        self.element = element
        self.textEditor = None

    def getRect(self):
        element = self.element
        location = element.location
        return rectForJustifiedText(location.x,location.y,element.text,element.justification)

    def draw(self,context):
        element = self.element
        location = element.location
        context.writeJustifiedText(location.x,location.y,element.text,element.justification)
        if self.textEditor is not None:
            cursor = self.textEditor.cursorOffset() + self.element.location
            ch = context.readChar(cursor.x,cursor.y)
            context.writeString(cursor.x,cursor.y,ch,False,True)

    class OnMe:
        def __init__(self,point):
            self.point = point
            self.isOnMe = False

        def isOnLine(self,l,y,text):
            r = l + len(text)
            if self.point.y==y and self.point.x>=l and self.point.x<r:
                self.isOnMe = True

    # Default is for entier rectangle to be true
    def isOnMe(self,point):
        element = self.element
        location = element.location
        onMe = TextComponent.OnMe(point)
        executeLambdaForJustifiedText(location.x,location.y,element.text,element.justification, onMe.isOnLine)
        return onMe.isOnMe

    def move(self,fromPoint,offset,context):
        self.element.location += offset

    def showContextMenu(self,point,context):
        if self.textEditor is not None:
            options = ["stop editing"]
        else:
            options = ["edit"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))
    
    def menuResult(self,menu):
        if menu.getSelectedOption()=="edit":
            self.textEditor = TextEditor(self.element.text,self.element.justification,self)
        else:
            self.textEditor = None
        editor = self.getEditor()
        if self.textEditor is not None:
            editor.addKeyListener(self.textEditor)
        else:
            self.stopEditing()

    def keyEvent(self,event):
        self.invalidate()
        self.textEditor.keyEvent(event)
        self.invalidate()

    def changeText(self,text):
        self.invalidate()
        self.element.text = text
        self.invalidate()

    def stopEditing(self):
        self.getEditor().removeKeyListener(self.textEditor)
        self.textEditor = None
        self.invalidate()
