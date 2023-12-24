import curses

from DiagramComponent import *
from Menu import *
from Model import *
from Component import *
from ConnectorComponent import *
from PathComponent import *
from OpenPath import *
from ClosedPath import *
from Context import *

def createTestDiagram():
    diagramElement = Diagram()
    #textBoxElement1 = testTextBox()
    ##textBoxElement1.x = 0
    ##textBoxElement1.y = 20
    #textBoxElement1.x = 20
    #textBoxElement1.y = 10
    #diagramElement.elements.append(textBoxElement1)

    #textBoxElement2 = testTextBox()
    #textBoxElement2.x = 60
    #textBoxElement2.y = 20
    #diagramElement.elements.append(textBoxElement2)


    #fromConnectionPoint1 = ConnectionPoint()
    #fromConnectionPoint1.element = textBoxElement1
    #fromConnectionPoint1.side = Direction.RIGHT
    #fromConnectionPoint1.where = 0.5
    #fromConnectionPoint1.end = Arrow.NONE

    #toConnectionPoint1 = ConnectionPoint()
    #toConnectionPoint1.element = textBoxElement2
    #toConnectionPoint1.side = Direction.LEFT
    #toConnectionPoint1.where = 0.25
    #toConnectionPoint1.end = Arrow.TRIANGLE

    #connectorElement1 = ConnectorElement()
    #connectorElement1.fromConnection = fromConnectionPoint1
    #connectorElement1.toConnection = toConnectionPoint1
    #connectorElement1.controlPoints.append(45)
    #diagramElement.elements.append(connectorElement1)

    #fromConnectionPoint2 = ConnectionPoint()
    #fromConnectionPoint2.element = textBoxElement1
    #fromConnectionPoint2.side = Direction.DOWN
    #fromConnectionPoint2.where = 1.0
    #fromConnectionPoint2.end = Arrow.LINES

    #toConnectionPoint2 = ConnectionPoint()
    #toConnectionPoint2.element = textBoxElement2
    #toConnectionPoint2.side = Direction.UP
    #toConnectionPoint2.where = 0.5
    #toConnectionPoint2.end = Arrow.NONE

    #connectorElement2 = ConnectorElement()
    #connectorElement2.fromConnection = fromConnectionPoint2
    #connectorElement2.toConnection = toConnectionPoint2
    #connectorElement2.controlPoints.append(19)
    #connectorElement2.controlPoints.append(51)
    #connectorElement2.controlPoints.append(15)
    #diagramElement.elements.append(connectorElement2)

    pathElement1 = PathElement()
    pathElement1.pathType = PathType.CLOSED
    #pathElement1.pathType = PathType.OPEN
    pathElement1.fill = Fill.OPAQUE
    pathElement1.startOrientation = Orientation.VERTICAL
    #pathElement1.turns = [5,23,12,30,20,2]
    pathElement1.turns = [0,0,10,20]
    #pathElement1.corners = Corners.ROUND
    pathElement1.corners = Corners.SQUARE
    #pathElement1.startArrow = Arrow.NONE
    #pathElement1.endArrow = Arrow.TRIANGLE
    diagramElement.elements.append(pathElement1)

    pathElement2 = PathElement()
    pathElement2.pathType = PathType.OPEN
    #pathElement2.fill = Fill.OPAQUE
    pathElement2.startOrientation = Orientation.VERTICAL #HORIZONTAL
    pathElement2.turns = [15,40,20,50,30,60]
    pathElement2.corners = Corners.SQUARE
    pathElement2.startArrow = Arrow.LINES
    pathElement2.endArrow = Arrow.TRIANGLE
    diagramElement.elements.append(pathElement2)

    pathElement3 = PathElement()
    pathElement3.pathType = PathType.CLOSED
    pathElement3.fill = Fill.OPAQUE
    pathElement3.startOrientation = Orientation.VERTICAL
    pathElement3.turns = [5,5,15,25,30,30]
    pathElement3.corners = Corners.ROUND
    diagramElement.elements.append(pathElement3)


    #pathElement3 = PathElement()
    #pathElement3.pathType = PathType.CLOSED
    #pathElement3.fill = Fill.OPAQUE
    #pathElement3.startOrientation = Orientation.HORIZONTAL
    #pathElement3.turns = [7,28,12]
    #pathElement3.corners = Corners.ROUND
    #diagramElement.elements.append(pathElement3)

    #fromConnection = ConnectionPoint()
    #fromConnection.element = pathElement1
    #fromConnection.segmentIndex = 2
    #fromConnection.where = .5
    #fromConnection.end = Arrow.TRIANGLE

    #toConnection = ConnectionPoint()
    #toConnection.element = pathElement1
    #toConnection.segmentIndex = 1
    #toConnection.where = .3
    #toConnection.end = Arrow.NONE

    #connection = ConnectorElement()
    #connection.fromConnection = fromConnection
    #connection.toConnection = toConnection
    #connection.turns = [40,50]

    #diagramElement.elements.append(connection)

    return diagramElement

def createDiagramComponent(editor,diagramElement):
    diagramComponent = DiagramComponent(editor,diagramElement)

    for element in diagramElement.elements:
        if type(element) is TextBoxElement:
            component = TextBoxComponent(diagramComponent)
        elif type(element) is ConnectorElement:
            component = ConnectorComponent(diagramComponent)
        elif type(element) is PathElement:
            refArray = []
            for val in element.turns:
               refArray.append( VarReference(val) )
            if element.pathType == PathType.CLOSED:
                fill = element.fill == Fill.OPAQUE
                renderer = ClosedPath(element.startOrientation,refArray,fill)
            else:
                renderer = OpenPath(element.startOrientation,refArray)
                renderer.startArrow = element.startArrow
                renderer.endArrow = element.endArrow
            renderer.corners = element.corners
            component = PathComponent(diagramComponent,element,renderer)

        diagramComponent.components.append(component)

    return diagramComponent


class Editor:
    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.screen.clear()
        diagram = createTestDiagram()
        self.diagramComponent = self.diagramComponent = createDiagramComponent(self,diagram)
        self.context = Context(self.screen)

    def getContext(self):
        return self.context

    def setState(self,state):
        self.state = state

    def goIdleState(self):
        import IdleState
        self.state = IdleState.IdleState(self,self.context,self.diagramComponent)

    def goLassoState(self,startDragPoint):
        import LassoState
        self.state = LassoState.LassoState(self,self.context,self.diagramComponent,startDragPoint)

    def goMovingState(self,startDragPoint):
        import MovingState
        self.state = MovingState.MovingState(self,self.context,self.diagramComponent,startDragPoint)

    def goSelectComponentState(self,eventListener):
        import SelectComponentState
        self.state = SelectComponentState.SelectComponentState(self.diagramComponent,eventListener)

    def run(self):
        #screen.addstr(0,0,"Hello",curses.color_pair(1)|curses.A_BOLD)

        self.goIdleState()

        self.diagramComponent.invalidateAll()
        self.diagramComponent.draw(self.context)
        self.screen.refresh()
        self.context.validateAll()

        curses.mouseinterval(0)

        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        while(True):
            event = self.screen.getch()
            #print("event='"+str(curses.keyname(event))+"'")
            #ch = 'N'
            if event == 27:
                self.screen.nodelay(True)
                nextKey = self.screen.getch()
                self.screen.nodelay(False)
                if nextKey==-1:
                    break;
            elif event == ord('q'):
                break
            elif event == curses.KEY_MOUSE:
                #ch = 'Y'
                _ , mx, my, _, bstate = curses.getmouse()
                #print("bstate="+str(bstate))
                if bstate & curses.BUTTON1_CLICKED != 0:
                    self.state.mouseClicked(mx,my)
                elif bstate & curses.BUTTON1_PRESSED != 0:
                    self.state.mousePressed(mx,my)
                elif bstate & curses.BUTTON1_RELEASED != 0:
                    self.state.mouseReleased(mx,my)
                elif bstate & curses.BUTTON3_RELEASED != 0:
                    self.state.rightReleased(mx,my)
                else:
                    self.state.mouseMoved(mx,my)
            else:
                self.state.keyPressed(event)
                #print("key pressed="+str(event))

            self.diagramComponent.draw(self.context)
            self.context.validateAll()
            self.screen.refresh()

        curses.endwin()
