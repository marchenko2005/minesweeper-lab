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
    
    def onClick(self, tile):
        if self.startTime is None:
            self.startTime = datetime.now()
        if tile["state"] in (1, 2):
            return
        if tile["isMine"]:
            self.gameOver(False)
        elif tile["mines"] == 0:
            tile["button"].config(text=" ", bg="#b5ebcd")
            self.clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(text=str(tile["mines"]))
        tile["state"] = 1
        self.clickedCount += 1
        if self.clickedCount == (self.size_x * self.size_y - self.mines):
            self.gameOver(True)

    def onRightClick(self, tile):
        if tile["state"] == 0:
            tile["button"].config(text="|>", bg="#edb766")
            tile["state"] = 2
            self.flagCount += 1
        elif tile["state"] == 2:
            tile["button"].config(text=" ", bg="#d9d9d9")
            tile["state"] = 0
            self.flagCount -= 1
        self.refreshLabels()
        if self.checkWinCondition():
            self.gameOver(True)
    
    def checkWinCondition(self):
        if self.flagCount != self.mines:
            return False
        for x in range(self.size_x):
            for y in range(self.size_y):
                tile = self.tiles[x][y]
                if tile["isMine"] and tile["state"] != 2:
                    return False
                if not tile["isMine"] and tile["state"] == 2:
                    return False
        return True

    def clearSurroundingTiles(self, id):
        queue = deque([id])
        seen = set(queue)
        while queue:
            current_id = queue.popleft()
            x, y = map(int, current_id.split("_"))
            current_tile = self.tiles[x][y]
            if current_tile["state"] == 0:
                current_tile["button"].config(text=" ", bg="#b5ebcd")
                current_tile["state"] = 1
                self.clickedCount += 1
                if current_tile["mines"] == 0:
                    for neighbor in self.getNeighbors(x, y):
                        neighbor_id = neighbor["id"]
                        if neighbor_id not in seen:
                            queue.append(neighbor_id)
                            seen.add(neighbor_id)
                else:
                    current_tile["button"].config(text=str(current_tile["mines"]))

    def getNeighbors(self, x, y):
        start_x = max(0, x-1)
        end_x = min(self.size_x, x+2)
        start_y = max(0, y-1)
        end_y = min(self.size_y, y+2)

        neighbors = []
        for nx in range(start_x, end_x):
            for ny in range(start_y, end_y):
                if (nx, ny) != (x, y):
                    neighbors.append(self.tiles[nx][ny])

        return neighbors
    def updateTimer(self):
        if self.startTime is not None:
            now = datetime.now()
            elapsed = now - self.startTime
            self.labels["time"].config(text=str(elapsed).split(".")[0])
        self.tk.after(1000, self.updateTimer)

    def gameOver(self, won):
        self.startTime = None  # Stop the timer
        for x in range(self.size_x):
            for y in range(self.size_y):
                tile = self.tiles[x][y]
                if tile["isMine"]:
                    tile["button"].config(text="*" if tile["state"] != 2 else "|>")
                elif tile["state"] == 2:
                    tile["button"].config(text="|>", bg="red")
                else:
                    tile["button"].config(text=str(tile["mines"]) if tile["mines"] > 0 else " ")
        self.tk.update()

        msg = "You Win! Play again?" if won else "You Lose! Play again?"
        play_again = messagebox.askyesno("Game Over", msg)

        if play_again:
            self.frame.destroy()
            self.start_game()
        else:
            if messagebox.askyesno("Quit", "Do you want to exit the game?"):
                self.tk.quit()
            else:
                self.frame.destroy()
                self.start_game()


def main():
    root = Tk()
    app = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()
