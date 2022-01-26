# ------------------------------
# Imports
# ------------------------------
import random
import numpy as np
import json
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


    def fill_board(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                code = random.randint(0,self.num_codes-1)
                self.board[x, y] = code
        self.moves_taken = 0
        return self.board
    
    
    def start_flood(self, flood_code):
        print("Flood code = " + str(flood_code))
        if flood_code >= 0 and flood_code < self.num_codes:
            target = self.board[0,0]
            self.flood(0, 0, target, flood_code)
            self.moves_taken += 1
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
    
    
    def save_model_state(self, filename):

        try:
            # open file for writing
            with open(filename, 'w+') as writer:
                
                writer.writelines("board_size\n")
                writer.writelines(str(self.board_size) + "\n")
                writer.writelines("num_codes\n")
                writer.writelines(str(self.num_codes) + "\n")
                
                writer.writelines("board\n")
                for i in range(self.board_size):
                    line = str(list(self.board[i])) + "\n"
                    writer.writelines(line)
                
                print("Saved model state in: " + filename)
                writer.close()
        except:
            print("WARNING: file: \'" + filename + "\' write error")
                
        
    def restore_model_state(self, filename):

        try:
            # open file for reading
            with open(filename, 'r') as reader:

                print("Restoring model state from file: " + filename)
                
                lines = reader.readlines()
                print("No of lines = " + str(len(lines)))
                
                i = 0
                while i < len(lines) - 1:
                    
                    if "board_size" in lines[i]:
                        self.board_size = int(lines[i+1])
                        print("board_size = " + str(self.board_size))
                        
                    if "num_codes" in lines[i]:
                        self.num_codes = int(lines[i+1])
                        print("num_codes = " + str(self.num_codes))
                        
                    if i > 1 and "board" in lines[i]:

                        for j in range(self.board_size):
                            row = lines[i+j+1]
                            #print("row = " + row)
                            self.board[j] = np.array(json.loads(row))
                    
                        print("board = ")
                        print(self.board)
                        i += self.board_size
                        
                    i += 1

                reader.close()
                
        except:
            print("WARNING: error reading file: \'" + filename + "\' ")
        
        return self.board
    
#############################################################################

#m = Model(8, 7)
#m.fill_board()