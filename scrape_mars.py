#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

import pandas as pd

def scrape():
    # #NASA Mars News

    # In[2]:


    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'


    # In[3]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)


    # In[4]:


    # Retrieve page with the requests module
    browser.visit(url)

    # Create BeautifulSoup object
    soup = bs(browser.html,'html.parser')
    headline = soup.select_one("ul.item_list li.slide")
    #print(temp)
    news_title = headline.find('div', class_='content_title').a.text
    news_p = headline.find('div', class_='article_teaser_body').text


    # #JPL Mars Space Images - Featured Image

    # In[5]:


    # URL of page to be scraped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


    # In[6]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)


    # In[7]:


    #Visit JPL URL
    browser.visit(jpl_url)
    soup = bs(browser.html,'html.parser')

    jpl_base_url = "https://www.jpl.nasa.gov"

    #Retrieve URL to page with featured image - full
    path = soup.select_one("a.button")["data-link"]


    # In[8]:


    #go to page with featured image - full
    browser.visit(jpl_base_url + path)

    soup = bs(browser.html,'html.parser')
    path = soup.select_one("img.main_image")["src"]
    featured_image_url = jpl_base_url + path


    # #Mars Weather

    # In[9]:


    url = 'https://twitter.com/marswxreport?lang=en'


    # In[10]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)


    # In[11]:


    # Retrieve page with the requests module
    browser.visit(url)

    # Create BeautifulSoup object
    soup = bs(browser.html,'html.parser')
    #mars_weather = soup.select_one("div.content p.TweetTextSize").text
    tweets = soup.select("div.js-tweet-text-container p.TweetTextSize")
    for tweet in range(len(tweets)):
    #Top tweet might not have the weather info as in the case of a pinned tweet, search for tweet that begins 
    #with "InSight sol" which appears to be the pattern
        if(tweets[tweet].text.startswith("InSight sol")):
                mars_weather = tweets[tweet].text
                break

    mars_weather


    # #Mars Facts

    # In[12]:


    mars_facts_url = 'https://space-facts.com/mars/'


    # In[13]:


    tables = pd.read_html(mars_facts_url)
    mars_facts = tables[1]

    mars_facts.columns = ['value' , 'description']

    mars_facts.set_index('description',inplace=True)

    mars_facts = mars_facts.to_html()


    # In[ ]:





    # #Mars Hemispheres

    # In[14]:


    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # In[15]:


    # Retrieve page with the requests module
    browser.visit(mars_hemispheres_url)

    # Create BeautifulSoup object
    soup = bs(browser.html,'html.parser')

    base_url="https://astrogeology.usgs.gov"

    #Get div with the items
    mars_hemispheres_all = soup.find("div", class_="collapsible results")


    #mars_hemispheres_desc has path to page with link to the full image
    mars_hemispheres_desc = mars_hemispheres_all.find_all("div", class_="description")

    #h3 has the title
    mars_hemispheres_titles = mars_hemispheres_all.find_all("h3")

    #list to store the titles & URLs
    hemisphere_image_urls = []


    for hemisphere in range(len(mars_hemispheres_desc)):
        #get a tag
        a = mars_hemispheres_desc[hemisphere].find("a", class_="itemLink product-item")
        
        #img_url - URL to the page with the full image
        img_url = base_url + a['href']
        
        #visit page with the full image
        browser.visit(img_url)    
        soup = bs(browser.html,'html.parser')
        
        #retrieve URL to the full image
        img_url = soup.find("div", class_="downloads").find('a')['href'] 
        
        #save to the dictionary    
        hemisphere_image_urls.append({'title' : mars_hemispheres_titles[hemisphere].text, 'img_url': img_url})
    
    
    
    scrape_dict =[]
    scrape_dict.append({'news_title': news_title, 'news_p': news_p, 'featured_image_url': featured_image_url, 'mars_weather': mars_weather,'mars_facts':mars_facts, 'hemisphere_image_urls': hemisphere_image_urls}) #hemisphere_image_urls

    return scrape_dict



