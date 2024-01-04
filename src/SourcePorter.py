import re
import shutil

from Model import *
from DiagramComponent import *
from MemoryContext import *

class SourcePorter:
    def __init__(self,format='\\${diagram:(.*)}'):
        self.formatRe = re.compile(format,re.IGNORECASE)
        self.openRe = re.compile('⦃\\s*(.*)')
        self.closeRe = re.compile('⦄')

    def writeToFile(self,fileName,diagram,diagramName=None):
        if diagramName==None:
            diagramName = diagram.name

        try:
            file = open(fileName,'r')
        except FileNotFoundError:
            print("File '"+fileName+"' not found.")
            exit(1)

        tempFileName = fileName+".tmp"
        tempFile = open(tempFileName,'w') 

        while True:
            line = file.readline()
            if not line:
                break

            formatTag = self.formatRe.search(line)
            openTag = self.openRe.search(line)

            if formatTag!=None:
                currentDiagName = formatTag.group(1)
                if currentDiagName!=diagramName:
                    tempFile.write(line)
                else:
                    prefix = line[0:formatTag.span()[0]]

                    tempFile.write(prefix)
                    tempFile.write("⦃ ")
                    tempFile.write(currentDiagName)
                    tempFile.write('\n')
                    SourcePorter._writeDiagramToFile(diagram,tempFile,prefix)
                    tempFile.write(prefix)
                    tempFile.write("⦄\n")

            elif openTag!=None:
                currentDiagName = openTag.group(1)
                if currentDiagName!=diagramName:
                    tempFile.write(line)
                else:
                    prefix = line[0:openTag.span()[0]]
                    tempFile.write(line)
                    SourcePorter._writeDiagramToFile(diagram,tempFile,prefix)
                    tempFile.write(prefix)
                    tempFile.write("⦄\n")

                    # skip past old diagram in file
                    while True:
                        line = file.readline()
                        if self.closeRe.search(line) is not None:
                            break

            else:
                tempFile.write(line)


                #line = line[diagramTag.span()[1]:]
                #print("dia start="+str(diagramTag.start))

                #openCurly = re.search('{',line[diagramTag.end:])



        file.close()
        tempFile.close()
        shutil.move(tempFileName,fileName)

    @staticmethod
    def _writeDiagramToFile(diagram,file,prefix):
        diagramComponent = DiagramComponent(None,diagram)
        memContext = MemoryContext(80,50)
        memContext.invalidateRect()
        diagramComponent.draw(memContext)
        memContext.writeToStream(file,prefix)
