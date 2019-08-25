from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # C:\Users\blake\Desktop\Cromedriver
    executable_path = {"executable_path": "C:/Users/blake/Desktop/Cromedriver/chromedriver.exe"}
    return Browser("chrome", ** executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    news = soup.find('div', id='page')
    news_title = news.find_all('a')[1].text
    news_pra = news.find_all('a')[0].text

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_pra

    base_url = "https://www.jpl.nasa.gov"
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    featured_img = soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img = featured_img.split("'")[1]
    featured_img_url = base_url + featured_img
    mars_data["featured_img_url"] = featured_img_url



    twitter_url= "https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    soup = bs(response.text, 'html.parser')
    mars_weather= soup.find(class_="TweetTextSize").text.strip()
    mars_data["mars_weather"] = mars_weather

    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.set_index('Mars - Earth Comparison', inplace=True)
    
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    mars_data["mars_facts"] = html_table

    hemisphere_image_urls = []
    hem_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response= requests.get(hem_url)
    soup = bs(response.text, 'html.parser')
    for hem_info in soup.find_all(class_='item'):
        title= hem_info.find('h3').text.strip()
        url_img_link = hem_info.find('a')
        img_link = url_img_link['href']
        url_img = "https://astrogeology.usgs.gov" + img_link
        response= requests.get(url_img)
        soup = bs(response.text, 'html.parser')
        pic_url = soup.find("a", target="_blank")
        url_link = pic_url['href']
        hemisphere_image_urls.append({"title":title,"img_url":url_link})

    mars_data["mars_hemisphere"] = hemisphere_image_urls

    return mars_data
