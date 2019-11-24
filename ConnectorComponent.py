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

    def setSelected(self,newSelected):
        Component.setSelected(self,newSelected)
        self.getConnectorCache().setSelected(newSelected)

    def children(self):
        return self.getConnectorCache().children()

    def isOnMe(self,point):
        return False

    #def allSelected(self):
    #    return self.getConnectorCache().allSelected()

    def invalidateMe(self,context):
        self.connectorCache = None

    class ConnectorCache:

        class Direction(Enum):
            HORIZONTAL=0
            VERTICAL=1

        class ConnectionPoint(Component):
            def __init__(self,connection):
                Component.__init__(self,connection)

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
                context.addString(connectionPosition.x,connectionPosition.y,self.char,self.selected)

            #def getLinePosition(self):
            #    return self.linePosition

            def getRect(self):
                rect = Rect()
                rect.includePoint(self.connectionPosition)
                #rect.includePoint(self.linePosition)
                return rect

        class Segment(Component):
            def __init__(self,direction,pos,fro,to):
                Component.__init__(self,None)
                self.direction = direction
                self.pos = pos
                self.fro = min(fro,to)+1
                self.to = max(fro,to)-1
                #print("Created segment dir="+str(direction)+" pos="+str(pos)+" from="+str(self.fro)+" to="+str(self.to))

            def draw(self,context):
                if self.direction == ConnectorComponent.ConnectorCache.Direction.HORIZONTAL:
                    function = context.drawHorizontalLine
                else:
                    function = context.drawVerticalLine
                function(self.pos,self.fro,self.to,self.selected)

            def getRect(self):
                if self.direction==ConnectorComponent.ConnectorCache.Direction.HORIZONTAL:
                    return Rect(self.fro,self.pos,self.to-self.fro+1,1)
                else:
                    return Rect(self.pos,self.fro,1,self.to-self.fro+1)

        class Elbow(Component):
            def __init__(self,x,y,char):
                Component.__init__(self,None)
                self.x = x
                self.y = y
                self.char = char
                #print("Created elbow x="+str(x)+" y="+str(y)+" char='"+char+"'")

            def getRect(self):
                retMe = Rect()
                retMe.includePoint( Point(self.x,self.y) )
                return retMe

            def draw(self,context):
                context.addString(self.x,self.y,self.char,self.selected)

        def __init__(self,connectorElement):
            #print("Creating CACHE")
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
                skip = False
                newDirection = direction
                if horizontalOrienation:
                    if controlPoint>x:
                        newDirection = 0
                    elif controlPoint<x:
                        newDirection = 2
                    else:
                        skip = True
                    if not skip:
                        self.segments.append( ConnectorComponent.ConnectorCache.Segment(ConnectorComponent.ConnectorCache.Direction.HORIZONTAL,y,x,controlPoint) )
                    nextX=controlPoint
                    nextY=y
                else:
                    if controlPoint>y:
                        newDirection = 1
                    elif controlPoint<y:
                        newDirection = 3
                    else:
                        skip = True
                    if not skip:
                        self.segments.append( ConnectorComponent.ConnectorCache.Segment(ConnectorComponent.ConnectorCache.Direction.VERTICAL,x,y,controlPoint) )
                    nextX=x
                    nextY=controlPoint

                if firstElbow:
                    firstElbow = False
                else:
                    self.elbows.append( ConnectorComponent.ConnectorCache.Elbow(x,y,ConnectorComponent.turnSymbol[direction][newDirection]) )
                x=nextX
                y=nextY
                direction = newDirection
                horizontalOrienation = 1 - horizontalOrienation

        def setSelected(self,newSelected):
            Component.setSelected(self,newSelected)
            for segment in self.segments:
                segment.selected = True

            for elbow in self.elbows:
                elbow.selected = True

            self.fromConnection.selected = True
            self.toConnection.selected = True

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

        def children(self):
            returnMe = set()
            for segment in self.segments:
                returnMe.add(segment)
            for elbow in self.elbows:
                returnMe.add(elbow)
            returnMe.add(self.fromConnection)
            returnMe.add(self.toConnection)
            return returnMe

    def getConnectorCache(self):
        if self.connectorCache==None:
            self.connectorCache = ConnectorComponent.ConnectorCache(self.element)
            if self.isSelected():
                self.connectorCache.setSelected(True)
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
          [ ["─","╮"," ","╯"], \
            ["╰","│","╯"," "], \
            [" ","╭","─","╰"], \
            ["╭"," ","╮","│"] ]

    def draw(self,context):
        self.getConnectorCache().draw(context)

    def isOnMe(self,point):
        return False

    def move(self,offset):
        element = self.element
        if isHorizontal(element.fromConnection.side):
            xElement = 0
        else:
            xElement = 1

        for arrayElement in range(len(element.controlPoints)):
            if arrayElement%2 == xElement:
                elementOffset = offset.x
            else:
                elementOffset = offset.y
            element.controlPoints[arrayElement] += elementOffset

        self.connectorCache = None

    def getRect(self):
        connectorCache = self.getConnectorCache()
        return connectorCache.getRect()


