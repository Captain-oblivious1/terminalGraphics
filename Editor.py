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
    pathElement1.pathType = PathType.CLOSED #OPEN
    pathElement1.startOrientation = Orientation.VERTICAL
    pathElement1.turns = [5,23,12,30,20,2]
    pathElement1.corners = Corners.ROUND
    diagramElement.elements.append(pathElement1)

    pathElement2 = PathElement()
    pathElement2.pathType = PathType.CLOSED #OPEN
    pathElement2.fill = Fill.FILLED
    pathElement2.startOrientation = Orientation.HORIZONTAL
    pathElement2.turns = [40,20,50,30]
    pathElement2.corners = Corners.SQUARE
    diagramElement.elements.append(pathElement2)

    return diagramElement

def createDiagramComponent(diagramElement):
    diagramComponent = DiagramComponent(diagramElement)

    for element in diagramElement.elements:
        if type(element) is TextBoxElement:
            component = TextBoxComponent(diagramComponent)
        elif type(element) is ConnectorElement:
            component = ConnectorComponent(diagramComponent)
        elif type(element) is PathElement:
            if element.pathType == PathType.CLOSED:
                fill = element.fill == Fill.FILLED
                renderer = ClosedPath(element.startOrientation,fill)
            else:
                renderer = OpenPath(element.startOrientation)
            renderer.corners = Corners.SQUARE
            component = PathComponent(diagramComponent,element,renderer)

        diagramComponent.components.append(component)

    return diagramComponent


class Editor:
    #def __init__(self):
        #self.state = State()

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

    def run(self):
        screen = curses.initscr()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        screen.clear()
        #screen.addstr(0,0,"Hello",curses.color_pair(1)|curses.A_BOLD)

        diagram = createTestDiagram()
        print("============")
        diagramComponent = self.diagramComponent = createDiagramComponent(diagram)

        context = self.context = Context(screen)
        self.goIdleState()

        diagramComponent.invalidateAll()
        diagramComponent.draw(context)
        screen.refresh()
        diagramComponent.validateAll()

        curses.mouseinterval(0)

        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        while(True):
            event = screen.getch()
            #print("event='"+str(curses.keyname(event))+"'")
            #ch = 'N'
            if event == 27:
                screen.nodelay(True)
                nextKey = screen.getch()
                screen.nodelay(False)
                if nextKey==-1:
                    break;
            #elif event == ord('q'):
            #    break
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

            diagramComponent.draw(context)
            diagramComponent.validateAll()
            screen.refresh()

        curses.endwin()
