from Path import *

class ClosedPath(Path):
    _plus  = [ "┼", "╋" ]

    def __init__(self,element):
         super().__init__(element)

    #def __setattr__(self,name,value):
    #    if name=="corners":
    #        self._setCorners(value)
    #    elif name=="elbowRefs":
    #        elbowRefs = self.closePath(value)
    #        super().__setattr__(name,elbowRefs)
    #    else:
    #        super().__setattr__(name,value)

    #def _setCorners(self,value):
    def updateStroke(self):
        super().updateStroke()

        element = self.element
        thickInt = int(element.thickness)
        styleInt = int(element.style)
        if element.corners==Corners.SQUARE:
            cornerArray = Path._squareCorners[thickInt]
        else:
            cornerArray = Path._roundCorners
        tl = cornerArray[0]
        tr = cornerArray[1]
        bl = cornerArray[2]
        br = cornerArray[3]
        h = Path._horizontalLines[thickInt][styleInt]
        v = Path._verticalLines[thickInt][styleInt]
        p = ClosedPath._plus[thickInt]
        s = ' '

        self.border = \
            [ [ [ [None, tl ],    
                  [ tr,  h ] ],  
                [ [ bl,  v ],    
                  [  p, br ] ], ], 
              [ [ [ br,  p ],    
                  [  v, bl ] ],  
                [ [  h, tr ],    
                  [ tl,  s ] ] ] ]

    def createElbowList(self,refList):
        if not self.testIfClosed(refList):
            refList = refList.copy()
            self.closePath(refList)
        else:
            refList = self.elbowRefs
        elbowList = super().createElbowList(refList)
        return elbowList

    def createSegmentList(self,refList):
        segmentList = super().createSegmentList(refList)
        segmentList[0].fromElbow = segmentList[-1].toElbow
        segmentList[0].fromElbow.toSegment = segmentList[0]
        segmentList[-1].toElbow.fromSegment = segmentList[-1]
        return segmentList

    def testIfClosed(self,refList):
        refLen = len(refList)
        if refLen<5:
            return False
        elif refLen%2==0:
            return refList[0]==refList[-2] and refList[1]==refList[-1]
        else:
            return refList[0]==refList[-1] and refList[1]==refList[-2]

    def closePath(self,refList):
        if len(refList)%2==0:
            if refList[-1] == refList[2]:
                refList.append(refList[0])
            else:
                refList.append(refList[0])
                refList.append(refList[1])
        else:
            if refList[-1] == refList[0]:
                refList.append(refList[1])
            else:
                refList.append(refList[1])
                refList.append(refList[0])
        return refList

    def draw(self,context,bold):
        if self.element.fill == Fill.OPAQUE:
            self.drawFilled(context,self.segments,bold)
        else:
            self.drawUnfilled(context,self.segments,bold)

    # mask[TL][TR][BL][BR]
    mask = \
        [ [ [ [ "█", "▛" ],     \
              [ "▜", "▀" ] ],   \
            [ [ "▙", "▌" ],     \
              [ "▚", "▘" ] ], ],\
          [ [ [ "▟", "▞" ],     \
              [ "▐", "▝" ] ],   \
            [ [ "▄", "▖" ],     \
              [ "▗", " " ] ] ] ]

    @staticmethod
    def maskCharFor(topLeft,topRight,bottomLeft,bottomRight):
        return ClosedPath.mask[topLeft][topRight][bottomLeft][bottomRight]

    def borderCharFor(self,topLeft,topRight,bottomLeft,bottomRight):
        return self.border[topLeft][topRight][bottomLeft][bottomRight]

    #def getRect(segmentList):
    #    rect = Rect()
    #    for seg in segmentList:
    #        rect.unionWith(seg.getRect())
    #    return rect

    def drawFilled(self,context,segmentList,bold):
        fillSnapshot = ClosedPath.FillSnapshot(segmentList)

        rect = self.getRect()
        prevRow = [False] * (rect.width() + 1)
        for row in range(rect.height()):
            y = rect.y()+row
            testY = y #+ .5
            prevInShape = False
            inShape = False
            for col in range(rect.width()):
                x = rect.x()+col
                testX = x #+ .5
                crossed = fillSnapshot.didCross(testX,testY)
                if crossed:
                    inShape = not inShape
                maskChar = ClosedPath.maskCharFor(prevRow[col],prevRow[col+1],prevInShape,inShape)
                borderChar = self.borderCharFor(prevRow[col],prevRow[col+1],prevInShape,inShape)
                context.andChar(x,y,maskChar,bold)
                if borderChar:
                    context.orChar(x,y,borderChar,bold)
                prevRow[col] = prevInShape
                prevInShape= inShape

    def drawUnfilled(self,context,segmentList,bold):
        oldDirection = segmentList[-1].direction()
        for segment in segmentList:
            direction = segment.direction()
            elbow = segment.fromElbow
            elbowChar = self.elbowSymbol[oldDirection.value][direction.value]
            context.orChar(elbow.getX(),elbow.getY(),elbowChar,bold)

            snapshot = segment.getSnapshot()
            element = self.element
            if snapshot.fro<=snapshot.to:
                if segment.orientation==Orientation.HORIZONTAL:
                    context.drawHorizontalLine(snapshot.pos,snapshot.fro,snapshot.to,element.thickness,element.style,bold)
                else:
                    context.drawVerticalLine(snapshot.pos,snapshot.fro,snapshot.to,element.thickness,element.style,bold)
            oldDirection = direction

    def move(self,offset,context):
        #print("ClosedPath.move offset x="+str(offset.x)+" y="+str(offset.y))
        element = self.element
        if element.startOrientation == Orientation.HORIZONTAL:
            xElement = 0
        else:
            xElement = 1

        turns = element.turns
        for i in range(len(turns)):
            #if i>=2:
            if i%2 == xElement:
                elementOffset = offset.x
            else:
                elementOffset = offset.y
            turns[i] += elementOffset
                #ref.set( ref.get() + elementOffset )

    # I am not sure I want this behavior
    #def isPointInPath(self,point):
    #    parentResult = super().isPointInPath(point)
    #    if parentResult:
    #        return True
    #    else:
    #        return self.isPointInside(point)

    # This doesn't work anyway...
    #def isPointInside(self,point):
    #    fillSnapshot = ClosedPath.FillSnapshot(self.segments)
    #    return fillSnapshot.didCross(point.x,point.y)

    class FillSnapshot:
        def __init__(self,segmentList):
            self.verticals=[]
            for segment in segmentList:
                if segment.orientation==Orientation.VERTICAL:
                    snapshot = segment.getSnapshot(True)
                    self.verticals.append(snapshot)

        def didCross(self,x,y):
            crossCount = 0
            for segment in self.verticals:  #added = to conditions to avoid floating point math
                if x>=segment.pos and (x-1)<segment.pos and y>=segment.fro and y<segment.to:
                    crossCount += 1
            return crossCount%2
