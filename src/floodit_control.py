# ------------------------------
# Imports
# ------------------------------

from access_game_scores import read_game_scores, write_game_scores
from access_game_settings import read_game_settings, write_game_settings

from floodit_model import Model
from floodit_view import View

# ------------------------------
# Variables
# ------------------------------
MAX_BOARD_SIZE = 20
# ------------------------------
# Classes
# ------------------------------

class Controller:
    def __init__(self):
        self.model = None
        self.size = 16
        self.user = "Anonymous"
        self.colours = []
        self.moves_taken = 0
        self.success = False
        self.view = View(self)
    
    def main(self):
        print("In main of controller")
        self.size, self.user, self.colours = read_game_settings("floodit_settings.csv")

        self.user_names, self.scores = read_game_scores("floodit_scores.csv")

        self.best_player, self.best_score = self.find_best_score(self.user_names, self.scores)

        # create board object
        self.model = Model(self.size, len(self.colours))

        b = self.model.fill_board(self.size, len(self.colours))

        self.view.main(b)

    def on_next_colour(self, code):
        print("Next colour: " + self.colours[code])
        b = self.model.start_flood(code)
        print(b)
        self.moves_taken += 1
        if self.model.all_the_same():
            self.success = True
            self.user_names.append(self.user)
            self.scores.append(self.moves_taken)
            write_game_scores("floodit_scores.csv", self.user_names, self.scores)
            self.best_player, self.best_score = self.find_best_score(self.user_names, self.scores)

        self.view.show_board(b)
        self.view.show_scores()
        
    def on_change_user(self, name):
        print("New user name: " + name)
        self.user = name
        write_game_settings("floodit_settings.csv", self.size, self.user, self.colours)
        self.view.show_user()
        
    def on_change_size(self, size):
        print("New board size: " + str(size))
        self.size = size
        write_game_settings("floodit_settings.csv", self.size, self.user, self.colours)
        self.on_request_replay()
        
    def on_request_replay(self):
        print("Replay requested")
        self.moves_taken = 0
        self.success = False
        self.view.reset_board()
        self.view.show_scores()
        b = self.model.fill_board(self.size, len(self.colours))
        self.view.show_board(b)        
        
    # Check for lowest score
    def find_best_score(self, user_names, scores):
        best_score = 500
        best_player ="Nobody" # default       
        for index in range(len(user_names)):
            if int(scores[index]) < best_score:
                best_player = user_names[index]
                best_score = int(scores[index])
        return best_player, best_score

# ------------------------------
# Functions
# ------------------------------

#def select_new_colour(code):
#    print("New colour code: " + str(code))

# ------------------------------
# App
# ------------------------------

game = Controller()
game.main()
     

