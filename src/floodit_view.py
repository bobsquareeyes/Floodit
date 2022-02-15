# ------------------------------
# Imports
# ------------------------------
from guizero import App, Window, Waffle, Box, Text, TextBox, PushButton
import pygame
from pygame import mixer

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
# ------------------------------
class View:
    def __init__(self, controller):
        self.controller = controller

    def main(self, board_codes):
        self._debug_1("In view.main()")
        self.app = App("Flood It")
        
        self.board = Waffle(self.app, width=self.controller.size,
                            height=self.controller.size, pad=0)
        self.palette = Waffle(self.app, width=len(self.controller.colours), height=1,
                              dotty=True, command=self.handle_set_next_colour)
        
        self.info_box = Box(self.app, layout="grid", border=10)
        self.info_box.set_border(thickness=10, color=self.app.bg)
        self.score_text = Text(self.info_box, grid=[0,0])     
        self.win_text = Text(self.info_box, grid=[1,0])
        self.win_text.value = "  "
        self.best_score_display = Text(self.info_box, grid=[2,0], text = "   Best score: " +
            self.controller.best_player +": " + str(self.controller.best_score))
        
        self.panel = Box(self.app, layout="grid", border=10)
        self.panel.set_border(thickness=10, color=self.app.bg)
        self.user_button = PushButton(self.panel, grid=[0,0], text="User: " + self.controller.user,
                                  command=self.handle_set_user)
        self.play_button = PushButton(self.panel, grid=[1,0], text="Play", command=self.handle_request_play)
        self.play_button.text_color = "grey"
        self.save_button = PushButton(self.panel, grid=[2,0], text="Save", command=self.handle_request_save)
        self.restore_button = PushButton(self.panel, grid=[3,0], text="Restore", command=self.handle_request_restore)

        # Stream background music from file, repeating continuously.
        pygame.init()
        mixer.music.load('background.wav')
        mixer.music.play(-1)
        
        self.show_board(board_codes)
        self._init_palette()
        self.reset_user_interface()
      
        # set up exit function
        self.app.when_closed = self.close_app
        
        # enter endless loop, waiting for user input.
        self.app.display()
        
    def reset_user_interface(self):
        self.user_button.text = "User: " + self.controller.user
        self.win_text.value = "   "
        self.score_text.value = "Move count: " + str(self.controller.moves_taken)
        self.score_text.show()
        self.best_score_display.value = "Best score: " + self.controller.best_player +": " + str(self.controller.best_score)
        self.best_score_display.show()
        self.play_button.text_color = "grey"
        mixer.music.unpause()
                            
    def show_board(self, board_codes):        
        self._debug_2(board_codes[0:self.controller.size, 0:self.controller.size])
        for x in range(self.controller.size):
            for y in range(self.controller.size):
                self.board.set_pixel(y, x, self.controller.colours[board_codes[x,y]])
             
    def show_user(self):        
        self.user_button.text = "User: " + self.controller.user
             
    def show_info(self):
        self._debug_1("Moves taken = " + str(self.controller.moves_taken))
        self.score_text.value = "Move count: " + str(self.controller.moves_taken)
        self.best_score_display.value = "Best score: " + self.controller.best_player + ": " + str(self.controller.best_score)
        if self.controller.success == True:
            self.win_text.value = "You win!"
            self.score_text.hide()
            self.best_score_display.hide()
            self.play_button.text_color = "black"
            mixer.music.pause()
            
    def close_app(self):
        print("\nFinal score: " + str(self.controller.moves_taken))
        mixer.music.stop()
        self.app.destroy()
    
    #################### Helper Functions ################
        
    def _init_palette(self):
        for x in range(len(self.controller.colours)):
            self.palette.set_pixel(x, 0, self.controller.colours[x])
            
    def _debug_1(self, message):
        # pass
        print(message)
        
    def _debug_2(self, message):
        # pass
        print(message)
    
    #################### Event Handlers ##################
    
    def handle_request_play(self):
        self.controller.on_request_play()
        
    def handle_request_save(self):
        self.controller.on_request_save()
        
    def handle_request_restore(self):
        self.controller.on_request_restore()
        
    def handle_set_next_colour(self, x, y):
        self._debug_2("Start flood with: (" + str(x) + ", " + str(y) + ")")
        flood_colour = self.palette.get_pixel(x,y)
        self._debug_2("Selected colour = " + flood_colour)
        self.controller.on_next_colour(x)

    def handle_set_user(self):
        new_user = self.app.question("Hello", "What's your name?")
        # If cancel is pressed, None is returned so check a name was entered
        if new_user is not None and new_user.isalnum():
            self.controller.on_change_user(new_user)          

#--------------------------- end of View class ---------------------------

