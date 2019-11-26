from Components import *
from Util import *

class ConnectorComponent(Component):
    # I wish there were arrows and triangles that lined up with blocks
    noneMap =     { Direction.UP:"┴", Direction.LEFT:"┤", Direction.RIGHT:"├", Direction.DOWN:"┬" }
    arrowMap =    { Direction.UP:"∨", Direction.LEFT:">", Direction.RIGHT:"<", Direction.DOWN:"∧" }
    triangleMap = { Direction.UP:"▽", Direction.LEFT:"▷", Direction.RIGHT:"◁", Direction.DOWN:"△" }

    offsetMap = { Direction.UP:Point(0,-1), Direction.LEFT:Point(-1,0), Direction.RIGHT:Point(1,0), Direction.DOWN:Point(0,1) }

    def __init__(self,connectorElement):
        self.connectorCache = None

    #def setSelected(self,newSelected):
    #    Component.setSelected(self,newSelected)
    #    self.getConnectorCache().setSelected(newSelected)

    def isOnMe(self,point):
        return False

    #def allSelected(self):
    #    return self.getConnectorCache().allSelected()

    def invalidateMe(self,context):
        self.connectorCache = None

    class WhereReference:
        def __init__(self,connection):
            self.connection = connection

        def get(self):
            connection = self.connection
            element = connection.element
            if isHorizontal(connection.side):
                return element.y + int(element.height * connection.where)
            else:
                return element.x + int(element.width * connection.where)

        def set(self,val):
            pass

    class EdgeReference:
        def __init__(self,connection):
            self.connection = connection

        def get(self):
            connection = self.connection
            element = connection.element
            if connection.side == Direction.UP:
                return element.y
            elif connection.side == Direction.LEFT:
                return element.x
            elif connection.side == Direction.RIGHT:
                return element.x + element.width
            elif connection.side == Direction.DOWN:
                return element.y + element.height
            else:
                raise "WTF"

        def set(self,val):
            pass

    class Orientation(Enum):
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
            if connection.side == Direction.UP:
                x = int(element.x + element.width * connection.where)
                y = element.y
            elif connection.side == Direction.LEFT:
                x = element.x
                y = int(element.y + element.height * connection.where)
            elif connection.side == Direction.RIGHT:
                x = element.x + element.width - 1
                y = int(element.y + element.height * connection.where)
            elif connection.side == Direction.DOWN:
                x = int(element.x + element.width * connection.where)
                y = element.y + element.height - 1
            else:
                raise "invalid side"

            return Point(x,y)

        def draw(self,context):
            connectionPosition = self.connectionPosition
            context.addString(connectionPosition.x,connectionPosition.y,self.char,self.selected)

        def getRect(self):
            rect = Rect()
            rect.includePoint(self.connectionPosition)
            #rect.includePoint(self.linePosition)
            return rect

    class Segment(Component):

        def __init__(self,fromRef,posRef,toRef,orientation):
            Component.__init__(self,None)
            self.fromRef = fromRef
            self.posRef = posRef
            self.toRef = toRef
            self.orientation = orientation

        def draw(self,context):
            if self.orientation == ConnectorComponent.Orientation.HORIZONTAL:
                function = context.drawHorizontalLine
            else:
                function = context.drawVerticalLine
            #function(self.pos,self.fro,self.to,self.selected)
            pos = self.posRef.get()
            rawFrom = self.fromRef.get()
            rawTo = self.toRef.get()
            fro = min(rawFrom,rawTo)
            to = max(rawFrom,rawTo)
            if to-fro>1:
                function(pos,fro+1,to-1,self.selected)

        def getRect(self):
            pos = self.posRef.get()
            rawFrom = self.fromRef.get()
            rawTo = self.toRef.get()
            fro = min(rawFrom,rawTo)
            to = max(rawFrom,rawTo)
            if to-fro<=1:
                return Rect()
            elif self.orientation == ConnectorComponent.Orientation.HORIZONTAL:
                return Rect(fro+1,pos,to-fro-1,1)
            else:
                return Rect(pos,fro+1,1,to-fro-1)

        def move(self,offset):
            pass

    class Elbow(Component):

        turnSymbol = \
              [ ["─","╮"," ","╯"], \
                ["╰","│","╯"," "], \
                [" ","╭","─","╰"], \
                ["╭"," ","╮","│"] ]

        def __init__(self,beforeSegment,afterSegment):
            Component.__init__(self,None)
            self.beforeSegment = beforeSegment
            self.afterSegment = afterSegment

        def getPoint(self):

            beforePos = self.beforeSegment.posRef.get()
            afterPos = self.afterSegment.posRef.get()

            if self.beforeSegment.orientation==ConnectorComponent.Orientation.VERTICAL:
                x = beforePos
            else:
                y = beforePos

            if self.afterSegment.orientation==ConnectorComponent.Orientation.VERTICAL:
                x = afterPos
            else:
                y = afterPos

            return Point(x,y)

        def getInfo(self):
            point = self.getPoint()

            beforeSum = self.beforeSegment.fromRef.get() + self.beforeSegment.toRef.get()
            afterSum = self.afterSegment.fromRef.get() + self.afterSegment.toRef.get()

            if self.beforeSegment.orientation==ConnectorComponent.Orientation.VERTICAL:
                if beforeSum < 2*point.y:
                    beforeDirection = Direction.DOWN
                elif beforeSum > 2*point.y:
                    beforeDirection = Direction.UP
                else:
                    beforeDirection = Direction.RIGHT if beforeSum<afterSum else Direction.LEFT
            else:
                if beforeSum < 2*point.x:
                    beforeDirection = Direction.RIGHT
                elif beforeSum > 2*point.x:
                    beforeDirection = Direction.LEFT
                else:
                    beforeDirection = Direction.DOWN if beforeSum<afterSum else Direction.UP

            if self.afterSegment.orientation==ConnectorComponent.Orientation.VERTICAL:
                if afterSum < 2*point.y:
                    afterDirection = Direction.UP
                elif afterSum > 2*point.y:
                    afterDirection = Direction.DOWN
                else:
                    afterDirection = Direction.RIGHT if beforeSum<afterSum else Direction.LEFT
            else:
                if afterSum < 2*point.x:
                    afterDirection = Direction.LEFT
                elif afterSum > 2*point.x:
                    afterDirection = Direction.RIGHT
                else:
                    afterDirection = Direction.DOWN if beforeSum<afterSum else Direction.UP

            return point,ConnectorComponent.Elbow.turnSymbol[beforeDirection.value][afterDirection.value]

        def getRect(self):
            return Rect().includePoint( self.getPoint() )

        def draw(self,context):
            point,char = self.getInfo()
            context.addString(point.x,point.y,char,self.selected)

    def __init__(self,connectorElement):
        Component.__init__(self,connectorElement)
        self.createChildren(connectorElement)

    def createChildren(self,connectorElement):
        self.segments = []
        self.elbows = []
        fromConnection = connectorElement.fromConnection
        toConnection = connectorElement.toConnection
        self.fromConnection = ConnectorComponent.ConnectionPoint(fromConnection)
        self.toConnection = ConnectorComponent.ConnectionPoint(toConnection)

        refs = []
        refs.append( ConnectorComponent.EdgeReference(fromConnection) )
        refs.append( ConnectorComponent.WhereReference(fromConnection) )
        for index in range(len(connectorElement.controlPoints)):
            refs.append( ArrayElementReference(connectorElement.controlPoints,index) )
        refs.append( ConnectorComponent.WhereReference(toConnection) )
        refs.append( ConnectorComponent.EdgeReference(toConnection) )

        horizontalOrienation = isHorizontal(fromConnection.side)
        directionMap = { True:ConnectorComponent.Orientation.HORIZONTAL, False:ConnectorComponent.Orientation.VERTICAL }

        for index in range(len(refs)-2):
            self.segments.append( ConnectorComponent.Segment(refs[index],refs[index+1],refs[index+2],directionMap[horizontalOrienation]) )
            horizontalOrienation = 1 - horizontalOrienation

        prevSegment = None
        for segment in self.segments:
            if prevSegment:
                self.elbows.append( ConnectorComponent.Elbow(prevSegment,segment) )
            prevSegment = segment


    def __initDelMe__(self,connectorElement):
        #print("Creating CACHE")
        self.segments = []
        self.elbows = []
        fromConnection = connectorElement.fromConnection
        toConnection = connectorElement.toConnection
        self.fromConnection = ConnectorComponent.ConnectorCache.ConnectionPoint(fromConnection)
        self.toConnection = ConnectorComponent.ConnectorCache.ConnectionPoint(toConnection)

        startPos = self.fromConnection.connectionPosition
        endPos = self.toConnection.connectionPosition

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
        if fromConnection.side==Direction.RIGHT:
            direction = 0
        elif fromConnection.side==Direction.DOWN:
            direction = 1
        elif fromConnection.side==Direction.LEFT:
            direction = 2
        elif fromConnection.side==Direction.UP:
            direction = 3

        firstElbow = True
        for controlPoint in controlPoints:
            skip = False
            newOrientation = direction
            if horizontalOrienation:
                if controlPoint>x:
                    newOrientation = 0
                elif controlPoint<x:
                    newOrientation = 2
                else:
                    skip = True
                if not skip:
                    self.segments.append( ConnectorComponent.ConnectorCache.Segment(connectorElement,ConnectorComponent.ConnectorCache.Orientation.HORIZONTAL,y,x,controlPoint) )
                nextX=controlPoint
                nextY=y
            else:
                if controlPoint>y:
                    newOrientation = 1
                elif controlPoint<y:
                    newOrientation = 3
                else:
                    skip = True
                if not skip:
                    self.segments.append( ConnectorComponent.ConnectorCache.Segment(connectorElement,ConnectorComponent.ConnectorCache.Orientation.VERTICAL,x,y,controlPoint) )
                nextX=x
                nextY=controlPoint

            #if firstElbow:
            #    firstElbow = False
            #else:
            #    self.elbows.append( ConnectorComponent.ConnectorCache.Elbow(x,y,ConnectorComponent.turnSymbol[direction][newOrientation]) )
            x=nextX
            y=nextY
            direction = newOrientation
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

    #def draw(self,context):
    #    self.getConnectorCache().draw(context)

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

    #def getRect(self):
    #    connectorCache = self.getConnectorCache()
    #    return connectorCache.getRect()


