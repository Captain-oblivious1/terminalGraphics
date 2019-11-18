from Components import *

class ConnectorComponent(Component):
    # I wish there were arrows and triangles that lined up with blocks
    noneMap =     { Side.TOP:"┴", Side.LEFT:"┤", Side.RIGHT:"├", Side.BOTTOM:"┬" }
    arrowMap =    { Side.TOP:"∨", Side.LEFT:">", Side.RIGHT:"<", Side.BOTTOM:"∧" }
    triangleMap = { Side.TOP:"▽", Side.LEFT:"▷", Side.RIGHT:"◁", Side.BOTTOM:"△" }

    offsetMap = { Side.TOP:Point(0,-1), Side.LEFT:Point(-1,0), Side.RIGHT:Point(1,0), Side.BOTTOM:Point(0,1) }

    def __init__(self,connectorElement):
        Component.__init__(self,connectorElement)
        self.connectorCache = None

    class ConnectorCache:

        class Direction(Enum):
            HORIZONTAL=0
            VERTICAL=1

        class ConnectionPoint:
            def __init__(self,connection):

                self.connectionPosition = self.getConnectorPosition(connection)
                offset = ConnectorComponent.offsetMap[ connection.side ]

                if connection.end == End.NONE:
                    charMap = ConnectorComponent.noneMap
                else:
                    self.connectionPosition += offset # need to dedicate a char to draw the arrow

                    if connection.end == End.ARROW:
                        charMap = ConnectorComponent.arrowMap
                    else:
                        charMap = ConnectorComponent.triangleMap

                self.char = charMap[ connection.side ]
                self.linePosition = self.connectionPosition + offset

            def getConnectorPosition(self,connection):
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

                return Point(x,y)

            def draw(self,context):
                connectionPosition = self.connectionPosition
                context.addString(connectionPosition.x,connectionPosition.y,self.char)

            def getLinePosition(self):
                return self.linePosition

            def getRect(self):
                rect = Rect()
                rect.includePoint(self.connectionPosition)
                rect.includePoint(self.linePosition)
                return rect

        class Segment:
            def __init__(self,direction,pos,fro,to):
                self.direction = direction
                self.pos = pos
                self.fro = fro
                self.to = to
                self.isSelected = False

            def draw(self,context):
                if self.direction == ConnectorComponent.ConnectorCache.Direction.HORIZONTAL:
                    function = context.drawHorizontalLine
                else:
                    function = context.drawVerticalLine
                function(self.pos,self.fro,self.to,False,self.isSelected)

            def getRect(self):
                if self.direction==ConnectorComponent.ConnectorCache.Direction.HORIZONTAL:
                    return Rect(self.fro,self.pos,self.to-self.fro,1)
                else:
                    return Rect(self.pos,self.fro,1,self.to-self.fro)

        class Elbow:
            def __init__(self,x,y,char):
                self.x = x
                self.y = y
                self.char = char

            def getRect(self):
                retMe = Rect()
                retMe.includePoint( Point(x,y) )
                return retMe

            def draw(self,context):
                context.addString(self.x,self.y,self.char)

        def __init__(self,connectorElement):
            self.segments = []
            self.elbows = []
            fromConnection = connectorElement.fromConnection
            toConnection = connectorElement.toConnection
            self.fromConnection = ConnectorComponent.ConnectorCache.ConnectionPoint(fromConnection)
            self.toConnection = ConnectorComponent.ConnectorCache.ConnectionPoint(toConnection)

            startPos = self.fromConnection.connectionPosition
            endPos = self.toConnection.connectionPosition
            #startPos = self.fromConnection.getLinePosition()
            #endPos = self.toConnection.getLinePosition()

            x = startPos.x
            y = startPos.y

            controlPoints = connectorElement.controlPoints.copy()
            if isHorizontal(toConnection.side):
                controlPoints.append(endPos.y)
                controlPoints.append(endPos.x)
            else:
                controlPoints.append(endPos.x)
                controlPoints.append(endPos.y)

            horizontalOrienation = isHorizontal(connectorElement.fromConnection.side)
            if fromConnection.side==Side.RIGHT:
                direction = 0
            elif fromConnection.side==Side.BOTTOM:
                direction = 1
            elif fromConnection.side==Side.LEFT:
                direction = 2
            elif fromConnection.side==Side.TOP:
                direction = 3

            firstElbow = True
            for controlPoint in controlPoints:
                if horizontalOrienation:
                    if controlPoint>x:
                        newDirection = 0
                    else:
                        newDirection = 2
                    self.segments.append( ConnectorComponent.ConnectorCache.Segment(ConnectorComponent.ConnectorCache.Direction.HORIZONTAL,y,x,controlPoint) )
                    #context.drawHorizontalLine(y,x,controlPoint,False,isSelected)
                    nextX=controlPoint
                    nextY=y
                else:
                    if controlPoint>y:
                        newDirection = 1
                    else:
                        newDirection = 3
                    self.segments.append( ConnectorComponent.ConnectorCache.Segment(ConnectorComponent.ConnectorCache.Direction.VERTICAL,x,y,controlPoint) )
                    #context.drawVerticalLine(x,y,controlPoint,False,isSelected)
                    nextX=x
                    nextY=controlPoint
                #context.addString(x,y,ConnectorComponent.turnSymbol[direction][newDirection])
                if firstElbow:
                    firstElbow = False
                else:
                    self.elbows.append( ConnectorComponent.ConnectorCache.Elbow(x,y,ConnectorComponent.turnSymbol[direction][newDirection]) )
                x=nextX
                y=nextY
                direction = newDirection
                horizontalOrienation = 1 - horizontalOrienation

            #context.addString(x,y,ConnectorComponent.turnSymbol[direction][newDirection])
            #self.elbows.append( Elbow(x,y,ConnectorComponent.turnSymbol[direction][newDirection])

        def getRect(self):
            rect = Rect()
            for seg in self.segments:
                rect.unionWith(seg.getRect())

            rect.unionWith(self.fromConnection.getRect())
            rect.unionWith(self.toConnection.getRect())
            return rect

        def draw(self,context):
            self.fromConnection.draw(context)
            self.toConnection.draw(context)
            for seg in self.segments:
                seg.draw(context)
            for elbow in self.elbows:
                elbow.draw(context)

    def getConnectorCache(self):
        if self.connectorCache==None:
            self.connectorCache = ConnectorComponent.ConnectorCache(self.element)
        return self.connectorCache


    def drawConnector(self,context,connection):
        x,y = getConnectorPosition(connection)

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
        self.getConnectorCache().draw(context)
        #fromConnection = self.element.fromConnection
        #toConnection = self.element.toConnection
        #isSelected = self.isSelected

        #x,y = self.drawConnector(context,fromConnection)
        #endX,endY = self.drawConnector(context,toConnection)

        #controlPoints = self.element.controlPoints.copy()
        #if isHorizontal(toConnection.side):
        #    controlPoints.append(endY)
        #    controlPoints.append(endX)
        #else:
        #    controlPoints.append(endX)
        #    controlPoints.append(endY)

        #horizontalOrienation = isHorizontal(fromConnection.side)
        #if fromConnection.side==Side.RIGHT:
        #    direction = 0
        #elif fromConnection.side==Side.BOTTOM:
        #    direction = 1
        #elif fromConnection.side==Side.LEFT:
        #    direction = 2
        #elif fromConnection.side==Side.TOP:
        #    direction = 3

        #for controlPoint in controlPoints:
        #    if horizontalOrienation:
        #        if controlPoint>x:
        #            newDirection = 0
        #        else:
        #            newDirection = 2
        #        context.drawHorizontalLine(y,x,controlPoint,False,isSelected)
        #        nextX=controlPoint
        #        nextY=y
        #    else:
        #        if controlPoint>y:
        #            newDirection = 1
        #        else:
        #            newDirection = 3
        #        context.drawVerticalLine(x,y,controlPoint,False,isSelected)
        #        nextX=x
        #        nextY=controlPoint
        #    context.addString(x,y,ConnectorComponent.turnSymbol[direction][newDirection])
        #    x=nextX
        #    y=nextY
        #    direction = newDirection
        #    horizontalOrienation = 1 - horizontalOrienation

        #context.addString(x,y,ConnectorComponent.turnSymbol[direction][newDirection])

    def isOnMe(self,x,y):
        return False

    def move(self,point):
        pass

    def getRect(self):
        connectorCache = self.getConnectorCache()
        return connectorCache.getRect()


