#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Quit the browser to stop using our resources:
    browser.quit()

    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page: wait a second before searching for components since the website may have heavy-loading images
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # set up the HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # pinpoints the <ul /> tag with a class of “item_list”, and the <li /> tag with the class of “slide.”
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Get the title: div tag, class = content_title
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the FIRST `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        news_p

    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

    # Steps to get the full-size original image size:
    # 1. visit the webpage, click the 'Full Image'
    # 2. Click "more info" button
    # 3. click on the image

def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the 'more info' button and click that
    # after waiting time, search for the text "more info", make sure we have it first:
    browser.is_element_present_by_text('more info', wait_time=1)
    # find the link associated with the text:
    more_info_elem = browser.find_link_by_partial_text('more info')
    # click the link:
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        #  use all 3 tags: <figure /> (class lede) --> <a /> --> <img />
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

### Collect table data: Mars Fact

def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        # specifying an index of 0, we’re telling Pandas to pull only the first table it encounters
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())