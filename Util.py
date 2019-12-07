from Model import *

class AttrReference:
    def __init__(self,obj,attr):
        self.obj = obj
        self.attr = attr

    def get(self):
        return getattr(self.obj,self.attr)

    def set(self,val):
        setattr(self.obj,self.attr,val)


class ArrayElementReference:
    def __init__(self,array,element):
        self.array = array
        self.element = element

    def get(self):
        return self.array[self.element]

    def set(self,val):
        self.array[self.element] = val

class ArrayReference:
    def __init__(self,array):
        self.array = array

    def clear(self):
        self.hj

_vToDArray = [ [ None          , Direction.UP  , None            ], \
               [ Direction.LEFT, Direction.NONE, Direction.RIGHT ], \
               [ None          , Direction.DOWN, None            ] ]

def vectorToDirection(vector):
    normed = vector.normalize().round()
    offset = normed + Point(1,1)
    return  _vToDArray[offset.y][offset.x]



#class Blah:
#    def __init__(self):
#        self.one = 1
#        self.two = 2
#
#b = Blah()
#attrRef = AttrReference(b,"one")
#
#print( "one="+str(attrRef.get()))
#attrRef.set(4)
#print( "one="+str(b.one))
#
#array = [1,2,3,4]
#arrayRef = ArrayElementReference(array,2)
#print( "array="+str(arrayRef.get() ))
#arrayRef.set(97)
#print( "array="+str(array))
