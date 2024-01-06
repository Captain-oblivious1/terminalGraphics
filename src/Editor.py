import curses

from DiagramComponent import *
from CursesContext import *

class Editor:
    def __init__(self,diagram,saveCallback):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.screen.clear()
        self.diagramComponent = DiagramComponent(self,diagram)
        self.context = CursesContext(self.screen)
        self.saveCallback = saveCallback
        self.listeners = set([])

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

    def addKeyListener(self,listener):
        self.listeners.add(listener)

    def removeKeyListener(self,listener):
        self.listeners.remove(listener)

    def run(self):
        #screen.addstr(0,0,"Hello",curses.color_pair(1)|curses.A_BOLD)
            

        self.goIdleState()

        diagram = self.diagramComponent

        diagram.invalidateAll()
        diagram.draw(self.context)
        self.screen.refresh()
        self.context.validateAll()

        curses.mouseinterval(0)

        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        oldX=-1
        oldY=-1
        while(True):
            event = self.screen.getch()
            #print("event='"+str(curses.keyname(event))+"'")
            #print("event='"+str(bin(event))+"'")
            #ch = 'N'
            if len(self.listeners)>0 and event>=0 and event<=255:
                for listener in self.listeners:
                    listener.keyEvent(chr(event))
            elif event == 27:
                self.screen.nodelay(True)
                nextKey = self.screen.getch()
                self.screen.nodelay(False)
                if nextKey==-1:
                    break;
            elif event == ord('s'):
                self.saveCallback()
            elif event == ord('q'):
                break
            elif event == curses.KEY_PPAGE:
                diagram.moveSelectedForward()
            elif event == curses.KEY_NPAGE:
                diagram.moveSelectedBackward()
            elif event == curses.KEY_HOME:
                diagram.moveSelectedToFront()
            elif event == curses.KEY_END:
                diagram.moveSelectedToBack()
            elif event == curses.KEY_MOUSE:
                _ , mx, my, _, bstate = curses.getmouse()
                if bstate & curses.BUTTON1_CLICKED != 0:
                    self.state.mouseClicked(mx,my)
                elif bstate & curses.BUTTON1_PRESSED != 0:
                    self.state.mousePressed(mx,my)
                elif bstate & curses.BUTTON1_RELEASED != 0:
                    self.state.mouseReleased(mx,my)
                elif bstate & curses.BUTTON3_RELEASED != 0:
                    self.state.rightReleased(mx,my)
                else:
                    #if mx!=oldX or my!=oldY: #This added the weird G characters when hilighting
                    self.state.mouseMoved(mx,my)
                    #    oldX = mx
                    #    oldY = my
            else:
                self.state.keyPressed(event)
                #print("key pressed="+str(event))

            diagram.draw(self.context)
            self.context.validateAll()
            self.screen.refresh()

        curses.endwin()