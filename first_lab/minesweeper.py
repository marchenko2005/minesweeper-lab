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
