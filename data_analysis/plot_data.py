import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt


days_in_month = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

# Helper method to get number of days since Jan 1 2000 from date string
# Leap year rules about multiples of 100 ignored
def date_to_days(date):
    year = int(date[2:4])
    month = int(date[4:6])
    day = int(date[6:8])
    # Determine whether we need to take leap year for this year into account
    if month <= 2 and year % 4 == 0:
        before_leap_year = True
    else:
        before_leap_year = False
    ans = 365 * year + np.sum(days_in_month[0:month - 1]) + day + (year//4)
    if not before_leap_year:
        ans += 1
    return ans

# Helper function to pad number with 0's to the front
def to_two_digit_string(num):
    if num < 10:
        return "0" + str(num)
    return str(num)

# Helper method to get date string from number of days since Jan 1 2000
def days_to_date(days):
    year = days // 365          # Number of full years after 2000
    remainder = days - (year * 365) - ((3 + year) // 4)
    if remainder <= 0:
        year -= 1
        remainder = days - (year * 365) - ((3 + year) // 4)
    month = 1
    # Take leap yaers into account
    if year % 4 == 0:
        days_in_month[1] += 1
    while remainder > days_in_month[month - 1]:
        remainder -= days_in_month[month - 1]
        month += 1
    # Undo changes for leap year
    if year % 4 == 0:
        days_in_month[1] -= 1
    return "20" + to_two_digit_string(year) + to_two_digit_string(month) + to_two_digit_string(remainder)

members = {}
score = {}

# Get list of all files
def populate():
    for i in range(0, 200, 50):
        directory = os.fsencode("data/" + str(i))
        
        # Go through all files in directory
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            days_str = date_to_days(filename[:-4].split("-")[0])
            # Open each file and read its contents
            with open("data/" + str(i) + "/" + filename, 'r') as f:
                while True:                             # Read more lines until no lines left
                    next_line = f.readline()
                    if len(next_line) == 0:
                        break
                    next_line = next_line[:-1]          # Remove newline at the end
                    temp = next_line.split(", ")        # Separate data
                    anime_name_list = temp[0:-2]        # In case anime name has a comma
                    anime_name = ""
                    for piece in anime_name_list:
                        anime_name += (piece + ", ")
                    anime_name = anime_name[:-2]
                    anime_score = temp[-2]
                    anime_members = temp[-1]
                    if not (anime_name in members):     # Add dataframe into dictionaries
                        members[anime_name] = {}
                        score[anime_name] = {}
                    # print(str(days_str) + " " + anime_name)
                    score[anime_name][days_str] = float(anime_score)
                    members[anime_name][days_str] = int(anime_members)
    # Record data into out.txt
    with open("out.txt", 'w') as f:
        for i in members:
            for j in members[i]:
                f.write(i + ":::" + str(j) + ":::" + str(score[i][j]) + "\n")

populate()

# Plot score of YLIA over time
anime_name = "Shigatsu wa Kimi no Uso"
days_arr = []
date_arr = []
for i in score[anime_name]:
    days_arr.append(i)
    date_arr.append(days_to_date(i))
days_arr.sort()
scores_arr = []
for i in days_arr:
    scores_arr.append(score[anime_name][i])
ax = sns.lineplot(x=days_arr, y=scores_arr, markers=True)
ax.set(xlabel ='Days', ylabel ='Score')
plt.title(anime_name)
plt.show()