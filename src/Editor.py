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
        self.keyListeners = set([])
        self.mouseListeners = set([])

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
        self.keyListeners.add(listener)

    def removeKeyListener(self,listener):
        self.keyListeners.remove(listener)

    def addMouseListener(self,listener):
        self.mouseListeners.add(listener)

    def removeMouseListener(self,listener):
        self.mouseListeners.remove(listener)

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
            #if event!=curses.KEY_MOUSE:
            #    print("event="+str(event))
            if event!=curses.KEY_MOUSE:
                print("Got event="+str(event)+" nListeners="+str(len(self.keyListeners)))
                handled = False
                if len(self.keyListeners)>0:
                    for listener in self.keyListeners.copy():
                        print("about to fire event to component")
                        if listener.keyEvent(event):
                            handled = True

                if not handled:
                    if event == 27: # ESC key
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
                    elif event == 330:  # del key
                        diagram.delete()
            else:
                handled = False
                if len(self.mouseListeners)>0:
                    for listener in self.mouseListeners.copy():
                        if listener.mouseEvent(event):
                            handled = True
                        
                if not handled:
                    _ , mx, my, _, bstate = curses.getmouse()
                    #print("Button state="+hex(bstate)+" (b1 click="+hex(curses.BUTTON1_CLICKED)+" b1 press="+hex(curses.BUTTON1_PRESSED)+" b1 release="+hex(curses.BUTTON1_RELEASED)+" b3 press="+hex(curses.BUTTON3_PRESSED)+" b3 release="+hex(curses.BUTTON3_RELEASED)+")")
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

            if not self.context.invalidatedRect.isNullRect():
                diagram.draw(self.context)
                self.context.validateAll()
                self.screen.refresh()

        curses.endwin()
