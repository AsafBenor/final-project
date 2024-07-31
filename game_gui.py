import tkinter as tk
from game import Game

class GameGUI:
    def __init__(self, n, c):
        self.root = tk.Tk()
        self.game = Game(n, c)

    def run(self):
        self.root.mainloop()

    