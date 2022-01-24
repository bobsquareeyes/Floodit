# load modules
import csv

def read_game_settings(filename):

    # first and second column data arrays (strings)
    setting_names = []
    setting_values = []

    try:
        # open file for reading
        with open(filename) as csv_data_file:

            # open file as csv file
            csv_reader = csv.reader(csv_data_file)

            # loop over rows
            for row in csv_reader:

                # add cell [0] to list of names
                setting_names.append(row[0])

                # add cell [1] to list of values
                setting_values.append(row[1])
    except:
        print("WARNING: file: \'" + filename + "\' not found.")
        
    # set default values
    board_size = 14
    current_user = "Anonymous"
    colours = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
        
    # update settings with new values from file, if available
    new_colours = []
    for i in range(len(setting_names)):
        if setting_names[i] == "board_size":
            board_size = int(setting_values[i])
        elif setting_names[i] == "current_user":
            current_user = setting_values[i]
        elif setting_names[i] == "colour":
            new_colours.append(setting_values[i])

    if (len(new_colours) > 4):
        colours = new_colours

    return board_size, current_user, colours

# Write user names and settings to the given file.
# A new file will be created or an old file will be overwritten.
def write_game_settings(filename, board_size, current_user, colours):
    
    setting_names = []
    setting_values = []
    
    setting_names.append("board_size")
    setting_values.append(str(board_size))
    
    setting_names.append("current_user")
    setting_values.append(current_user)
    
    for i in range(len(colours)):
        setting_names.append("colour")
        setting_values.append(str(colours[i]))

    with open(filename, "w", newline='') as csv_data_file:
        
        csv_writer = csv.writer(csv_data_file, delimiter=',')
        
        for i in range(len(setting_names)):
            csv_writer.writerow([setting_names[i], setting_values[i]])
            

def test_game_settings(filename):
    # read old settings
    board_size, current_user, colours = read_game_settings(filename)

    # add a new setting
    colours.append("pink")

    write_game_settings(filename, board_size, current_user, colours)

    # show data
    print("board_size = " + str(board_size))
    print("current_user = " + current_user)
    print("colours = ", end="")
    print(colours)   
        
#----------------------------------------------------------------
    
#print("Functions to read from and write to a CSV file of game settings.\n")
#print("Function \'read_game_settings(filename)\' returns game settings and values.")
#print("Function \'write_game_settings(filename, setting_names, setting_values)\' saves game settings and values.")
#print("Function \'test_game_settings(filename)\' reads, modifies and writes game settings.")
