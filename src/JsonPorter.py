import json

from Model import *
from Point import *

class JsonPorter:
    @staticmethod
    def importDiagram(fileName,diagramName):
        fileData = JsonPorter._loadJsonFile(fileName)
        diagramData = fileData.get(diagramName)
        if diagramData is None:
            raise Exception("Could not find diagram '"+diagramName+"' in file '"+fileName+"'.")

        return JsonPorter._convertToDiagram(diagramData)

    @staticmethod
    def exportDiagram(fileName,diagram):
        newDiagramData = JsonPorter._convertToDictionary(diagram)
        diagramName = newDiagramData["name"]
        
        try:
            fileData = JsonPorter._loadJsonFile(fileName)
        except FileNotFoundError:
            fileData = {}

        fileData[diagramName] = newDiagramData

        JsonPorter._dumpJsonFile(fileName,fileData)


    primitives = (bool, str, int, float, type(None))

    @staticmethod
    def _convertToDictionary(thing):
        if isinstance(thing,Element):
            jsonData = {}
            jsonData['_type'] = type(thing).__name__
            for attr in dir(thing):
                if not attr.startswith('_'):
                    attrValue = getattr(thing,attr)
                    attrData = JsonPorter._convertToDictionary(attrValue)
                    jsonData[attr] = attrData
            return jsonData
        elif isinstance(thing,list):
            attrData = []
            for it in thing:
                attrData.append(JsonPorter._convertToDictionary(it))
            return attrData
        elif isinstance(thing,JsonPorter.primitives):
            return thing
        elif isinstance(thing,Enum):
            return thing.name
        elif isinstance(thing,Point):
            return [thing.x,thing.y]
        else:
            return str(thing)

    @staticmethod
    def _convertToDiagram(jsonData):
        if jsonData["_type"]!="Diagram":
            raise Exception("Inpropertly constucted data file.  Expect Diagram componenent to have _type of 'Diagram'")

        diagram = Diagram(jsonData["name"])
        for elementData in jsonData["elements"]:
            diagram.elements.append(JsonPorter._convertToElement(elementData))

        return diagram
            
    nameToTypes = { 
        "corners": lambda t : Corners[t],
        "endArrow": lambda t : Arrow[t],
        "fill": lambda t : Fill[t],
        "pathType": lambda t : PathType[t],
        "startArrow": lambda t : Arrow[t],
        "startOrientation": lambda t : Orientation[t],
        "turns": lambda t: JsonPorter._strListToIntList(t),
        "justification": lambda t : Justification[t],
        "location": lambda t : JsonPorter._arrayToPoint(t),
        "text": lambda t : t }

    @staticmethod
    def _convertToElement(jsonData):
        dataType = jsonData["_type"]
        if dataType=="PathElement":
            element = PathElement()
        elif dataType=="TextElement":
            element = TextElement()
        else:
            raise Exception("Unrecognized element type '"+dataType+"'")

        for key,value in jsonData.items():
            if key!="_type":
                setattr(element,key, JsonPorter.nameToTypes[key](value))

        return element

    @staticmethod
    def _strListToIntList(stringList):
        return list(map(int,stringList))

    @staticmethod
    def _arrayToPoint(array):
        return Point(array[0],array[1])

    @staticmethod
    def _loadJsonFile(fileName):
        with open(fileName,'r') as f:
            return json.load(f)

    @staticmethod
    def _dumpJsonFile(fileName,data):
        with open(fileName,'w') as f:
            return json.dump(data,f,indent=1)
