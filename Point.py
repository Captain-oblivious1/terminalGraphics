import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self,right):
        return Point(self.x+right.x,self.y+right.y)

    def __iadd__(self,right):
        self.x += right.x
        self.y += right.y
        return self

    def __sub__(self,right):
        return Point(self.x-right.x,self.y-right.y)

    def length(self):
        return math.sqrt(self.x*self.x+self.y*self.y)

    def normalize(self):
        length = self.length()
        if length==0:
            return Point(0,0)
        else:
            return Point(self.x/length,self.y/length)

    def round(self):
        return Point(round(self.x),round(self.y))

    def __eq__(self,right):
        return right!=None and self.x==right.x and self.y==right.y

    def __ne__(self,right):
        return not self.__eq__(right)

    def __str__(self):
        return "Point("+str(self.x)+","+str(self.y)+")"

    def isEqual(self,x,y):
        return self.x==x and self.y==y

