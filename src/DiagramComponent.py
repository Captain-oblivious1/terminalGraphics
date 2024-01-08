from Component import *
from Menu import *
from PathComponent import *
from TextComponent import *
from RectComponent import *

class DiagramComponent(Component):
    def __init__(self,editor,element):
        super().__init__(None)
        self.editor = editor
        self.element = element
        self.components = {}
        self.invalidatedRect = Rect()
        self.selectionRect = None
        self.createDiagramComponent(element)
        self.menu = None

    def addElement(self,element,addToElement=True):
        if type(element) is TextElement:
            component = TextComponent(self,element)
        elif type(element) is PathElement:
            component = PathComponent(self,element)
        elif type(element) is RectElement:
            component = RectComponent(self,element)
        else:
            raise Exception("Unsupported element type '"+element.type+"'")

        if addToElement:
            self.element.elements.append(element)
        self.components[element] = component

    def invalidateAll(self):
        for element in self.element.elements:
            component = self.components[element]
            component.invalidate()

    def getEditor(self):
        return self.editor

    def createDiagramComponent(self,diagramElement):
        for element in diagramElement.elements:
            self.addElement(element,False)

    #def invalidateRect(self,rect):
    #    self.invalidatedRect.unionWith(rect)

   #def validateAll(self):
    #    self.invalidatedRect = Rect()

    #def getInvalidatedRect(self):
    #    return self.invalidatedRect

    #def allInvalidatedComponents(self):
    #    return self.invalidatedComponents

    def draw(self,context):
        invalidatedRect = context.getInvalidatedRect()
        #print("context.rect="+str(context.invalidatedRect))
        context.clearRect(invalidatedRect)

        #print("About to draw all components")
        for element in self.element.elements:
            component = self.components[element]
            #print("   Testing component intersection for="+str(component))
            #print("testing intesection of "+str(component.getRect())+" and "+str(invalidatedRect))
            if component.getRect().doesIntersect(invalidatedRect):
                #print("Found intersection")
                #print("drawing component="+str(component))
                component.draw(context)

        if self.selectionRect!=None:
            for col in range(self.selectionRect.l,self.selectionRect.r):
                for row in range(self.selectionRect.t,self.selectionRect.b):
                    char = context.readChar(col,row)
                    #print("char='"+char+"' ord="+hex(ord(char)))
                    context.writeString(col,row,char,False,True)

        if self.menu!=None and self.menu.getRect().doesIntersect(invalidatedRect):
            self.menu.draw(context)

    def children(self):
        return self.components.values()

    def setSelectionRect(self,rect):
        self.selectionRect = rect

    @staticmethod
    def allSelectedComponent(component,theSet):
        if component.isSelected():
            theSet.add(component)
        for child in component.children():
            DiagramComponent.allSelectedComponent(child,theSet)

    def allSelected(self):
        returnMe = set()
        DiagramComponent.allSelectedComponent(self,returnMe)
        return returnMe

    def componentAt(self,point):
        #print("testing at point="+str(point))  (51,17)
        #for child in component.children():
        #    found = DiagramComponent.componentAt(child,point)
        #    #print("testing child="+str(child)+" found="+str(found))
        #    if found!=None:
        #        return found
        if self.menu!=None and self.menu.getRect().isInsidePoint(point):
            return self.menu

        for child in self.children():
            if child.getRect().isInsidePoint(point) and child.isOnMe(point):
                return child

        return None

    def isOnMe(self, point):
        return False

    def moveSelectedToFront(self):
        topList = []
        bottomList = []
        selected = self.allSelected()
        for element in self.element.elements:
            component = self.components[element]
            if component in selected:
                bottomList.append(element)
                component.invalidate()
            else:
                topList.append(element)
        self.element.elements = topList + bottomList

    def moveSelectedToBack(self):
        topList = []
        bottomList = []
        selected = self.allSelected()
        for element in self.element.elements:
            component = self.components[element]
            if component in selected:
                topList.append(element)
                component.invalidate()
            else:
                bottomList.append(element)
        self.element.elements = topList + bottomList

    def moveSelectedForward(self):
        pass

    def moveSelectedBackward(self):
        pass

    def showMenu(self,menu):
        if self.menu is not None:
            self.menu.invalidate()
        self.menu = menu
        menu.invalidate()

    def clearMenu(self):
        self.menu = None
