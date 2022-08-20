from datetime import date
from tkinter import W
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
    driver.get(next_url)
    # Sleep for 2 seconds to allow javascript to render
    time.sleep(2)
    htmlSource = driver.page_source         # Scraped HTML of the website

    soup = BeautifulSoup(htmlSource, 'lxml')    # Enable us to search the scraped HTML easily
    try:
        rows = soup.find_all('tr')
        scores = []
        for row in rows:
            name = row.contents[4]
            if len(str(name)) > 1:
                try_strong = name.strong
                if try_strong is None:
                    key = str(name.string)
                else:
                    key = str(name.strong.string)

                score = row.contents[6]
                scores.append(key + ", " + str(score.string))
        date_str = next_url.split("web/")[1].split("/")[0]
        with open('data/' + date_str + '.txt', 'w') as txt_file:
            for score in scores:
                txt_file.write(score + "\n")
    except Exception as e:
        print(next_url + " doesn't have the correct format.")
        print(bcolors.WARNING + "Scraping: " + str(e) + bcolors.ENDC)
        break