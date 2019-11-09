from  tkinter import *
import numpy as np

class Run_Game(Tk):
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

class MineSweeperE(Frame):
    def __init__(self, parent, controller):
        global F_T, minelox, mineloy,background, turn, flags, N
        self.controller = controller
        Frame.__init__(self, parent)
        self.grid()
        MineBoard(self,10)
        bt_reset = Button(self, text="Reset", command=lambda: reset(self, 10), bg="green")
        bt_reset.grid(row=0, column=8, columnspan=2)

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

class Board:
    def __init__(self, N):
        self.minelox, mineloy = [], []
        self.loc = np.array([[], []])
        self.F_T = np.full((N, N), 0)
        self.turn = 0
        self.mines = round(0.15 * N ** 2)
        self.flags = self.mines


    def mine(self,N):  # creates an array representation of a mine swepeter board of NXN size
        n0 = np.full((round( N ** 2- self.mines)), 0)
        m1 = np.full(self.mines, 1)
        B = np.concatenate((n0, m1)).reshape((N ** 2))
        np.random.shuffle(B)
        Boa = B.reshape((N, N))
        Board = np.full((N, N), 0)
        def nmine(B, i, j, N):  # counts the number of mines around a specific spot for a given array
            num = 0
            ti = [i + 1, i + 1, i + 1, i, i - 1, i - 1, i - 1, i]
            tj = [j, j + 1, j - 1, j + 1, j, j + 1, j - 1, j - 1]
            for k, m in zip(ti, tj):
                if k < 0 or m < 0 or k == N or m == N:
                    continue
                else:
                    num += B[k, m]
            return num
        for i in range(0, N):
            for j in range(0, N):
                if Boa[i, j] == 1:
                    Board[i, j] = -1
                else:
                    num = nmine(Boa, i, j, N)
                    Board[i, j] = num
        self.loc = Board

def MineBoard(self,N,size = 33,fnt = 20): #sets up the full gui to allow for playing
    global flags
    BR = Board(N)

    def Rclick(event, i, j): # will determine actins after a right click on the block
        if BR.turn == 0:
            BR.turn = + 1
            first_turn(i, j)
        elif BR.F_T[i, j] > 0:
            pass
        else:
            BR.turn = + 1
            turn_event(i, j)

    def first_turn(i, j): #creates the board of a new game assuring the spot that was click had zeroe mines around it
        BR.mine(N)
        BR.minelox, BR.mineloy = np.where(BR.loc == -1)
        B = BR.loc[i, j]
        while B != 0:
            BR.mine(N)
            BR.minelox, BR.mineloy = np.where(BR.loc == -1)
            B = BR.loc[i, j]
        turn_event(i, j)
        #print(minelox, "\n",mineloy)

    def turn_event(i, j): # will adjust the block depending on what is underline value
        BR.F_T[i, j] = 1
        B = BR.loc[i, j]
        if B == -1: #mine click game over
            for k, g in zip(BR.minelox, BR.mineloy):
                gameover(k, g)
            BR.F_T = np.full((N, N), 1)
            gm = Label(self, text="Game Over", bg="Black", font=("Verdana", 40), fg="red")
            gm.grid(row=int(N / 2 - 1), column=0, columnspan=N, rowspan=3)
        elif B == 0: # reveal the block and all adjacets blocks
            Frames[i,j].config(bg="White", highlightthickness=0.5)
            Texts[i, j].config(bg="White")
            expand(i, j)
            fx, fy = np.where(BR.F_T == 2)
            BR.flags = BR.mines - len(fx)
            fl.config(text="flags: " + str(BR.flags))
        else: # reveals the one block
            reveal(B, i, j)

    def reveal(B, i, j, c= "white"): # reveal the underline value of the block
        Frames[i,j].config(bg=c, highlightthickness=0.5)
        if B == "X" or B == "F":
            Texts[i,j].config(text=B, bg = c,fg = "black")
        elif B != 0:
            Texts[i, j].config(text=B, bg=c,fg = color(B))
        else:
            Texts[i, j].config(bg=c)

    def gameover(i, j): # will end the game showing a game over
        if BR.F_T[i, j] == 2:
            reveal("F",i, j, c="#5f7552")
        else:
            reveal("X",i, j,c ="#D93D21")


    def expand(i, j): #reveales all blocks around the location
        ti = [i + 1, i + 1, i + 1, i, i - 1, i - 1, i - 1, i]
        tj = [j, j + 1, j - 1, j + 1, j, j + 1, j - 1, j - 1]
        for k, m in zip(ti, tj):
            if k < 0 or m < 0 or k == N or m == N: #out of board value
                continue
            elif BR.F_T[k, m] == 1: #alredy revealed block
                continue
            elif BR.loc[k, m] == 0: #continues expansion
                BR.F_T[k, m] = 1
                reveal(0, k, m)
                expand(k, m)
            else: #stops expansion
                BR.F_T[k, m] = 1
                reveal(BR.loc[k, m], k, m)


    def win(): # checks if win condition has been met if so end game if not keep trying
        flagx, flagy = np.where(BR.F_T == 2)
        if np.all(flagx == BR.minelox) and np.all(flagy == BR.mineloy):
            for x,y in zip(flagx, flagy):
                Frame(self, width=size, height=size, bg="#636963",highlightbackground="Black",
                      highlightthickness=1, bd=0).grid(row=x + 1, column=y)
                Label(self, text="F", font=("Verdana", fnt),
                      fg="#00660e", bg="#636963").grid(row= x + 1, column=y)
            hx, hy = np.where(BR.F_T == 0)
            B = BR.loc
            for k, g in zip(hx, hy):
                reveal(B[k, g], k, g)
            BR.F_T = np.full((N, N), 1)
            gm = Label(self, text="Win", bg="Blue", font=("Verdana", 40), fg="Green")
            gm.grid(row=int(N / 2 - 1), column=0, columnspan=N, rowspan=3)
        else:
            fl.config(text="Keep Trying")

    def flag_event(event, i, j):
        if BR.F_T[i, j] == 2:
            Texts[i, j].config(text="")
            BR.F_T[i, j] = 0
            BR.flags = BR.flags + 1
            fl.config(text="flags: " + str(BR.flags))
        elif BR.F_T[i, j] == 1:
            pass
        elif BR.flags == 0:
            pass
        elif BR.flags == 1:
            flag_pl(i, j)
            win()
        else:
            flag_pl(i, j)


    def flag_pl(i,j): # places flag on the block
        BR.flags = BR.flags - 1
        fl.config(text="flags: " + str(BR.flags))
        Texts[i,j].config(text="F", fg="#0087ff")
        Texts[i,j].bind("<Button-2>", lambda x, i=i, j=j: flag_event(x, i, j))
        BR.F_T[i, j] = 2


    def color(i): #determines color of the number revealed
        c = ["white","Blue","#196c28","red","#6f20e8","#754138","#40e0d0","#080808","#707577"]
        return c[i]

    f = Frame(self, width=size * N, height=size, bg="green")
    f.grid(row=0, column=0, columnspan=N)
    txt = Label(self, text="Mineswepper", bg="green", font=("Verdana", 20))
    txt.grid(row=0, column=0, columnspan=N)
    fl = Label(self, text="flags: " + str(BR.flags), bg="green")
    fl.grid(row=0, column=0, columnspan=2)
    Frames = np.zeros((N, N)).astype(object)
    Texts = np.zeros((N, N)).astype(object)
    for i in range(0, N):
        for j in range(0, N):
            frame = Frame(self, width=size, height=size, bg="grey",
                          highlightbackground="Black", highlightthickness=1, bd=0)
            frame.bind("<Button-1>", lambda x, i=i, j=j: Rclick(x, i, j))
            frame.grid(row=i + 1, column=j)
            frame.bind("<Button-2>", lambda x, i=i, j=j: flag_event(x, i, j))
            txt = Label(self, text="", font=("Verdana", fnt), bg="grey")
            txt.bind("<Button-1>", lambda x, i=i, j=j: Rclick(x, i, j))
            txt.grid(row=i + 1, column=j)
            txt.bind("<Button-2>", lambda x, i=i, j=j: flag_event(x, i, j))
            Frames[i, j] = frame
            Texts[i,j] = txt

def reset(self,N,size = 33,fnt = 20):
    for obj in self.winfo_children():
            obj.destroy()
    MineBoard(self, N, size, fnt)
    bt_reset = Button(self, text="Reset", command=lambda: reset(self, N, size=size, fnt=fnt), bg="green")
    bt_reset.grid(row=0, column=N-2, columnspan=2)


Run_Game().mainloop()
