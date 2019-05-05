#!/usr/bin/env python
# coding: utf-8

#NASA Mars News


#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
    

# https://splinter.readthedocs.io/en/latest/drivers/chrome.html



#pointing to the directory where chromedriver existsr
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    listings = {}
    hemisphere_image_urls = []
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")



    #collect the latest News Title and Paragraph Text
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    
    #JPL Mars Space Images - Featured Image



    nasa_image= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_image)



    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #image = '/spaceimages/images/wallpaper/PIA19113-1920x1200.jpg'
    image = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image


    #Mars Weather

    nasa_image = "https://twitter.com/marswxreport?lang=en"
    browser.visit(nasa_image)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #Mars Facts

    nasa_fact = "https://space-facts.com/mars/"

    tables = pd.read_html(nasa_fact)


    df = tables[0]
    df.columns =['descrpition','value']
    df1= df.set_index('descrpition')

    #DataFrames as HTML
    
    df1.to_html('table.html')

    # Mars Hemispheres



    nasa_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(nasa_hemi)

    



    # loop through the four tags and load the data to the dictionary

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()



    listings["news_title"] = news_title
    listings["news_p"] = news_p
    listings["featured_image_url"] = featured_image_url
    listings["mars_weather"] = mars_weather
    #listings["table"] = mars_table 
    listings["hemisphere_image_urls"] = hemisphere_image_urls

    return listings








