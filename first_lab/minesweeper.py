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
