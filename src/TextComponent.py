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
        rect = rectForJustifiedText(location.x,location.y,element.text,element.justification)
        if self.textEditor is not None:
            rect.r += 1
        return rect

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

        options += [""]
        just = self.element.justification 
        if just!=Justification.LEFT:
            options += ["left justify"]
        if just!=Justification.CENTER:
            options += ["center justify"]
        if just!=Justification.RIGHT:
            options += ["right justify"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))
    
    def menuResult(self,menu):
        option = menu.getSelectedOption()
        if option=="edit":
            self.textEditor = TextEditor(self.element.text,self.element.justification,self)
            editor = self.getEditor()
            editor.addKeyListener(self.textEditor)
        elif option=="stop editing":
            self.stopEditing()

        else:
            halfWidth = longestLineFor(self.element.text)/2
            oldJust = self.element.justification
            location = self.element.location
            x = location.x
            if oldJust == Justification.LEFT:
                center = x + halfWidth
            elif oldJust == Justification.CENTER:
                center = x
            elif oldJust == Justification.RIGHT:
                center = x - halfWidth
            else:
                raise Exception("Justification unset")

            if option=="left justify":
                just = Justification.LEFT
                x = center - halfWidth
            elif option=="center justify":
                just = Justification.CENTER
                x = center
            elif option=="right justify":
                just = Justification.RIGHT
                x = center + halfWidth
            else:
                just = None

            if just is not None:
                self.invalidate()
                self.element.justification = just
                self.element.location.x = int(x)
                self.invalidate()

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
