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
MAX_BOARD_SIZE = 18
# ------------------------------
# Classes
# ------------------------------

class Controller:
    def __init__(self):
        self.model = None
        self.size = 16
        self.user = "Anonymous"
        self.colours = []
        self.success = False
        self.moves_taken = 0
        self.view = View(self)
    
    def main(self):
        print("In main of controller")
        self.size, self.user, self.colours = read_game_settings("floodit_settings.txt")
        if self.size > MAX_BOARD_SIZE:
            self.size = MAX_BOARD_SIZE
        self.user_names, self.scores = read_game_scores("floodit_scores.txt")
        self.best_player, self.best_score = find_best_score(self.user_names, self.scores)
        # create board object
        self.model = Model(self.size, len(self.colours))
        b = self.model.fill_board()
        self.view.main(b)

    def on_next_colour(self, code):
        print("Next colour = " + self.colours[code])
        b = self.model.start_flood(code)
        print(b)
        self.moves_taken += 1
        if self.model.all_the_same():
            self.success = True
            self.user_names.append(self.user)
            self.scores.append(self.moves_taken)
            write_game_scores("floodit_scores.txt", self.user_names, self.scores)
            self.best_player, self.best_score = find_best_score(self.user_names, self.scores)
        self.view.show_board(b)
        self.view.show_scores()
        
    def on_change_user(self, name):
        print("New user name: " + name)
        self.user = name
        write_game_settings("floodit_settings.txt", self.size, self.user, self.colours)
        self.view.show_user()
        
    def on_change_size(self, size):
        print("New board size: " + str(size))
        self.size = size
        write_game_settings("floodit_settings.txt", self.size, self.user, self.colours)
        self.on_request_replay()
        
    def on_request_replay(self):
        print("Replay requested")
        self.success = False
        self.moves_taken = 0
        self.view.reset_board()
        self.view.show_scores()
        b = self.model.fill_board()
        self.view.show_board(b)        
        
    def on_request_save(self):
        print("Save requested")
        self.save_control_state("floodit_control_state.txt")
        self.model.save_model_state("floodit_model_state.txt")
        
    def on_request_restore(self):
        print("Restore requested")
        self.restore_control_state("floodit_control_state.txt")
        b = self.model.restore_model_state("floodit_model_state.txt")
        self.view.show_board(b)
        self.view.reset_board()
        self.view.show_scores()

    def save_control_state(self, filename):
        try: # open file for writing          
            with open(filename, 'w+') as writer:
                writer.writelines("moves_taken\n")
                writer.writelines(str(self.moves_taken) + "\n")
                writer.close()
                print("Saved controller state in: " + filename)             
        except:
            print("WARNING: file: \'" + filename + "\' write error")
                        
    def restore_control_state(self, filename):
        try: # open file for reading
            with open(filename, 'r') as reader:
                print("Restoring controller state from file: " + filename)
                lines = reader.readlines()
                print("No of lines = " + str(len(lines)))
                i = 0
                while i < len(lines):
                    print("Line 1 = " +lines[i])
                    print("Line 2 = " +lines[i+1])
                    if "moves_taken" in lines[i]:
                        self.moves_taken = int(lines[i+1])
                        print("moves_taken = " + str(self.moves_taken))
                    i += 1
                reader.close()
        except:
            print("WARNING: error reading file: \'" + filename + "\' ")
        
# ------------------------------
# Helper Functions
# ------------------------------

# Check for lowest score 
def find_best_score(user_names, scores):
    best_score = 500
    best_player ="Nobody" # default       
    for index in range(len(user_names)):
        if int(scores[index]) < best_score:
            best_player = user_names[index]
            best_score = int(scores[index])
    return best_player, best_score


# ------------------------------
# App
# ------------------------------

game = Controller()
game.main()
     
#game.restore_control_state("floodit_control_state.txt")
