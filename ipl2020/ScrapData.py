import requests
from bs4 import BeautifulSoup
import time

def geturls():
    homepage = 'https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-results'
    page = requests.get(homepage)
    soup = BeautifulSoup(page.content, 'html.parser')
    fixtures = soup.find(class_='card content-block league-scores-container').findAll(class_='match-info-link-FIXTURES')
    commentaryUrls = []
    for fixture in fixtures:
        href = fixture.get('href')
        url = 'https://www.espncricinfo.com'+href.replace('full-scorecard','ball-by-ball-commentary')
        commentaryUrls.append(url)
    return commentaryUrls

def getCommentary(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    #opts = Options()
    #opts.add_argument('- headless') scroll doesnt work with headless
    chrome_driver = r'D:\Downloads\chromedriver\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver)
    SCROLL_PAUSE_TIME = 0.5

    driver.get(url)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser').find(class_='match-body')
    comments = soup.findAll(class_='match-comment')
    for comment in comments:
        over = comment.find(class_='match-comment-over').text
        short_text = comment.find(class_='match-comment-short-text').text
        long_text = comment.find("div", {"class": "match-comment-long-text", "itemprop":"articleBody"}).text

if __name__ == '__main__':
    commentaryUrls = geturls()
    testUrl = commentaryUrls[-1]
    commentary = getCommentary(testUrl)