from Path import *

class ClosedPath(Path):
    def __init__(self,initialOrientation=None,elbowRefs=None,filled=False):
         super().__init__(initialOrientation,elbowRefs)
         self.filled = filled

    def __setattr__(self,name,value):
        if name=="corners":
            self._setCorners(value)
        elif name=="elbowRefs":
            elbowRefs = self.closePath(value)
            super().__setattr__(name,elbowRefs)
        else:
            super().__setattr__(name,value)

    def _setCorners(self,value):
        super()._setCorners(value)
        if value==Corners.SQUARE:
            array = Path._squareCorners
        else:
            array = Path._roundCorners
        tl = array[0]
        tr = array[1]
        bl = array[2]
        br = array[3]
        self.border = \
            [ [ [ [None, tl  ],    \
                  [  tr, "─" ] ],  \
                [ [  bl, "│" ],    \
                  [ "┼", br] ], ], \
              [ [ [  br, "┼" ],    \
                  [ "│", bl  ] ],  \
                [ [ "─", tr  ],    \
                  [  tl, " " ] ] ] ]

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

    def drawSegmentList(self,context,segmentList):
        if self.filled:
            self.drawFilled(context,segmentList)
        else:
            self.drawUnfilled(context,segmentList)

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

    def maskCharFor(topLeft,topRight,bottomLeft,bottomRight):
        return ClosedPath.mask[topLeft][topRight][bottomLeft][bottomRight]

    def borderCharFor(self,topLeft,topRight,bottomLeft,bottomRight):
        return self.border[topLeft][topRight][bottomLeft][bottomRight]

    def getRect(segmentList):
        rect = Rect()
        for seg in segmentList:
            rect.unionWith(seg.getRect())
        return rect

    def drawFilled(self,context,segmentList):
        fillSnapshot = ClosedPath.FillSnapshot(segmentList)

        rect = ClosedPath.getRect(segmentList)
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
                context.andChar(x,y,maskChar)
                if borderChar:
                    context.orChar(x,y,borderChar)
                prevRow[col] = prevInShape
                prevInShape= inShape

    def drawUnfilled(self,context,segmentList):
        oldDirection = segmentList[-1].direction()
        for segment in segmentList:
            direction = segment.direction()
            elbow = segment.fromElbow
            elbowChar = self.elbowSymbol[oldDirection.value][direction.value]
            context.orChar(elbow.getX(),elbow.getY(),elbowChar)

            snapshot = segment.getSnapshot()
            if snapshot.fro<=snapshot.to:
                if segment.orientation==Orientation.HORIZONTAL:
                    context.drawHorizontalLine(snapshot.pos,snapshot.fro,snapshot.to)
                else:
                    context.drawVerticalLine(snapshot.pos,snapshot.fro,snapshot.to)
            oldDirection = direction

    def move(self,offset,context):
        #print("ClosedPath.move offset x="+str(offset.x)+" y="+str(offset.y))
        if self.initialOrientation == Orientation.HORIZONTAL:
            xElement = 0
        else:
            xElement = 1

        arrayElement = 0
        for ref in self.elbowRefs:
            if arrayElement>=2:
                if arrayElement%2 == xElement:
                    elementOffset = offset.x
                else:
                    elementOffset = offset.y
                ref.set( ref.get() + elementOffset )
            arrayElement += 1
