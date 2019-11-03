# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from time import sleep
import re

hemisphere_image_urls = [
    {"title":"Cerberus Hemisphere Enhanced", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title":"Valles Marineris Hemisphere Enhanced", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title":"Schiaparelli Hemisphere Enhanced", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title":"Syrtis Major Hemisphere Enhanced", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}
]

def scrape():
    # Hi, Windows user initializing Splinter here...if you're a Mac user, comment this out and use the lines above
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # Run the function below:
    news_title, news_p = mars_news(browser)
    
    # Run the functions below and store into a dictionary
    mars_dict = {
        "news_title": news_title,
        "news_teaser": news_p,
        "featured_image_url": jpl_image(browser),
        "mars_weather": mars_weather_tweet(browser),
        "mars_facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
    }

    # Quit the browser and return the scraped results
    browser.quit()
    return mars_dict

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/?page=1&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    mars_news_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the first article title and teaser paragraph text; return them
    news_title = mars_news_soup.find('div', class_='content_title').text
    news_p = mars_news_soup.find('div', class_='article_teaser_body').text
    return news_title, news_p

def jpl_image(browser):
    #Activate driver
    browser = Browser('chrome')

    nasa_url = 'https://www.jpl.nasa.gov'
    #images_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16217_hires.jpg'
    destiny = str(nasa_url) + "/spaceimages/?search=&category=Mars"
    #Load source
    browser.visit(destiny)
    html_source = browser.html
    #Click <Full image> pic
    browser.find_by_id('full_image').click()
    #Go to More Info
    soup = BeautifulSoup(html_source, 'html.parser')
    #print(soup.prettify())
    buttons = soup.find('article', class_='carousel_item')
    url_pic = '/spaceimages/images/largesize/'
    id_pic = buttons.a['data-link'] + ":"
    #Get image ID cleaning id_pic string
    m = re.search('=(.+?):', id_pic)
    if m:
        featured_image_url = nasa_url + url_pic + m.group(1) + '_hires.jpg'
        browser.visit(featured_image_url)
        
    return featured_image_url

def mars_weather_tweet(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')
    
    # Scrape the tweet info and return
    mars_weather = tweet_soup.find('p', class_='TweetTextSize').text
    return mars_weather
    
def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    space_facts_df = tables[1]
    space_facts_df.columns = ['Property', 'Value']
    # Set index to property in preparation for import into MongoDB
    space_facts_df.set_index('Property', inplace=True)
    
    # Convert to HTML table string and return
    return space_facts_df.to_html()