from Component import *
from Menu import *

class TableComponent(Component):
    def __init__(self,parent,tableElement):
        super().__init__(parent)
        self.tableElement = tableElement
        self.editing = None

    def getRect(self):
        element = self.tableElement
        totalWidth = 1
        for width in element.columnWidths:
            totalWidth += width + 1

        totalHeight = 1
        for height in element.rowHeights:
            totalHeight += height + 1

        rect = Rect(element.location.x,element.location.y,totalWidth,totalHeight)
        return rect

        #mask = \
        #    [ [ [ [ "█", "▛" ],     \
        #          [ "▜", "▀" ] ],   \
        #        [ [ "▙", "▌" ],     \
        #          [ "▚", "▘" ] ], ],\
        #      [ [ [ "▟", "▞" ],     \
        #          [ "▐", "▝" ] ],   \
        #        [ [ "▄", "▖" ],     \
        #          [ "▗", " " ] ] ] ]

    def draw(self,context):
        element = self.tableElement
        selected = self.isSelected()
        rect = self.getRect()
        l = rect.l
        r = rect.r - 1
        t = rect.t
        b = rect.b - 1
        context.andChar(l,t,'▛',selected)
        context.andChar(r,t,'▜',selected)
        context.andChar(l,b,'▙',selected)
        context.andChar(r,b,'▟',selected)
        for i in range(l+1,r):
            context.andChar(i,t,'▀',selected)
            context.andChar(i,b,'▄',selected)
        for i in range(t+1,b):
            context.andChar(l,i,'▌',selected)
            context.andChar(r,i,'▐',selected)
        for i in range(t+1,b):
            for j in range(l+1,r):
                context.andChar(j,i,' ',selected) 
        context.orChar(l,t,'┌',selected)
        context.orChar(r,t,'┐',selected)
        context.orChar(l,b,'└',selected)
        context.orChar(r,b,'┘',selected)
        widths = element.columnWidths
        nWidths = len(widths)
        x = l
        context.drawVerticalLine(x,t+1,b-1,Thickness.THIN,Style.SOLID,selected)
        for i in range(nWidths):
            x += widths[i] + 1
            if i<nWidths-1:
                context.orChar(x,t,'┬',selected)
                context.orChar(x,b,'┴',selected)
            context.drawVerticalLine(x,t+1,b-1,Thickness.THIN,Style.SOLID,selected)
        y = t
        heights = element.rowHeights
        nHeights = len(heights)
        context.drawHorizontalLine(y,l+1,r-1,Thickness.THIN,Style.SOLID,selected)
        for i in range(nHeights):
            y += heights[i] + 1
            if i<nHeights-1:
                context.orChar(l,y,'├',selected)
                context.orChar(r,y,'┤',selected)
            context.drawHorizontalLine(y,l+1,r-1,Thickness.THIN,Style.SOLID,selected)

        y = t + 1
        for i in range(len(element.dataRows)):
            height = heights[i]
            row = element.dataRows[i]
            x = l + 1
            for j in range(len(row)):
                width = widths[j]
                field = row[j]
                justification = field.justification
                text = field.text
                if justification==Justification.LEFT:
                    offset = 0
                elif justification==Justification.RIGHT:
                    offset = width 
                else:
                    offset = int(width/2)
                context.writeJustifiedText(x+offset,y,text,justification)
                x += width + 1
            y += height + 1

        

    def move(self,fromPoint,offset,context):
        self.tableElement.location += offset

    def showContextMenu(self,point,context):
        options = []
        col,row = self._fieldAt(point)
        legitCol = col is not None
        legitRow = row is not None

        if legitCol and legitRow:
            options += ["edit text"]
            just = self.tableElement.dataRows[row][col].justification 
            if just!=Justification.LEFT:
                options += ["left justify"]
            if just!=Justification.CENTER:
                options += ["center justify"]
            if just!=Justification.RIGHT:
                options += ["right justify"]
            options += [""]

        if legitRow:
            options += ["add row above", "add row below", "delete row"]
            options += [""]

        if legitCol:
            options += ["add column left", "add column right", "delete column"]

        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        option = menu.getSelectedOption()
        if option=="left justify":
            just = Justification.LEFT
        elif option=="center justify":
            just = Justification.CENTER
        elif option=="right justify":
            just = Justification.RIGHT
        else:
            just = None

        tableElement = self.tableElement
        col,row = self._fieldAt(menu.getTopLeft())
        #legitCol = col is not None
        #legitRow = row is not None
        if just is not None:
            tableElement.dataRows[row][col].justification = just
            self.invalidate()
        else:
            editor = self.getEditor()
            if option=="edit text":
                #if legitCol and legitRow:
                self.editing = [row,col]
                editor.addKeyListener(self)
                self._changeText('')
            elif option=="add column left":
                self._insertColumn(col)
            elif option=="add column right":
                self._insertColumn(col+1)
            elif option=="delete column":
                del tableElement.columnWidths[col]
                for row in tableElement.dataRows:
                    del row[col]
            elif option=="add row above":
                self._insertRow(row)
            elif option=="add row below":
                self._insertRow(row+1)
            elif option=="delete row":
                del tableElement.rowHeights[row]
                del tableElement.dataRows[row]
            else:
                self._stopEditing()
            self.invalidate()

    def keyEvent(self,event):
        if event>=0 and event<=255:
            if(event==27):
                self._stopEditing()
            else:
                self._changeText( chr(event), True )
        else:
            if event==263: # Backspace
                self._changeText( self._editingField().text[0:-1], False )

    def _insertColumn(self,col):
        tableElement = self.tableElement
        tableElement.columnWidths.insert(col,3)
        newFieldText = "new"
        for row in tableElement.dataRows:
            tableField = TableField()
            tableField.text = newFieldText
            tableField.justification = Justification.LEFT
            row.insert(col,tableField)
            newFieldText = ""

    def _insertRow(self,row):
        tableElement = self.tableElement
        tableElement.rowHeights.insert(row,1)
        newRow = []
        newFieldText = "new"
        for _ in range(len(tableElement.columnWidths)):
            tableField = TableField()
            tableField.text = newFieldText
            tableField.justification = Justification.LEFT
            newRow.append(tableField)
            newFieldText = ""
        tableElement.dataRows.insert(row,newRow)

    def _editingField(self):
        if self.editing==None:
            return None
        else:
            row = self.editing[0]
            col = self.editing[1]
            return self.tableElement.dataRows[row][col]

    def _stopEditing(self):
        self.getEditor().removeKeyListener(self)
        self.editing = None
        self.invalidate()

    def _changeText(self,ch,append=False):
        self.invalidate()
        tableElement = self.tableElement
        row = self.editing[0]
        col = self.editing[1]
        editingField = self._editingField()
        if append:
            editingField.text += ch
        else:
            editingField.text = ch

        widestCell = 0
        for i in range(len(tableElement.rowHeights)):
            longestLine,_ = longestLineAndNumberLines(tableElement.dataRows[i][col].text)
            #print("longestLine for '"+tableElement.dataRows[i]
            if longestLine>widestCell:
                widestCell = longestLine

        tallestCell = 0
        for i in range(len(tableElement.columnWidths)):
            _,nLines = longestLineAndNumberLines(tableElement.dataRows[row][i].text)
            if nLines>tallestCell:
                tallestCell = nLines

        #print("widest="+str(widestCell)+" tallest="+str(tallestCell))
        tableElement.columnWidths[col] = widestCell
        tableElement.rowHeights[row] = tallestCell

        self.invalidate()

    def _fieldAt(self,point):
        rect = self.getRect()
        element = self.tableElement

        x = rect.l
        widths =  element.columnWidths
        nWidths = len(widths)
        col = None
        for i in range(nWidths):
            x += widths[i] + 1
            if point.x<x:
                col = i
                break

        y = rect.t
        heights =  element.rowHeights
        nHeights = len(heights)
        row = None
        for i in range(nHeights):
            y += heights[i] + 1
            if point.y<y:
                row = i
                break

        return col,row
