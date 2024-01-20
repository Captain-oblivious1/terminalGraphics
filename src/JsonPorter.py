import json

from Model import *
from Point import *
from Rect import *

class JsonPorter:
    @staticmethod
    def importDiagram(fileName,diagramName):
        fileData = JsonPorter._loadJsonFile(fileName)
        diagramData = fileData.get(diagramName)
        if diagramData is None:
            return Diagram(diagramName)
        else:
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
        if isinstance(thing,list):
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
            jsonData = {}
            jsonData['_type'] = type(thing).__name__
            for attr in dir(thing):
                if not attr.startswith('_'):
                    attrValue = getattr(thing,attr)
                    attrData = JsonPorter._convertToDictionary(attrValue)
                    if attr=="fro":
                        attr="from"
                    jsonData[attr] = attrData
            return jsonData

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
        "style": lambda t : t,
        "text": lambda t : t,
        "thickness": lambda t : t,
        "columnWidths": lambda t: JsonPorter._strListToIntList(t),
        "rowHeights": lambda t: JsonPorter._strListToIntList(t),
        "dataRows": lambda t: JsonPorter._listToTableData(t),
        "top": lambda t: int(t),
        "actors": lambda t: JsonPorter._strListToActorData(t),
        "lines": lambda t: JsonPorter._strListToLineData(t),
        }

    @staticmethod
    def _convertToElement(jsonData):
        dataType = jsonData["_type"]
        if dataType=="PathElement":
            element = PathElement()
        elif dataType=="TextElement":
            element = TextElement()
        elif dataType=="TableElement":
            element = TableElement()
        elif dataType=="SequenceElement":
            element = SequenceElement()
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
    def _arrayToRect(array):
        return Rect(array[0],array[1],array[2],array[3])

    @staticmethod
    def _listToTableData(array):
        rowList = []
        for row in array:
            colList = []
            for field in row:
                tableField = TableField()
                text = field["text"]
                if text is not None:
                    tableField.text = text
                justification = field.get("justification")
                tableField.justification = Justification[justification] if justification is not None else Justification.LEFT
                colList.append(tableField)
            rowList.append(colList)
        return rowList

    @staticmethod
    def _strListToActorData(array):
        actorList = []
        for jsonStruct in array:
            actor = Actor()
            actor.x = int(jsonStruct["x"])
            actor.label = jsonStruct["label"]
            actorList.append(actor)
        return actorList

    @staticmethod
    def _strListToLineData(array):
        lineList = []
        for jsonStruct in array:
            line = Line()
            line.y = int(jsonStruct["y"])
            line.dashed = bool(jsonStruct["dashed"])
            line.fro = int(jsonStruct["from"])
            line.to = int(jsonStruct["to"])
            lineList.append(line)
        return lineList

    @staticmethod
    def _loadJsonFile(fileName):
        with open(fileName,'r') as f:
            return json.load(f)

    @staticmethod
    def _dumpJsonFile(fileName,data):
        with open(fileName,'w') as f:
            return json.dump(data,f,indent=1)
