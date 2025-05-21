import tkinter as tk
from mazeCheckClass import Maze

def takeInput():
    input = textEnter.get("1.0",tk.END)
    mazeChecker = Maze()
    mazeChecker.parseMaze(input,True)
    textDisplay.delete("1.0",tk.END)
    textDisplay.insert(tk.END,mazeChecker.solveMaze())

root = tk.Tk()
root.title("Maze Solver")
root.minsize(200,200)
root.geometry("300x250+50+50")

for i in range(2):
    root.grid_columnconfigure(i, weight=1)

title = tk.Label(root,text="Maze Solver")
title.grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="ns"
)

textEnter = tk.Text(root,height=10,width=20)
textEnter.grid(
    row=2,
    column=0,
    sticky="ns"
)

textDisplay = tk.Text(root,height=10,width=20)
textDisplay.grid(
    row=2,
    column=1,
    sticky="ns"
)

solve = tk.Button(root,text="Solve Maze!",width=10,height=3,command=lambda:takeInput())
solve.grid(
    row=3,
    column = 0,
    columnspan=2,
    sticky="ns"
)

root.mainloop()
