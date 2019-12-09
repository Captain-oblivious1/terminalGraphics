from Path import *

class Shape(Path):
    def __init__(self,initialOrientation,filled=True):
         Path.__init__(self,initialOrientation)
         self.filled = filled

    def createElbowList(self):
        if not self.testIfClosed():
            refList = self._elbowRefs.copy()
            self.closePath(refList)
        else:
            refList = self._elbowRefs
        elbowList = self.createElbowListFromProvided(refList)
        if self.initialOrientation==Orientation.HORIZONTAL: 
            xRef = refList[0]
            yRef = refList[-1]
        else:
            xRef = refList[-1]
            yRef = refList[0]
        elbowList.append( Path.Elbow(xRef,yRef) )
        return elbowList

    def createSegmentList(self):
        segmentList = super().createSegmentList()
        segmentList[0].fromElbow = segmentList[-1].toElbow
        return segmentList


    def testIfClosed(self):
        refList = self._elbowRefs
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
                    #print("adding vertical x="+str(snapshot.pos)+" from="+str(snapshot.fro)+" to="+str(snapshot.to))
                    self.verticals.append(snapshot)

        def didCross(self,x,y):
            for segment in self.verticals:
                #print("pos="+str(segment.pos)+" fro="+str(segment.fro)+" to="+str(segment.to)+" x="+str(x)+" y="+str(y))
                if x>segment.pos and (x-1)<segment.pos and y>segment.fro and y<segment.to:
                    #print("returning True at x="+str(x)+" y="+str(y))
                    return True
            #print("returning False at x="+str(x)+" y="+str(y))
            return False

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

    # mask[TL][TR][BL][BR]
    border = \
        [ [ [ [None, "┌" ],     \
              [ "┐", "─" ] ],   \
            [ [ "└", "│" ],     \
              [ "┼", "┘" ] ], ],\
          [ [ [ "┘", "┼" ],     \
              [ "│", "└" ] ],   \
            [ [ "─", "┐" ],     \
              [ "┌", " " ] ] ] ]

    def maskCharFor(topLeft,topRight,bottomLeft,bottomRight):
        return Shape.mask[topLeft][topRight][bottomLeft][bottomRight]

    def borderCharFor(topLeft,topRight,bottomLeft,bottomRight):
        return Shape.border[topLeft][topRight][bottomLeft][bottomRight]

    def getRect(segmentList):
        rect = Rect()
        for seg in segmentList:
            rect.unionWith(seg.getRect())
        return rect

    def drawFilled(self,context,segmentList):
        fillSnapshot = Shape.FillSnapshot(segmentList)

        rect = Shape.getRect(segmentList)
        prevRow = [False] * (rect.width() + 1)
        #for col in range(rect.width()+1):
        #    print( str(col%10), end='')
        #print("")
        for row in range(rect.height()):
            y = rect.y()+row
            testY = y + .5
            #print("row="+str(row)+" y="+str(y)+" testY="+str(testY))
            prevInShape = False
            inShape = False
            for col in range(rect.width()):
                x = rect.x()+col
                testX = x + .5
                crossed = fillSnapshot.didCross(testX,testY)
                if crossed:
                    inShape = not inShape
                maskChar = Shape.maskCharFor(prevRow[col],prevRow[col+1],prevInShape,inShape)
                #if context.readChar(x,y)=="c":
                #    print("About to do C maskChar='"+maskChar+"' col="+str(col))
                #    print("tl="+str(prevRow[col])+" tr="+str(prevRow[col+1])+" bl="+str(prevInShape)+" br="+str(inShape))
                #print("maskChar='"+maskChar+"'")
                context.andChar(x,y,maskChar)
                #if col==3:
                    #return
                borderChar = Shape.borderCharFor(prevRow[col],prevRow[col+1],prevInShape,inShape)
                if borderChar:
                    context.orChar(x,y,borderChar)
                #context.orChar(x,y,"#" if inShape else "@")    
                prevRow[col] = prevInShape
                prevInShape= inShape
            #for col in range(rect.width()+1):
            #    print("T" if prevRow[col] else "F", end='')
            #print("")

    def drawUnfilled(self,context,segmentList):
        oldDirection = segmentList[-1].direction()
        for segment in segmentList:
            direction = segment.direction()
            elbow = segment.fromElbow
            context.orChar(elbow.x(),elbow.y(),self.elbowSymbol[oldDirection.value][direction.value])

            snapshot = segment.getSnapshot()
            if snapshot.fro<=snapshot.to:
                if segment.orientation==Orientation.HORIZONTAL:
                    context.drawHorizontalLine(snapshot.pos,snapshot.fro,snapshot.to)
                else:
                    context.drawVerticalLine(snapshot.pos,snapshot.fro,snapshot.to)
            oldDirection = direction

