import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root=root
        self.root.title("Tic Tac Toe Deluxe")
        self.root.geometry("800x700")
        self.mode="2p"
        self.current="X"
        self.board=[""]*9

        self.canvas=tk.Canvas(root,bg="black",highlightthickness=0)
        self.canvas.pack(fill="both",expand=True)
        self.circles=[]
        colors=["#ff4d4d","#ffaa00","#ffee00","#33dd66","#33bbff","#9966ff","#ff66cc"]
        for _ in range(30):
            x=random.randint(0,800); y=random.randint(0,700); r=random.randint(20,60)
            oid=self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=random.choice(colors),outline="")
            self.circles.append([oid,random.choice([-2,-1,1,2]),random.choice([-2,-1,1,2])])
        self.animate()
        self.menu()

    def animate(self):
        for c in self.circles:
            oid,dx,dy=c
            self.canvas.move(oid,dx,dy)
            x1,y1,x2,y2=self.canvas.coords(oid)
            if x1<0 or x2>800:c[1]*=-1
            if y1<0 or y2>700:c[2]*=-1
        self.root.after(30,self.animate)

    def clear(self):
        self.canvas.delete("ui")

    def menu(self):
        self.clear()
        self.canvas.create_text(400,120,text="TIC TAC TOE",fill="white",font=("Arial",34,"bold"),tags="ui")
        b1=tk.Button(self.root,text="2 Players",font=("Arial",18),bg="#2ecc71",fg="white",command=lambda:self.start("2p"))
        b2=tk.Button(self.root,text="Play with AI",font=("Arial",18),bg="#3498db",fg="white",command=lambda:self.start("ai"))
        self.canvas.create_window(400,280,window=b1,tags="ui")
        self.canvas.create_window(400,360,window=b2,tags="ui")

    def start(self,mode):
        self.mode=mode
        self.board=[""]*9
        self.current="X"
        self.clear()
        self.buttons=[]
        self.turn=self.canvas.create_text(400,40,text="Turn: X",fill="yellow",font=("Arial",20,"bold"),tags="ui")
        frame=tk.Frame(self.root,bg="#222")
        self.canvas.create_window(400,330,window=frame,tags="ui")
        for i in range(9):
            btn=tk.Button(frame,text="",width=4,height=2,font=("Arial",28,"bold"),
                          command=lambda i=i:self.move(i))
            btn.grid(row=i//3,column=i%3,padx=5,pady=5)
            self.buttons.append(btn)
        tk.Button(self.root,text="Restart",command=lambda:self.start(self.mode)).place(x=250,y=650)
        tk.Button(self.root,text="Menu",command=self.menu).place(x=450,y=650)

    def move(self,i):
        if self.board[i]!="": return
        self.place(i,self.current)
        if self.endcheck(): return
        self.current="O" if self.current=="X" else "X"
        self.canvas.itemconfig(self.turn,text=f"Turn: {self.current}")
        if self.mode=="ai" and self.current=="O":
            self.root.after(400,self.ai)

    def place(self,i,p):
        self.board[i]=p
        self.buttons[i]["text"]=p
        self.buttons[i]["fg"]="red" if p=="X" else "blue"

    def ai(self):
        empty=[i for i,v in enumerate(self.board) if v==""]
        if not empty:return
        self.place(random.choice(empty),"O")
        if self.endcheck(): return
        self.current="X"
        self.canvas.itemconfig(self.turn,text="Turn: X")

    def endcheck(self):
        wins=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.board[a]!="" and self.board[a]==self.board[b]==self.board[c]:
                messagebox.showinfo("Winner",f"{self.board[a]} Wins!")
                self.start(self.mode)
                return True
        if "" not in self.board:
            messagebox.showinfo("Draw","It's a Draw!")
            self.start(self.mode)
            return True
        return False

root=tk.Tk()
TicTacToe(root)
root.mainloop()
