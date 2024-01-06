import math
from Point import *

class Rect:
    def __init__(self,x=math.inf,y=math.inf,width=-math.inf,height=-math.inf):
        self.l,self.r = Rect._initDim(x,width)
        self.t,self.b = Rect._initDim(y,height)

    def _initDim(pos,length):
        if length==-math.inf:
            return pos,-math.inf  #cannot do ∞-∞.  So returning max of -∞
        elif length<0:
            return pos+length, pos  #always want min to be less than max (i.e. no negative width allowed)
        else:
            return pos, pos+length

    def makeRectFromPoints(topLeft,bottomRight):
        return Rect(
                topLeft.x,
                topLeft.y,
                bottomRight.x-topLeft.x+1,
                bottomRight.y-topLeft.y+1)

    def includePoint(self,point):
        rect = Rect(point.x,point.y,1,1)
        self.unionWith(rect)
        return self

    def unionWith(self,rect):
        self.l = min(self.l,rect.l)
        self.t = min(self.t,rect.t)
        self.r = max(self.r,rect.r)
        self.b = max(self.b,rect.b)
        return self

    def doesIntersect(self,rect):
        return self.l <= rect.r and self.r > rect.l and self.t <= rect.b and self.b > rect.t

    def isNullRect(self):
        return self.l==math.inf or self.t==math.inf or self.r==-math.inf or self.b==-math.inf

    def isInsideRect(self,amIInside,inclusive=False):
        if inclusive:
            r = self.r+1
            b = self.b+1
        else: 
            r = self.r
            b = self.b
        return self.l<=amIInside.l and r>amIInside.r and self.t<=amIInside.t and b>amIInside.b

    def isInsidePoint(self,amIInside):
        return self.l<=amIInside.x and self.r>amIInside.x and self.t<=amIInside.y and self.b>amIInside.y

    def x(self):
        return self.l

    def y(self):
        return self.t

    def width(self):
        return self.r-self.l

    def height(self):
        return self.b-self.t

    def topLeft(self):
        return Point(self.l,self.t)

    def bottomRight(self):
        return Point(self.r,self.b)

    #def area(self):
    #    return self.width()*self.height()

    def __eq__(self,other):
        return other is not None and \
               self.l==other.l and \
               self.r==other.r and \
               self.t==other.t and \
               self.b==other.b

    def __str__(self):
        return "Rect:{x="+str(self.l)+",y="+str(self.t)+",width="+str(self.width())+",height="+str(self.height())+"}"

def testRect():
    print("inf="+str(math.inf-math.inf))
    print(Rect(5,10,45,30).unionWith(Rect(20,20,50,25)))
    print(Rect(25,30,10,10).unionWith(Rect(20,20,50,25)))
    print(Rect().unionWith(Rect(20,20,50,25)))



