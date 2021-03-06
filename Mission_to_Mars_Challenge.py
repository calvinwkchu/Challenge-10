#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[10]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[13]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[15]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[16]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[20]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[21]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

html = browser.html
hemisphere_soup = soup(html,'html.parser')

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for x in range(len(hemisphere_soup.find_all('h3'))):
    
    # Create empty dict
    hemisphere = {}
    
    # Go to heading page to download image
    full_image_elem = browser.find_by_tag('h3')[x]
    full_image_elem.click()

    html = browser.html
    hemisphere_soup = soup(html,'html.parser')

    # Grab jpg from website
    img_url = hemisphere_soup.select_one('div.downloads a').get('href')

    # Get title of website
    title_url = hemisphere_soup.find('h2', class_='title').get_text()
   
    # Define dict to hold values
    hemisphere = {'img_url':img_url,
                  'title':title_url}        
    
    # Put dictionary results onto earlier defined list
    hemisphere_image_urls.append(hemisphere)
    
    # Loop back to main page
    browser.visit(url)


# In[22]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[23]:


# 5. Quit the browser
browser.quit()


# In[ ]:




