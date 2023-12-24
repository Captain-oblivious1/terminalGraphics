from Component import *
from Menu import *

class DiagramComponent(Component):
    def __init__(self,editor,diagramElement):
        super().__init__(None)
        self.editor = editor
        self.diagramElement = diagramElement
        self.components = []
        self.invalidatedRect = Rect()
        self.selectionRect = None

    def invalidateAll(self):
        for component in self.components:
            component.invalidate()

    def getEditor(self):
        return self.editor

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
        context.clearRect(invalidatedRect)

        #print("About to draw all components")
        for component in self.components:
            #print("   Testing component intersection for="+str(component))
            #print("testing intesection of "+str(component.getRect())+" and "+str(invalidatedRect))
            if component.getRect().doesIntersect(invalidatedRect):
                #print("Found intersection")
                component.draw(context)

        if self.selectionRect!=None:
            for col in range(self.selectionRect.l,self.selectionRect.r):
                for row in range(self.selectionRect.t,self.selectionRect.b):
                    char = context.readChar(col,row)
                    #print("char='"+char+"' ord="+hex(ord(char)))
                    context.addString(col,row,char,False,True)

    def children(self):
        return self.components

    def setSelectionRect(self,rect):
        self.selectionRect = rect

    def allSelectedComponent(component,theSet):
        if component.isSelected():
            theSet.add(component)
        for child in component.children():
            DiagramComponent.allSelectedComponent(child,theSet)

    def allSelected(self):
        returnMe = set()
        DiagramComponent.allSelectedComponent(self,returnMe)
        return returnMe

    def componentAt(component,point):
        #print("testing at point="+str(point))  (51,17)
        for child in component.children():
            found = DiagramComponent.componentAt(child,point)
            #print("testing child="+str(child)+" found="+str(found))
            if found!=None:
                return found

        if component.isOnMe(point):
            return component
        else:
            return None

    def isOnMe(self, point):
        return False

    def showMenu(self,menu):
        self.components.append(menu)
        menu.invalidate()

    def clearMenu(self):
        newComponentList = []
        for component in self.components:
            if not issubclass(type(component),Menu):
                newComponentList.append(component)

        self.components = newComponentList

