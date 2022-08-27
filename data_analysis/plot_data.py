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
animes = set()                          # Set of anime names not in top 200 of MAL today
final_animes = set()                    # Set of anime names in top 200 of MAL today
# Some animes may go under two names. For consistency we change the name to the one currently on MAL
name_swap = {
    "Kono Oto Tomare! 2nd Season": "Kono Oto Tomare! Part 2",
    "Gintama Movie: Shinyaku Benizakura-hen": "Gintama Movie 1: Shinyaku Benizakura-hen",
    "Gintama. Porori-hen": "Gintama.: Porori-hen",
    "JoJo no Kimyou na Bouken: Stardust Crusaders 2nd Season": "JoJo no Kimyou na Bouken Part 3: Stardust Crusaders 2nd Season",
    "Gintama.: Shirogane no Tamashii-hen 2": "Gintama.: Shirogane no Tamashii-hen - Kouhan-sen",
    "86 2nd Season": "86 Part 2",
    "Mo Dao Zu Shi 2": "Mo Dao Zu Shi: Xian Yun Pian",
    "Ansatsu Kyoushitsu (TV) 2nd Season": "Ansatsu Kyoushitsu 2nd Season",
    "YURI!!! on ICE": "Yuri!!! on Ice",
    "Yuri!!! on ICE": "Yuri!!! on Ice",
    "Kara no Kyoukai 7: Satsujin Kousatsu (Go)": "Kara no Kyoukai Movie 7: Satsujin Kousatsu (Go)",
    "Detective Conan: Episode One - Chiisaku Natta Meitantei": "Detective Conan: Episode One - The Great Detective Turned Small",
    "JoJo no Kimyou na Bouken: Diamond wa Kudakenai": "JoJo no Kimyou na Bouken Part 4: Diamond wa Kudakenai",
    "Fruits Basket (2019)": "Fruits Basket 1st Season",
    "Haikyuu!!: To the Top": "Haikyuu!! To the Top",
    "Gintama Movie: Kanketsu-hen - Yorozuya yo Eien Nare": "Gintama Movie 2: Kanketsu-hen - Yorozuya yo Eien Nare",
    "Kono Subarashii Sekai ni Shukufuku wo!: Kurenai Densetsu": "Kono Subarashii Sekai ni Shukufuku wo! Movie: Kurenai Densetsu",
    "JoJo no Kimyou na Bouken (2012)": "JoJo no Kimyou na Bouken (TV)",
    "Mushoku Tensei: Isekai Ittara Honki Dasu 2nd Season": "Mushoku Tensei: Isekai Ittara Honki Dasu Part 2",
    "Fate/stay night: Unlimited Blade Works (TV) 2nd Season": "Fate/stay night: Unlimited Blade Works 2nd Season",
    "Bakuman. 2": "Bakuman. 2nd Season",
    "Girls und Panzer der Film": "Girls & Panzer Movie",
    "Kizumonogatari Part 1: Tekketsu-hen": "Kizumonogatari I: Tekketsu-hen",
    "Tengen Toppa Gurren Lagann Movie: Lagann-hen": "Tengen Toppa Gurren Lagann Movie 2: Lagann-hen",
    "Fate/stay night: Unlimited Blade Works (TV)": "Fate/stay night: Unlimited Blade Works",
    "Bakuman. 3": "Bakuman. 3rd Season",
    "Working!!! Lord of the Takanashi": "Working!!!: Lord of the Takanashi",
    "Haikyuu!!: To the Top 2nd Season": "Haikyuu!! To the Top Part 2",
    "Mo Dao Zu Shi 2nd Season": "Mo Dao Zu Shi: Xian Yun Pian",
    "Hunter x Hunter OVA": "Hunter x Hunter: Original Video Animation", 
    "Fate/stay night: Unlimited Blade Works (TV) - Prologue": "Fate/stay night: Unlimited Blade Works - Prologue",
    "Hunter x Hunter: Yorkshin City Kanketsu-hen": "Hunter x Hunter: Original Video Animation",
    "Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuiokuhen": "Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuioku-hen",
    "Kara no Kyoukai 5: Mujun Rasen": "Kara no Kyoukai Movie 5: Mujun Rasen",
    "JoJo no Kimyou na Bouken: Ougon no Kaze": "JoJo no Kimyou na Bouken Part 5: Ougon no Kaze",
    "One Piece Film Z": "One Piece Film: Z",
    "Ping Pong The Animation": "Ping Pong the Animation",
    "Haikyuu!!: Karasuno Koukou VS Shiratorizawa Gakuen Koukou": "Haikyuu!!: Karasuno Koukou vs. Shiratorizawa Gakuen Koukou",
    "Pingu in the City 2nd Season": "Pingu in the City (2018)",
    "Shiguang Daili Ren": "Shiguang Dailiren",
    "Ghost in the Shell: Stand Alone Complex": "Koukaku Kidoutai: Stand Alone Complex",
    "Rose of Versailles": "Versailles no Bara",
    "Ghost in the Shell: Stand Alone Complex 2nd GIG": "Koukaku Kidoutai: Stand Alone Complex 2nd GIG",
    "Mushishi Special: Hihamukage": "Mushishi: Hihamukage",
    "Steins;Gate: Fuka Ryouiki no Déjà vu": "Steins;Gate Movie: Fuka Ryouiki no Déjà vu",
    "Haikyuu!! To the Top 2nd Season": "Haikyuu!! To the Top Part 2",
    "Quanzhi Gaoshou: Tebie Pian": "Quanzhi Gaoshou Specials",
    "Gintama. (2017)": "Gintama.",
    "Saiki Kusuo no Ψ-nan (TV) 2": "Saiki Kusuo no Ψ-nan 2",
    "Koukaku Kidoutai S.A.C. 2nd GIG": "Koukaku Kidoutai: Stand Alone Complex 2nd GIG"
}

# Get list of all files
def populate():
    for i in range(0, 200, 50):
        directory = os.fsencode("data/" + str(i))
        
        # Go through all files in directory
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            days_str = date_to_days(filename[:-4].split("-")[0])
            # Open each file and read its contents
            with open("data/" + str(i) + "/" + filename, 'r', encoding='utf8') as f:
                while True:                             # Read more lines until no lines left
                    next_line = f.readline()
                    if len(next_line) == 0:
                        break
                    next_line = next_line[:-1]          # Remove newline at the end
                    temp = next_line.split(", ")        # Separate data
                    anime_name_list = temp[0:-2]        # In case anime name has a comma
                    anime_name = ""
                    # Add commas back into the name
                    for piece in anime_name_list:
                        anime_name += (piece + ", ")
                    anime_name = anime_name[:-2]
                    if anime_name in name_swap:         # Swap name if necessary
                        anime_name = name_swap[anime_name]
                    anime_score = temp[-2]
                    anime_members = temp[-1]
                    animes.add(anime_name)
                    if (days_str > date_to_days("20220731")):
                        final_animes.add(anime_name)
                    if not (anime_name in members):     # Add data into dictionaries
                        members[anime_name] = {}
                        score[anime_name] = {}
                    # print(str(days_str) + " " + anime_name)
                    score[anime_name][days_str] = float(anime_score)
                    members[anime_name][days_str] = int(anime_members)
    
    # Find anime with less than 30 datapoints
    bad_anime = []
    for anime_name in score:
        if len(score[anime_name]) < 30:
            bad_anime.append(anime_name)

    # Remove anime with less than 30 datapoints
    for anime in bad_anime:
        score.pop(anime)
        members.pop(anime)
        if anime in animes:
            animes.remove(anime)
        if anime in final_animes:
            final_animes.remove(anime)

    # Record data into out.txt
    with open("out.txt", 'w', encoding='utf8') as f:
        for i in members:
            for j in members[i]:
                # f.write(i + ":::" + str(j) + ":::" + str(score[i][j]) + "\n")
                k = 1

populate()

# Record list of anime remaining
with open("out.txt", 'a', encoding='utf8') as f:
    counter = 0
    for anime in animes:
        if anime in final_animes:
            continue
        counter += 1
        f.write(anime + "\n")
    counter = 0
    for anime in final_animes:
        counter += 1
        f.write(anime + "\n")

# Plot score of YLIA over time
anime_names = list(final_animes)
days_arr = []
temp = []
for i in range(len(anime_names)):
    temp.append([])

for i in range(5711, 8271):
    days_arr.append(i)
df_dict = {'Days': days_arr}        # First column of the dataframe

# Add joint data into temp
max_arr = []
for j in range(len(anime_names)):
    prev = 10000
    max_diff = 0
    diff = (0,0)
    for i in range(5711, 8271):
        try:
            temp[j].append(score[anime_names[j]][i])
            max_diff = max(max_diff, i - prev)
            if max_diff == i - prev:
                diff = (i, prev)
            prev = i
        except:
            temp[j].append(np.NaN)
    max_arr.append(max_diff)
    print(anime_names[j] + ": " + str(max_arr[j]) + "; " + days_to_date(diff[0]) + ", " + days_to_date(diff[1]))
print(max(1,2))
# Add data in temp to dataframe
for j in range(len(anime_names)):
    if anime_names[j] == "Cowboy Bebop: Tengoku no Tobira":
        df_dict[j] = temp[j]

data_preproc = pd.DataFrame(df_dict)
print(data_preproc.head())
# Plot the dataframe
ax = sns.lineplot(x='Days', y='value', hue='variable', 
             data=pd.melt(data_preproc, ['Days']))
ax.set(xlabel ='Days', ylabel ='Score')

# for legend text
plt.setp(ax.get_legend().get_texts(), fontsize='5') 
 
# for legend title
plt.setp(ax.get_legend().get_title(), fontsize='5') 
plt.title("ANIME SCORES")
plt.show()