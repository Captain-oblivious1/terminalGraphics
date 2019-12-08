from Path import *

class Shape(Path):
    def __init__(self,initialOrientation):
         Path.__init__(self,initialOrientation)

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


    #def drawSegmentList(self,context,segmentList):
    #    inShape = False
    #    rect = self.getRect()
    #    for row in range(rect.height):
    #        for col in range(rect.width):
    #            x = rect.x()+col
    #            y = rect.y()+row



    def drawSegmentList(self,context,segmentList):
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

