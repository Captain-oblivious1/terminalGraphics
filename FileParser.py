import re

from Model import *

class FileParser:
    def __init__(self):
        self.diagramRe = re.compile("\\$diagram",re.IGNORECASE)
        self.nameRe = re.compile("name:",re.IGNORECASE)
        self.hashRe = re.compile("hash:",re.IGNORECASE)
        self.openRe = re.compile("\\s*{")
        self.closeRe = re.compile("}")

    def loadFromFile(self,fileName,diagramName=None):
        try:
            file = open(fileName,'r')
        except FileNotFoundError:
            print("File '"+fileName+"' not found.")
            exit(1)

        print("loading from file="+str(fileName)+" diagram="+str(diagramName))

        while True:
            line = file.readline()
            if not line:
                break

            diagramTag = self.diagramRe.search(line)
            if diagramTag!=None:
                diagramBlock = FileParser._parseDiagramBlock(line,file)

                    

                    

                #line = line[diagramTag.span()[1]:]
                #print("dia start="+str(diagramTag.start))

                #openCurly = re.search('{',line[diagramTag.end:])


                print("found '"+line+"'")

        file.close()
        return Diagram()

        #self.diagramComponent = createDiagramComponent(self,createTestDiagram())

    def saveToFile(self,file,diagram):
        print("saving to file="+str(file)+" diagram="+str(diagram))

    @staticmethod
    def _parseDiagramBlock(line,file):
        diagramText = ""

        while True:
            if line[-1]=='\n':
                diagramText += line[:-1]
            else:
                diagramText += line

            line = file.readline()
            if not line:
                break


    @staticmethod
    def _parseName(line):
        pass
        #line.find("name"

    @staticmethod
    def _parseHash(line):
        pass

class DiagramBlock:
    def __init__(self,name,hash):
        self.name = name
        self.hash = hash
