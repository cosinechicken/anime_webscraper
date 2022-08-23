from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import os

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

# Helper function to add the limit to a string if necessary
def add_limit(string):
    if limit > 0:
        return string + "-" + str(limit)
    return string

# Helper function to create the directory for data if it doesn't exist
def create_dir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
    print("Created Directory : ", dir)
  else:
    print("Directory already existed : ", dir)
  return dir

start_ns = time.time_ns()
# Prevent browser from being opened while scraping
op = webdriver.ChromeOptions()
op.add_argument('headless')

# Iterate through possible value of limits
for limit in range(150, 200, 50):
    # Scrape the archive for each year
    urls = []
    for i in range(15, 23):
        # 4-digit representation of the year
        year = i + 2000
        print(bcolors.HEADER + "Scraping: " + str(year) + bcolors.ENDC)
        url = 'https://web.archive.org/web/' + str(year) + '0101000000*/https://myanimelist.net/topanime.php'
        
        if limit > 0:
            url += ('?limit=' + str(limit))

        # Scrape the url
        driver = webdriver.Chrome(options=op)
        driver.get(url)
        # Sleep for 2 seconds to allow javascript to render
        time.sleep(3)
        htmlSource = driver.page_source         # Scraped HTML of the website

        soup = BeautifulSoup(htmlSource, 'lxml')    # Enable us to search the scraped HTML easily
        links = soup.find_all('a')                  # Find all links in the HTML

        num_appended = 0
        # Obtain the list of URLs we want to scrape
        for a in links:
            temp = str(a)
            if temp.find("myanimelist") != -1:                          # Eliminate junk URL's
                new_url = (temp.split("href=\"")[1].split("\">")[0])    # Format tag
                date_str = new_url.split("/")[2]
                if date_str[:4] == str(year) and len(date_str) == 8:    # Ensure URL is correct format
                    urls.append("https://web.archive.org" + new_url)
                    num_appended += 1
        print("")
        # Output warning message if some year did not have any URLs saved
        if num_appended == 0:
            print(bcolors.FAIL + str(year) + " was empty" + bcolors.ENDC)

    create_dir("data/" + str(limit))
    file_name = add_limit("data/urls") + ".txt"

    with open(file_name, 'w') as file:
        for url in urls:
            file.write(url + "\n")

    end_ns = time.time_ns()

    print(bcolors.HEADER + "Total time taken: " + str((end_ns - start_ns)/1000000000) + " s" + bcolors.ENDC)

    