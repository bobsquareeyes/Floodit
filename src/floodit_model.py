# ------------------------------
# Imports
# ------------------------------
import random
import numpy as np

# ------------------------------
# Variables
# ------------------------------


# ------------------------------
# Classes
# ------------------------------

class Model:
    def __init__(self, board_size, num_codes):
        self.board_size = board_size
        self.num_codes = num_codes
        self.board = np.zeros((board_size, board_size), dtype=int)


    def fill_board(self, size, num_codes):
        if size > self.board_size:
            print("WARNING: board size > " + str(self.board_size))
            size = self.board_size
        for x in range(size):
            for y in range(size):
                code = random.randint(0,num_codes-1)
                self.board[x, y] = code
        return self.board
    
    
    def start_flood(self, flood_code):
        print("Flood code = " + str(flood_code))
        if flood_code >= 0 and flood_code < self.num_codes:
            target = self.board[0,0]
            self.flood(0, 0, target, flood_code)
        else:
            print("WARNING: flood_code out of range: " + str(flood_code))
        return self.board[0:self.board_size, 0:self.board_size]
        #win_check()
        

    # Recursively floods adjacent squares (by calling itself)
    def flood(self, x, y, target, replacement):
        # Algorithm from https://en.wikipedia.org/wiki/Flood_fill
        if target == replacement:
            return
        if self.board[x, y] != target:
            return
        self.board[x, y] = replacement
        if y+1 <= self.board_size-1:   # South
            self.flood(x, y+1, target, replacement)
        if y-1 >= 0:                   # North
            self.flood(x, y-1, target, replacement)
        if x+1 <= self.board_size-1:   # East
            self.flood(x+1, y, target, replacement)
        if x-1 >= 0:                   # West
            self.flood(x-1, y, target, replacement)
           

    # Check whether all squares are the same
    def all_the_same(self):
        top_left = self.board[0][0]
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x ,y] != top_left:
                    return False
        return True
    
#    def test_model(self):
#        model = Model(12, 8)
#        return self
