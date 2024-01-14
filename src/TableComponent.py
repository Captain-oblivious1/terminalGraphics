from Component import *

class TableComponent(Component):
    def __init__(self,parent,tableElement):
        super().__init__(parent)
        self.tableElement = tableElement

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
            if i<nWidths-1:
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
        options = ["stop editing","","split","join"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        print("Chose menu option '"+menu.getSelectedOption()+"'")
