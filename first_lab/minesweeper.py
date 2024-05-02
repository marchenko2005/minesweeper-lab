from tkinter import *
from tkinter import simpledialog, messagebox
import random
from datetime import datetime, timedelta
from collections import deque

class Minesweeper:
    def __init__(self, tk):
        self.tk = tk
        self.tk.title("Minesweeper")
        self.start_game()
    def start_game(self):
        self.size_x = simpledialog.askinteger("Input", "Enter number of rows for the minesweeper grid:", minvalue=3, maxvalue=15)
        self.size_y = self.size_x  
        num_mines = simpledialog.askinteger("Input", f"Enter number of mines (less than {self.size_x * self.size_y}):",
                                        minvalue=1, maxvalue=(self.size_x * self.size_y - 1))

        self.frame = Frame(self.tk)
        self.frame.pack()

        self.labels = {
            "time": Label(self.frame, text="00:00:00"),
            "mines": Label(self.frame, text="Mines: 0"),
            "flags": Label(self.frame, text="Flags: 0")
        }
        self.labels["time"].grid(row=0, column=0, columnspan=self.size_y)
        self.labels["mines"].grid(row=self.size_x+1, column=0, columnspan=int(self.size_y/2))
        self.labels["flags"].grid(row=self.size_x+1, column=int(self.size_y/2)-1, columnspan=int(self.size_y/2))

        self.setup(num_mines)
        self.updateTimer()

    def setup(self, num_mines):
        self.flagCount = 0
        self.clickedCount = 0
        self.startTime = None
        self.tiles = {}
        self.mines = num_mines 
        all_positions = [(x, y) for x in range(self.size_x) for y in range(self.size_y)]
        mines_positions = set(random.sample(all_positions, self.mines))

        for x in range(self.size_x):
            for y in range(self.size_y):
                isMine = (x, y) in mines_positions
                id = f"{x}_{y}"
                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": 0,
                    "coords": {"x": x, "y": y},
                    "button": Button(self.frame, text=" ", width=4, height=2),
                    "mines": 0
                }
                tile["button"].grid(row=x+1, column=y)
                tile["button"].bind("<Button-1>", self.onClickWrapper(x, y))
                tile["button"].bind("<Button-3>", self.onRightClickWrapper(x, y))
                if x not in self.tiles:
                    self.tiles[x] = {}
                self.tiles[x][y] = tile

        for x in range(self.size_x):
            for y in range(self.size_y):
                tile = self.tiles[x][y]
                mine_count = sum((1 for n in self.getNeighbors(x, y) if n["isMine"]))
                tile["mines"] = mine_count

        self.refreshLabels()

    def refreshLabels(self):
        self.labels["flags"].config(text=f"Flags: {self.flagCount}")
        self.labels["mines"].config(text=f"Mines: {self.mines}")

    def onClickWrapper(self, x, y):
        return lambda Button: self.onClick(self.tiles[x][y])

    def onRightClickWrapper(self, x, y):
        return lambda Button: self.onRightClick(self.tiles[x][y])