# load modules
import csv

def read_game_scores(filename):
    # first cell data
    user_names = []

    # second cell data
    scores = []

    try:
        # open file for reading
        with open(filename) as csv_data_file:

            # open file as csv file
            csv_reader = csv.reader(csv_data_file)

            # loop over rows
            for row in csv_reader:

                # add cell [0] to list of dates
                user_names.append(row[0])

                # add cell [1] to list of scores
                scores.append(row[1])
    except:
        print("WARNING: file: \'" + filename + "\' not found.")

    return user_names, scores

# Write user names and scores to the given file.
# A new file will be created or an old file will be overwritten.
def write_game_scores(filename, user_names, scores):
    
    with open(filename, "w", newline='') as csv_data_file:
        
        csv_writer = csv.writer(csv_data_file, delimiter=',')
        
        for i in range(len(user_names)):
            csv_writer.writerow([user_names[i], scores[i]])
            

def test_game_scores(filename):
    # read old scores
    users, scores = read_game_scores(filename)

    # add a new score
    users.append("Fred")
    scores.append("57")

    write_game_scores(filename, users, scores)

    # show data
    print("Users: ", end="")
    print(users)
    print("Scores: ", end="")
    print(scores)
    print("No. of users = ", len(users))    
        
#----------------------------------------------------------------
    
#print("Functions to read from and write to a CSV file of user game scores.\n")
#print("Function \'read_game_scores(filename)\' returns user names and scores.")
#print("Function \'write_game_scores(filename, user_names, scores)\' saves user names and scores.")
#print("Function \'test_game_scores(filename)\' reads, modifies and writes user game scores.")
