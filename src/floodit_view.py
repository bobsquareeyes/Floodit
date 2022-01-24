# ------------------------------
# Imports
# ------------------------------

from guizero import App, Window, Waffle, Text, TextBox, PushButton

# ------------------------------
# Variables
# ------------------------------

# ------------------------------
#  Notes:
#  
#  1. None of the View method functions return any values.
#  2. The View methods can read and write View variables.
#  3. The View methods can read but not write Controller variables.
#  4. View data is transferred to the Controller using Controller request methods.
#  5. The View class only communicates with the Controller, not the Model.
#  6. All the commands called by GUI widgets are event handler methods in the View class.
#     This enables the appropriate data to be sent to the controller, independent of any
#     Widget peculiarities or limitations.
#  7. All class method names begin with a verb describing the action to be performed.
# ------------------------------

class View:
    def __init__(self, controller):
        self.controller = controller

   
    def main(self, board_codes):
        print("In view.main()")
        self.app = App("Flood It")
        self.button = PushButton(self.app, text="User: " + self.controller.user,
                                 command=self.handle_set_user)
        self.board = Waffle(self.app, width=self.controller.size,
                            height=self.controller.size, pad=0)
        self.palette = Waffle(self.app, width=len(self.controller.colours),
                              height=1, dotty=True, command=self.handle_set_next_colour)
        self.score_text = Text(self.app)
        self.win_text = Text(self.app)

        self.best_score_display = Text(self.app, text = "Best score: " +
            self.controller.best_player +": " + str(self.controller.best_score))
        
        self.replay_button = PushButton(self.app, command=self.handle_request_replay, text="Replay")
        self.replay_button.bg = "green"
        self.replay_button.text_size = 20

        self.settings_button = PushButton(self.app, text="Settings", command=self.handle_modify_settings)

        self.show_board(board_codes)
        self.init_palette()
        self.reset_board()
        # enter endless loop, waiting for user input.
        self.app.display()
        
        
    def reset_board(self):
        self.win_text.hide()
        self.score_text.value = "Move count: " + str(self.controller.moves_taken)
        self.best_score_display.value = "Best score: " + self.controller.best_player +": " + str(self.controller.best_score)
        self.replay_button.hide()
                
                
    def show_board(self, board_codes):        
        self.button.text = "User: " + self.controller.user
        print(board_codes[0:self.controller.size, 0:self.controller.size])
        for x in range(self.controller.size):
            for y in range(self.controller.size):
                self.board.set_pixel(y, x, self.controller.colours[board_codes[x,y]])
        
        
    def show_user(self):        
        self.button.text = "User: " + self.controller.user
        
        
    def show_scores(self):
        print("Moves taken = " + str(self.controller.moves_taken))
        self.score_text.value = "Move count: " + str(self.controller.moves_taken)
        self.best_score_display.value = "Best score: " + self.controller.best_player + ": " + str(self.controller.best_score)
        if self.controller.success == True:
            self.win_text.value = "You win!"
            self.win_text.show()
            self.replay_button.show()
        
        
    def init_palette(self):
        for x in range(len(self.controller.colours)):
            self.palette.set_pixel(x, 0, self.controller.colours[x])
    
    #################### Event Handlers ##################
    
    def handle_request_replay(self):
        self.controller.request_replay()
        
            
    def handle_set_next_colour(self, x, y):
        #print("Start flood with: (" + str(x) + ", " + str(y) + ")")
        flood_colour = self.palette.get_pixel(x,y)
        print("Selected colour = " + flood_colour)
        self.controller.select_next_colour(x)


    def handle_set_user(self):
        new_user = self.app.question("Hello", "What's your name?")
        # If cancel is pressed, None is returned so check a name was entered
        if new_user is not None and new_user.isalnum():
            self.controller.change_user(new_user)          


    def handle_modify_settings(self):
        self.input_window = Window(self.app, "Modify Settings", height=200)
        Text(self.input_window, text="User name", size=15)
        self.input_box_1 = TextBox(self.input_window, width=30)
        Text(self.input_window, text="Board Size", size=15)
        self.input_box_2 = TextBox(self.input_window, width=30)
        self.input_box_1.focus()
        PushButton(self.input_window, text="Continue", command=self.handle_save_settings)
        

    # Check for valid inputs and send any new data to the controller.    
    def handle_save_settings(self):     
        new_user = self.input_box_1.value  
        if new_user is not None and new_user.isalnum():
            self.controller.change_user(new_user) 
        new_size = self.input_box_2.value
        if new_size is not None and new_size.isdecimal():
            self.controller.change_size(int(new_size)) 
        print("Board size: " + str(self.controller.size) + ", User: " + self.controller.user)
        self.input_window.destroy()
 
#--------------------------- end of View class ---------------------------
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
