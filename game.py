import tkinter as tk
from board import Board
from player import Robber, Cop

class Game:
    def __init__(self, n, c):
        self.board = Board(n)
        self.robber = Robber(self.board)
        self.cops = [Cop(self.board) for i in range(c)]
        self.board.place_cops(self.cops)
        self.board.place_robber(self.robber)

        self.board.display()

    def run_game(self):
        while not self.is_game_over():
            self.play_turn()
            self.board.display()

        if self.is_robber_caught():
            print('You lose!')
        else:
            print('You win!')

    def play_turn(self):
        self.robber.move()
        robber_position = self.get_robber_position()
        for cop in self.cops:
            if not self.is_robber_caught():
                cop.move(robber_position=robber_position)
        
    def is_game_over(self):
        if self.is_robber_caught() or self.is_robber_escape():
            return True
        else:
            return False

    def is_robber_caught(self):
        # TODO: Implement the game over logic
        robber_position = self.get_robber_position()

        for cop in self.cops:
            if cop.x == robber_position[0] and cop.y == robber_position[1]:
                return True
        return False
    
    def is_robber_escape(self):
        # if the robber gets to (0,0) he wins
        robber_position = self.get_robber_position()
        if robber_position[0] == 0 and robber_position[1] == 0:
            return True
        
    def get_robber_position(self):
        return [self.robber.x, self.robber.y]