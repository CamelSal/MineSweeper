from  tkinter import *
import numpy as np
import time
import gc

r = "#D10A0A"
Red = "#D93D21"


def mine(N): #creates an array representation of a mine swepeter board of NXN size
    n0 = np.full((round(0.85*N**2)),0)
    m1 = np.full(round((0.15*N**2)),1)
    B = np.concatenate((n0,m1)).reshape((N**2))
    np.random.shuffle(B)
    Boa = B.reshape((N,N))
    Board = np.full((N,N),0)
    for i in range(0,N):
        for j in range(0,N):
            if Boa[i, j] == 1:
                Board[i, j] = -1
            else:
                num = nmine(Boa,i,j,N)
                Board[i,j] = num
    return Board

def nmine(B, i, j,N): #counts the number of mines around a specific spot for a given array
    num = 0
    ti = [i + 1, i + 1, i + 1, i, i - 1, i - 1, i - 1, i]
    tj = [j, j + 1, j - 1, j + 1, j, j + 1, j - 1, j - 1]
    for k, m in zip(ti, tj):
        if k < 0 or m < 0 or k == N or m == N:
            continue
        else:
            num += B[k,m]
    return num


class SeaofBTCapp(Tk): #makes the opening screen to allow you to select difficulty
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Starpage, MineSweeperE, MineSweeperM, MineSweeperH):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Starpage)

    def show_frame(self, cont):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[cont]
        frame.tkraise()
        frame.grid()

class MineSweeperE(Frame):
    def __init__(self, parent, controller):
        global F_T, minelox, mineloy,background, turn, flags, N
        self.controller = controller
        Frame.__init__(self, parent)
        self.grid()
        MineBoard(self,8)
        bt_reset = Button(self, text="Reset", command=lambda: reset(self, 8), bg="green")
        bt_reset.grid(row=0, column=6, columnspan=2)


class MineSweeperM(Frame):
    def __init__(self, parent, controller):
        global F_T, minelox, mineloy,background, turn, flags, N
        self.controller = controller
        Frame.__init__(self, parent)
        self.grid()
        ns = 15
        MineBoard(self,ns)
        bt_reset = Button(self, text="Reset", command= lambda: reset(self,ns), bg="green")
        bt_reset.grid(row=0, column= ns-2, columnspan=2)


class MineSweeperH(Frame):
    def __init__(self, parent, controller):
        global F_T, minelox, mineloy,background, turn, flags, N
        self.controller = controller
        Frame.__init__(self, parent)
        self.grid()
        MineBoard(self,20)
        bt_reset = Button(self, text="Reset", command= lambda: reset(self,20,size = 33,fnt = 20), bg="green")
        bt_reset.grid(row=0, column= 18, columnspan=2)

        #rest = reset(self,20,size = 33,fnt = 20)
        #List = Menu(self)
        #List.add_command(label="Reset",command = lambda: reset(self,20,size = 33,fnt = 20))
        #Frame.config(self,menu=List)



def reset(self,N,size = 33,fnt = 20): # reset the whole board destroying all obj to not overload memory
    global F_T, minelox, mineloy, background, turn, flags
    for obj in self.winfo_children():
            obj.destroy()
    MineBoard(self, N, size, fnt)
    bt_reset = Button(self, text="Reset", command=lambda: reset(self, N, size=size, fnt=fnt), bg="green")
    bt_reset.grid(row=0, column=N-2, columnspan=2)

def MineBoard(self,N,size = 33,fnt = 20): #sets up the full gui to allow for playing
    global F_T, minelox, mineloy, background, turn, flags
    background = np.array([[],[]])
    minelox, mineloy = [], []
    turn = 0
    mines = round(0.15 * N ** 2)
    flags = mines


    def Rclick(event, i, j, f): # will determine the type of event that will occur after  the click on the specific spot
        global F_T, turn
        if turn == 0: # if first turn will create the whole board
            F_T = np.full((N,N),0)
            turn = + 1
            first_turn(i, j, f)
        elif F_T[i, j] > 0: # do nothing space either has a flag or has been revealed
            pass
        else: #revealed the spot and determine next move
            turn = + 1
            turn_event(i, j, f)

    def turn_event(i, j, f):
        global F_T, flags
        F_T[i, j] = 1
        B = background[i, j]
        if B == -1: #the spot is mine initiate game over
            for k, g in zip(minelox, mineloy):
                gameover(k, g)
            #F_T = np.full((N, N), 1)
            gm = Label(self, text="Game Over", bg="Black", font=("Verdana", 40), fg="red")
            gm.grid(row=int(N / 2 - 1), column=0, columnspan=N, rowspan=3)
        elif B == 0: # revealed all surround frames
            f.config(bg="White", highlightthickness=0.5)
            expand(i, j)
            fx, fy = np.where(F_T == 2)
            flags = mines - len(fx)
            fl.config(text="flags: " + str(flags))
        else: # revealed only the specific frame
            reveal(B, i, j)

    def reveal(B, i, j, c= "white"): # change the frame on the spot i,j to reveale B
        frame = (Frame(self, width=size, height=size, bg=c,
                       highlightbackground="Black", highlightthickness=0.5, bd=0))
        frame.grid(row=i + 1, column=j)
        if B == "X" or B == "F":
            txt = Label(self, text=B, font=("Verdana", fnt), bg = c)
            txt.grid(row=i + 1, column=j)
        elif B != 0:
            txt = Label(self, text=B, font=("Verdana", fnt), bg = c,fg = color(B))
            txt.grid(row=i + 1, column=j)

    def gameover(i, j): # will end the game showing a game over
        stsf = F_T[i, j]
        if stsf == 2:
            reveal("F",i, j, c="#5f7552")
        else:
            reveal("X",i, j,c =Red)

    def first_turn(i, j, f): #creates the board of a new game assuring the spot that was click had zeroe mines around it
        global F_T, minelox, mineloy, background, turn
        background = mine(N)
        minelox, mineloy = np.where(background == -1)
        B = background[i, j]
        while B != 0:
            background = mine(N)
            minelox, mineloy = np.where(background == -1)
            B = background[i, j]
        turn_event(i, j, f)
        #print(minelox, "\n",mineloy)

    def expand(i, j): #reveales all blocks around the location
        ti = [i + 1, i + 1, i + 1, i, i - 1, i - 1, i - 1, i]
        tj = [j, j + 1, j - 1, j + 1, j, j + 1, j - 1, j - 1]
        for k, m in zip(ti, tj):
            if k < 0 or m < 0 or k == N or m == N:
                continue
            elif F_T[k, m] == 1:
                continue
            else:
                try:
                    drawb(k, m)
                    self.update_idletasks()
                except:
                    continue

    def drawb(i, j): #determine if there are no mines around to continue expand revealed
        B = background[i, j]
        F_T[i, j] = 1
        if B == 0:
            expand(i, j)
            reveal("", i, j, c="white")
        else:
            reveal(B, i, j, c="white")

    def win(): # checks if win condition has been met if so end game if not keep trying and no more flags allowed
        global F_T
        flagx, flagy = np.where(F_T == 2)
        if np.all(flagx == minelox) and np.all(flagy == mineloy):
            for x,y in zip(flagx, flagy):
                Label(self, text="F", font=("Verdana", fnt),
                      fg="#00660e", bg="#636963").grid(row= x + 1, column=y)
                Frame(self, width=size, height=size, bg="#636963").grid(row= x + 1, column=y)
            hx, hy = np.where(F_T == 0)
            B = background
            for k, g in zip(hx, hy):
                reveal(B[k, g], k, g)
            F_T = np.full((N, N), 1)
            gm = Label(self, text="Win", bg="Blue", font=("Verdana", 40), fg="Green")
            gm.grid(row=int(N / 2 - 1), column=0, columnspan=N, rowspan=3)
        else:
            fl.config(text="Keep Trying")

    def flag_event(event, i, j): #determine if a flag can be place and check if it is that last check win conditions
        global flags
        if F_T[i, j] == 2: # removed place flag
            frame_mk(i, j)
            F_T[i, j] = 0
            flags = flags + 1
            fl.config(text="flags: " + str(flags))
        elif F_T[i, j] == 1: #no flag allowed spot revealed
            pass
        elif flags == 0: #no flags left and win condition not met
            pass
        elif flags == 1:# last flag check if condition are met
            flag_pl(i, j)
            win()
        else: # place flag
            flag_pl(i, j)

    def frame_mk(i,j): # sets up the frame for the block setting up two mouse events when clicked
        self.update_idletasks()
        frame = (Frame(self, width=size, height=size, bg="grey",
                       highlightbackground="Black", highlightthickness=1, bd=0))
        frame.bind("<Button-1>", lambda x, i=i, j=j, frame=frame: Rclick(x, i, j, frame))
        frame.grid(row=i + 1, column=j)
        frame.bind("<Button-2>", lambda x, i=i, j=j: flag_event(x, i, j))

    def flag_pl(i,j): # places flag on the block
        global flags
        flags = flags - 1
        fl.config(text="flags: " + str(flags))
        txt = Label(self, text="F", font=("Verdana", fnt), fg="#0087ff", bg="grey")
        txt.grid(row=i + 1, column=j)
        txt.bind("<Button-2>", lambda x, i=i, j=j: flag_event(x, i, j))
        F_T[i, j] = 2





    def inistt(): # inisiates the board 
        global F_T, minelox, mineloy, background, turn, flags
        for i in range(0, N):
            for j in range(0, N):
                frame_mk(i, j)
        F_T = np.full((N, N), 0)
        flags = mines
        fl.config(text="flags: " + str(flags))
        turn = 0

    def color(i): # determines the color of the font
        c = ["white","Blue","#196c28","red","#6f20e8","#754138","#40e0d0","#080808","#707577"]
        return c[i]


    # laids out the area above the screen
    f = Frame(self, width=size * N, height=size, bg="green")
    f.grid(row=0, column=0, columnspan=N)
    txt = Label(self, text="Mineswepper", bg="green", font=("Verdana", 20))
    txt.grid(row=0, column=0, columnspan=N)
    fl = Label(self, text="flags: " + str(flags), bg="green")
    fl.grid(row=0, column=0, columnspan=2)
    inistt()


size = 40

class Starpage(Frame):
    def __init__(self,parent,controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self,text = "Mine Sweeper",font=("Verdana",22))
        label.grid(row=2,column = 1,columnspan = 6)
        Label(self,text = "",font=("Verdana",22)).grid(row=7,column = 0,columnspan = 6)
        Label(self,text = "",font=("Verdana",22)).grid(row=1,column = 0,columnspan = 6)
        Label(self, text="", font=("Verdana", 22)).grid(row=3, column=0, columnspan=6)
        Label(self, text="", font=("Verdana", 22)).grid(row=3, column=0)
        Label(self, text="", font=("Verdana", 22)).grid(row=3, column=8)
        bt_E = Button(self, text="Easy", command=lambda: controller.show_frame(MineSweeperE), bg="green")
        bt_E.grid(row=4, column=1, columnspan=6)
        bt_M = Button(self, text="Medium", command=lambda: controller.show_frame(MineSweeperM), bg="green")
        bt_M.grid(row=5, column=1, columnspan=6)
        bt_H = Button(self, text="Hard", command=lambda: controller.show_frame(MineSweeperH), bg="green")
        bt_H.grid(row=6, column=1, columnspan=6)



SeaofBTCapp().mainloop()
