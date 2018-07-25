import curses
import time
mydirs = {260:[0,-1],
 261:[0,1],
 259:[-1,0],
258:[1,0]}
myboxchars ='┌┐└┘│─'
#               0-UL     1-UR     2-LL     3-LR     4-H      5-V

def main(stdscr):
    stdscr.clear()
    #stdscr.addstr(1,1,'Hello World.')
    stdscr.refresh()
    curses.noecho()
    curses.curs_set(False)
    y = 4
    x = 4
    myinput = ''
    drawbox(0,0,10,3,stdscr)
    stdscr.addstr(1,3,"DSAM")
    menu1 = menu(stdscr,3,0,10,[['Option 1',1],['Option 2',2],['Option 3',3],['Option 4',4]])
    stdscr.addstr(3,0,truncatepad(menu1.run(),10))
    textbox1 = textbox(stdscr,4,0,10,'Thisisareallylongstring',True)
    textbox1.refresh()
    stdscr.refresh()
    stdscr.getch()
        
def drawbox(y,x,width,height,stdscr):
   
    i = y+1
    mydispstr = myboxchars[0]+(myboxchars[5]*(width-2))+myboxchars[1]
    stdscr.addstr(y,x,mydispstr)
    while(i<y + height-1):
        stdscr.addstr(i,x,myboxchars[4])
        stdscr.addstr(i,x+width-1,myboxchars[4])
        i = i + 1
    mydispstr = myboxchars[2]+(myboxchars[5]*(width-2))+myboxchars[3]
    stdscr.addstr(y+height-1,x,mydispstr)



    
def clearblock(y,x,width,height,stdscr):
    i = 0
    while(i<height):
        stdscr.addstr(y+i,x,' '*width)
        i = i + 1

class textbox:
    def __init__(self,myscreen,y,x,width,initial='',boxed=False):
        self.myscreen = myscreen
        self.x = x
        self.y = y
        self.pos = 0
        self.value = initial
        self.boxed = boxed
        self.width = width
        self.cursor = 0
    def edit(self):
        y = self.y
        x = self.x
        
        texty = y
        textx = x
        stdscr = self.myscreen
        if(self.boxed):
            texty = texty + 1
            textx = textx + 1
        try:
            cursorchar = self.dispstr[self.cursor]
        except:
            cursorchar = ' '
        
    def refresh(self):
        y = self.y
        x = self.x
        texty = y
        textx = x
        stdscr = self.myscreen
        if(self.boxed):
            texty = texty + 1
            textx = textx + 1
            mydispstr = myboxchars[0]+(myboxchars[5]*(self.width-2))+myboxchars[1]
            stdscr.addstr(y,x,mydispstr)
            stdscr.addstr(y+1,x,myboxchars[4])
            stdscr.addstr(y+1,x+self.width-1,myboxchars[4])
            mydispstr = myboxchars[2]+(myboxchars[5]*(self.width-2))+myboxchars[3]
            stdscr.addstr(y+2,x,mydispstr)
        self.dispstr = self.getdisplaystring()
        stdscr.addstr(texty,textx,self.dispstr)
        
            
    def getdisplaystring(self):
        effectivewidth = self.width
        myval = self.value
        mylen = len(myval)
        if(self.boxed):
            effectivewidth = effectivewidth - 2
        if(mylen<=effectivewidth):
            self.pos = 0
            return self.value
       
        if(self.pos>0):
            return '…'+truncatepad(myval[self.pos:],self.pos+effectivewidth-1)
        return truncatepad(myval[self.pos:],effectivewidth)

        
class menu:
    def __init__(self,myscreen,y,x,width,items):
        self.myscreen = myscreen
        self.x = x
        self.y = y
        self.width = width
        self.items = items
    def run(self):
        x = self.x
        y = self.y
        current = 0
        i = 0
        numitems = len(self.items)
        while(i<numitems):
            self.myscreen.addstr(y+i,x+1,truncatepad(self.items[i][0],self.width-1))
            i = i + 1
        myinput = 0
        while(myinput!=10):
            self.myscreen.addstr(y+current,x,' ')
            try:
                current = current + mydirs[myinput][0]
            except:
                pass
            if(current<0):
                current = numitems-1
            if(current==numitems):
                current = 0
            self.myscreen.addstr(y+current,x,'*')
            #stdscr.addstr(0,0,truncatepad(myinput,20))
            self.myscreen.refresh()
            myinput = self.myscreen.getch()
        clearblock(y,x,self.width,numitems,self.myscreen)
        return self.items[current][1]
                   
def truncatepad(mystring,mylen):
    mystring = str(mystring)
    if(len(mystring)>mylen):
          return mystring[0:mylen-1]+'…'
    return mystring + (' '*(mylen-len(mystring)))


curses.wrapper(main)
