from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

# Class to enable printing colors to console
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# helper method to add name, score, and members to data in string format
def add_data (data_, name_, score_, members_):
    if name_ == "None":
        raise Exception("Name was null")
    if score_ == "None":
        raise Exception("Score was null")
    if members_ == "None":
        raise Exception("Members was null")
    data_.append(name_ + ", " + score_ + ", " + members_)

# remove commas from string representation of number
def remove_commas(num):
    while num[0] == '\t' or num[0] == '\n' or num[0] == ' ':
        num = num[1:]
    while num[-1] == '\t' or num[-1] == '\n' or num[-1] == ' ':
        num = num[:-1]

    arr = num.split(",")
    new_str = ""
    for chunk in arr:
        new_str += chunk
    return new_str

start_ns = time.time_ns()
# Prevent browser from being opened while scraping
op = webdriver.ChromeOptions()
op.add_argument('headless')

urls = []
with open('data/urls.txt', 'r') as url_file:
    while True:
        next_url = url_file.readline()
        if len(next_url) == 0:
            break
        urls.append(next_url)

for next_url in urls:
    print(bcolors.HEADER + "Scraping: " + next_url + bcolors.ENDC)

    if next_url[0] == "#":
        continue

    # Scrape the url
    driver = webdriver.Chrome(options=op)
    driver.set_page_load_timeout(60)
    try:
        driver.get(next_url)
    except:
        print(bcolors.FAIL + "OUT OF TIME" + bcolors.ENDC)
    # Sleep for 2 seconds to allow javascript to render
    time.sleep(2)
    htmlSource = driver.page_source         # Scraped HTML of the website

    soup = BeautifulSoup(htmlSource, 'lxml')    # Enable us to search the scraped HTML easily
    try:
        # Turn the date into a string
        date_str = next_url.split("web/")[1].split("/")[0]
        data = []
        if int(date_str) < 20160120:
            rows = soup.find_all('td', class_="borderClass", align="left", valign="top")
            # Collect information about name, score, and members from each row
            for row in rows:
                name = str(row.contents[3].strong.string)
                score = str(row.contents[7].contents[0]).split("scored ")[1]
                members = remove_commas(str(row.contents[7].span.string).split(" ")[0])
                # Append the data to the array
                add_data(data, name, score, members)
                
        elif int(date_str) < 20160406:
            rows = soup.find_all('tr', class_="ranking-list")
            # Collect information about name, score, and members from each row
            for row in rows:
                name = str(row.contents[3].contents[3].contents[3].string)
                score = str(row.contents[5].div.span.string)
                members = remove_commas(str(row.contents[3].contents[3].contents[6].contents[4])).split(" members")[0]
                # Append the data to the array
                add_data(data, name, score, members)
        elif int(date_str) < 20160504:
            rows = soup.find_all('tr', class_="ranking-list")
            # Collect information about name, score, and members from each row
            for row in rows:
                name = str(row.contents[3].contents[3].contents[2].string)
                score = str(row.contents[5].div.span.string)
                members = remove_commas(str(row.contents[3].contents[3].contents[-1].contents[-1])).split(" members")[0]
                # Append the data to the array
                add_data(data, name, score, members)
        else:
            rows = soup.find_all('tr', class_="ranking-list")
            # Collect information about name, score, and members from each row
            for row in rows:
                name = str(row.contents[3].contents[3].contents[2].a.string)
                score = str(row.contents[5].div.span.string)
                members = remove_commas(str(row.contents[3].contents[3].contents[-1].contents[-1])).split(" members")[0]
                # Append the data to the array
                if name == "None":
                    raise Exception("Name was null")
                if score == "None":
                    raise Exception("Score was null")
                if members == "None":
                    raise Exception("Members was null")
                data.append(name + ", " + score + ", " + members)

        # If length was 0 then there was an error in scraping the files
        if len(data) == 0:
            raise Exception("File was empty")
        # If everything went well we write the data into the text files
        with open('data/' + date_str + '.txt', 'w', encoding='utf8') as txt_file:
            for data_point in data:
                txt_file.write(data_point + "\n")
    except Exception as e:
        print(next_url + " doesn't have the correct format.")
        print(bcolors.WARNING + "Scraping: " + str(e) + bcolors.ENDC)
        break