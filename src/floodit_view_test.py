# ------------------------------
# Imports
# ------------------------------
from floodit_view import View

# ------------------------------
# Test Variables
# ------------------------------
TEST_BOARD_SIZE = 16
import numpy as np
import random
from access_game_settings import read_game_settings, write_game_settings
# ------------------------------
# Test Class
# ------------------------------

class TestController:
    def __init__(self):
        self.size = TEST_BOARD_SIZE
        self.user = "Anonymous"
        self.colours = []
        self.board = np.zeros((TEST_BOARD_SIZE, TEST_BOARD_SIZE), dtype=int)
        self.moves_taken = 0
        self.success = False
        self.view = View(self)
    
    def main(self):
        print("In main of test controller")
        self.size, self.user, self.colours = read_game_settings("floodit_test_settings.csv")

        self.user_names = ["John", "Fred"]
        
        self.scores = [32 ,25]

        self.best_player = "Fred"
        self.best_score = 25
        
        num_codes = len(self.colours)
        for x in range(self.size):
            for y in range(self.size):
                code = random.randint(0,num_codes-1)
                self.board[x, y] = code

        self.view.main(self.board)

    def select_next_colour(self, code):
        print("Next colour: " + self.colours[code])

        self.moves_taken += 1
        if self.moves_taken > 5:
            self.success = True
            self.best_player = self.user
            self.best_score = self.moves_taken

        self.view.show_board(self.board)
        self.view.show_scores()
        
    def change_user(self, name):
        print("New user name: " + name)
        self.user = name
        write_game_settings("floodit_test_settings.csv", self.size, self.user, self.colours)
        self.view.show_user()
        
    def change_size(self, size):
        print("New board size: " + str(size))
        self.size = size
        write_game_settings("floodit_test_settings.csv", self.size, self.user, self.colours)
        self.request_replay()
        
    def request_replay(self):
        print("Replay requested")
        self.moves_taken = 0
        self.success = False
        self.view.reset_board()
        self.view.show_scores()
        
        num_codes = len(self.colours)
        for x in range(self.size):
            for y in range(self.size):
                code = random.randint(0,num_codes-1)
                self.board[x, y] = code
        self.view.show_board(self.board)       
        

        
def test_view():
    tc = TestController()
    tc.main()