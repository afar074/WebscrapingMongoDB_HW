
# coding: utf-8

# In[72]:


# Import dependencies needed 
from flask import Flask
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import time
from splinter import Browser


# In[2]:


executable_path = {'executable_path': '/Users/amgadfarah/Desktop/WebScrapingDB/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# NASA MARS NEWS

# In[3]:


# Scrape the NASA Mars News Site
def get_soup(url):
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = bs(nasa_html,'html.parser')
    return nasa_soup


# In[4]:


# Collect the latest News Title
def NASA_news():
    nasa_url = "https://mars.nasa.gov/news/"
    news_soup = get_soup(nasa_url)
    news = news_soup.find_all("div",{"class":"list_text"})[0]
    return {
        "news-title":news.find("div",{"class":"content_title"}).text,
        "news-content":news.find("div",{"class":"article_teaser_body"}).text
    }


# In[5]:


NASA_news()


# JPL Mars Space Images

# In[32]:


# Visit the url for JPL Featured Space Image
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)
html = browser.html
soup = bs(html, "html.parser")


# In[43]:


# assign the url string to a variable called `featured_image_url`
image = soup.find("img", class_="thumb")["src"]
featured_image_url = "https://www.jpl.nasa.gov" + image
print(featured_image_url)


# ### Make sure to save a complete url string for this image.
# https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA22666-640x350.jpg

# Mars Weather

# In[44]:


# Visit the Mars Weather twitter account
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather) 


# In[45]:


# Scrape the latest Mars weather tweet from the page. 
html_weather = browser.html
soup = bs(html_weather, "html.parser")


# In[46]:


# Save the tweet text for the weather report as a variable called `mars_weather`.
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)


# Mars Facts

# In[47]:


# Visit the Mars Facts webpage
mars_facts_url = "http://space-facts.com/mars/"


# In[48]:


# use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
table = pd.read_html(mars_facts_url)
table[0]


# In[52]:


df_mars_facts = table[0]
df_mars_facts.columns = ["Parameter", "Values"]
df_mars_facts


# In[57]:


# Use Pandas to convert the data to a HTML table string.
mars_html_table = df_mars_facts.to_html(header = False, index = False)
print(mars_html_table)


# Mars Hemispheres

# In[65]:


#Visit the USGS Astrogeology site
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)"
browser.visit(hemispheres_url)
html = browser.html
soup = bs(html, "html.parser")
mars_hemisphere = []
#You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image
products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")


# In[66]:


#Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name.
for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup= bs(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    mars_hemisphere.append({"title": title, "img_url": image_url})


# In[67]:


mars_hemisphere

