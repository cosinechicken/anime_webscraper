import pandas as pd
import numpy as np
import os

members = {}
score = {}

# Get list of all files
def populate():
    for i in range(0, 200, 50):
        directory = os.fsencode("data/" + str(i))
        
        # Go through all files in directory
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            date_str = filename[:-4].split("-")[0]
            # Open each file and read its contents
            with open("data/" + str(i) + "/" + filename, 'r') as f:
                while True:                             # Read more lines until no lines left
                    next_line = f.readline()
                    if len(next_line) == 0:
                        break
                    next_line = next_line[:-1]          # Remove newline at the end
                    temp = next_line.split(", ")        # Separate data
                    anime_name = temp[0]
                    anime_score = temp[1]
                    anime_members = temp[2]
                    if not (anime_name in members):     # Add dataframe into dictionaries
                        members[anime_name] = {}
                        score[anime_name] = {}
                    members[anime_name][date_str] = anime_members
                    score[anime_name][date_str] = anime_score

with open("out.txt", 'w') as f:
    for i in members:
        for j in members[i]:
            f.write(i + ": " + j + ", " + score[i][j] + "\n")
