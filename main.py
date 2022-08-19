from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

op = webdriver.ChromeOptions()
op.add_argument('headless')

url = 'https://web.archive.org/web/20220101000000*/https://myanimelist.net/topanime.php'

driver = webdriver.Chrome(options=op)
driver.get(url)
time.sleep(2)
htmlSource = driver.page_source

soup = BeautifulSoup(htmlSource, 'lxml')
links = soup.find_all('a')
for a in links:
    if str(a).find("myanimelist") != -1:
        print(a)

if __name__ == '__main__':
    print("HI")
    