import pandas as pd
import numpy as np
import os

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

### TEST ### 
is_good = True
for i in range(1,8272):
    print(days_to_date(i))
    if date_to_days(days_to_date(i)) != i:
        is_good = False
print(is_good)
### END TEST ###

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

populate()

with open("out.txt", 'w') as f:
    for i in members:
        for j in members[i]:
            f.write(i + ": " + j + ", " + score[i][j] + "\n")
