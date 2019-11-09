from Model import *

def isHorizontal(side):
    return side == Side.LEFT or side == Side.RIGHT

class Component:
    def __init__(self, element):
        self.element = element
        self.isSelected = False

    def isOnMe(self, x, y):
        print( "Error.. unimplemented isOnMe() in component "+str(self))

class BoxComponent(Component):
    # These maps are so that when a box is drawn on top of other things, it doesn't look bad
    #
    # So like this:    │        Not this:    │
    #               ┌──┴──┐               ┌─────┐
    #             ──┤ box ├──           ──│ box │──
    #               └──┬──┘               └─────┘
    #                  │                     │
    #
    # So for example, when drawing the top part of a box, and it's about to draw over an existing "│" with "─", it
    # will first check the topMap and find the "│" as a key and will draw the corresponding "┴" value instead.
    #
    #                  ─        │        ┌        ┐        └        ┘        ├        ┤        ┬        ┴        ┼
    topMap    =      {         "│":"┴",                   "└":"┴", "┘":"┴", "├":"┴", "┤":"┴",          "┴":"┴", "┼":"┴"}
    bottomMap =      {         "│":"┬", "┌":"┬", "┐":"┬",                   "├":"┬", "┤":"┬", "┬":"┬",          "┼":"┬"}
    leftMap   =      {"─":"┤",                   "┐":"┤",          "┘":"┤",          "┤":"┤", "┬":"┤", "┴":"┤", "┼":"┤"}
    rightMap  =      {"─":"├",          "┌":"├",          "└":"├",          "├":"├",          "┬":"├", "┴":"├", "┼":"├"}

    topLeftMap     = {"─":"┬", "│":"├",          "┐":"┬", "└":"├", "┘":"┼", "├":"├", "┤":"┼", "┬":"┬", "┴":"┼", "┼":"┼"}
    topRightMap    = {"─":"┬", "│":"┤", "┌":"┬",          "└":"┤", "┘":"┤", "├":"┼", "┤":"┤", "┬":"┬", "┴":"┼", "┼":"┼"}
    bottomLeftMap  = {"─":"┴", "│":"├", "┌":"├", "┐":"┼",          "┘":"┴", "├":"├", "┤":"┼", "┬":"┼", "┴":"┴", "┼":"┼"}
    bottomRightMap = {"─":"┴", "│":"┤", "┌":"┼", "┐":"┤", "└":"┴", "┘":"┘", "├":"┼", "┤":"┤", "┬":"┼", "┴":"┴", "┼":"┼"}

    def __init__(self,boxElement):
        Component.__init__(self,boxElement)

    def _drawBorderChar(self,context,x,y,mapping,default):
        context.drawChar(x,y,mapping,default,self.isSelected)

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
            self._drawBorderChar(context,x+i,bottom,TextBoxComponent.bottomMap,"─")

        for i in range(1,height):
            self._drawBorderChar(context,x,y+i,TextBoxComponent.leftMap,"│")
            self._drawBorderChar(context,right,y+i,TextBoxComponent.rightMap,"│")

        self._drawBorderChar(context,x,y,TextBoxComponent.topLeftMap,"┌")
        self._drawBorderChar(context,right,y,TextBoxComponent.topRightMap,"┐")
        self._drawBorderChar(context,x,bottom,TextBoxComponent.bottomLeftMap,"└")
        self._drawBorderChar(context,right,bottom,TextBoxComponent.bottomRightMap,"┘")

        context.fillChar(x+1,y+1,width-1,height-1," ")

    def isOnMe(self,x,y):
        element = self.element
        myX=element.x
        myY=element.y
        return x>=myX and y>=myY and x<myX+element.width and y<myY+element.height

class TextBoxComponent(BoxComponent):
    def __init__(self,textBoxElement):
        BoxComponent.__init__(self,textBoxElement)

    def draw(self,context):
        BoxComponent.draw(self,context)
        x = self.element.x
        y = self.element.y
        width = self.element.width
        height = self.element.height
        height -= 1
        width -= 2

        row = y+1
        for line in self.element.lines:
            lineLength = len(line.text)
            if line.justification == Justification.LEFT:
                col = x + 1
            elif line.justification == Justification.CENTER:
                col = x + int(width/2-lineLength/2) + 1
            elif line.justification == Justification.RIGHT:
                col = x + width - lineLength + 1

            context.addString(col,row,line.text,self.isSelected)
            row += 1

class ConnectorComponent(Component):
    # I wish there were arrows and triangles that lined up with blocks
    noneMap =     { Side.TOP:"┴", Side.LEFT:"┤", Side.RIGHT:"├", Side.BOTTOM:"┬" }
    arrowMap =    { Side.TOP:"∨", Side.LEFT:">", Side.RIGHT:"<", Side.BOTTOM:"∧" }
    triangleMap = { Side.TOP:"▽", Side.LEFT:"▷", Side.RIGHT:"◁", Side.BOTTOM:"△" }

    offsetMap = { Side.TOP:(0,-1), Side.LEFT:(-1,0), Side.RIGHT:(1,0), Side.BOTTOM:(0,1) }

    def __init__(self,connectorElement):
        Component.__init__(self,connectorElement)

    def drawConnector(self,context,connection):
        element = connection.element
        if connection.side == Side.TOP:
            x = int(element.x + element.width * connection.where)
            y = element.y
        elif connection.side == Side.LEFT:
            x = element.x
            y = int(element.y + element.height * connection.where)
        elif connection.side == Side.RIGHT:
            x = element.x + element.width - 1
            y = int(element.y + element.height * connection.where)
        elif connection.side == Side.BOTTOM:
            x = int(element.x + element.width * connection.where)
            y = element.y + element.height - 1
        else:
            raise "invalid side"

        offX, offY = ConnectorComponent.offsetMap[ connection.side ]

        if connection.end == End.NONE:
            context.addString(x,y,ConnectorComponent.noneMap[ connection.side ])
            return (x + offX, y + offY)
        else:
            x += offX
            y += offY

            if connection.end == End.ARROW:
                theMap = ConnectorComponent.arrowMap
            else:
                theMap = ConnectorComponent.triangleMap

            context.addString(x,y,theMap[ connection.side ])

            return (x + offX, y + offY)

    turnSymbol = \
          [ ["─","╮","X","╯"], \
            ["╰","│","╯","X"], \
            ["X","╭","─","╰"], \
            ["╭","X","╮","│"] ]

    def draw(self,context):
        fromConnection = self.element.fromConnection
        toConnection = self.element.toConnection
        isSelected = self.isSelected

        x,y = self.drawConnector(context,fromConnection)
        endX,endY = self.drawConnector(context,toConnection)

        controlPoints = self.element.controlPoints.copy()
        if isHorizontal(toConnection.side):
            controlPoints.append(endY)
            controlPoints.append(endX)
        else:
            controlPoints.append(endX)
            controlPoints.append(endY)

        horizontalOrienation = isHorizontal(fromConnection.side)
        if fromConnection.side==Side.RIGHT:
            direction = 0
        elif fromConnection.side==Side.BOTTOM:
            direction = 1
        elif fromConnection.side==Side.LEFT:
            direction = 2
        elif fromConnection.side==Side.TOP:
            direction = 3

        for controlPoint in controlPoints:
            if horizontalOrienation:
                if controlPoint>x:
                    newDirection = 0
                else:
                    newDirection = 2
                context.drawHorizontalLine(y,x,controlPoint,False,isSelected)
                nextX=controlPoint
                nextY=y
            else:
                if controlPoint>y:
                    newDirection = 1
                else:
                    newDirection = 3
                context.drawVerticalLine(x,y,controlPoint,False,isSelected)
                nextX=x
                nextY=controlPoint
            context.addString(x,y,ConnectorComponent.turnSymbol[direction][newDirection])
            x=nextX
            y=nextY
            direction = newDirection
            horizontalOrienation = 1 - horizontalOrienation

        context.addString(x,y,ConnectorComponent.turnSymbol[direction][newDirection])

    def isOnMe(self,x,y):
        return False

class DiagramComponent(Component):
    def __init__(self,diagramElement):
        Component.__init__(self,diagramElement)
        self.components = []

    def draw(self,context):
        for component in self.components:
            component.draw(context)

    def allComponents(self):
        return self.components


