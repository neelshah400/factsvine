from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

# import nltk
# nltk.download("punkt")

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import numpy as np
# import networkx as nx

# import pandas as pd

from selenium import webdriver
import time

import warnings
warnings.filterwarnings('ignore')

from bs4 import BeautifulSoup
import urllib.request

from flask import Flask, request, render_template
import time

from waitress import serve

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route('/act', methods=['POST'])
def act():
  projectpath = request.form['url']
  return render_template("home.html", url=projectpath, headline=scrape_headline(projectpath), summary = summarize(projectpath), status = fakeNews(projectpath))

@app.route("/feed")
def feed():
  headlines = list()
  summaries = list()
  statuses = list()
  # urls = list()
  # urls.append("https://www.cnn.com/2019/11/02/sport/breeders-cup-horse-racing-winning-post-saturday-spt-intl/index.html")
  # urls.append("https://www.nytimes.com/interactive/2019/11/02/us/politics/trump-twitter-presidency.html?action=click&module=Top%20Stories&pgtype=Homepage")
  # urls.append("https://www.nytimes.com/2019/11/02/sports/trump-ufc-244-nyc.html?action=click&module=Top%20Stories&pgtype=Homepage")
  # urls.append("https://www.cnn.com/2019/11/02/americas/niagara-falls-weather-iron-scow-trnd/index.html")
  # urls.append("https://www.nytimes.com/interactive/2019/11/02/us/politics/trump-twitter-disinformation.html")
  urls = scrape_google("https://news.google.com/news/rss")
  for i in range(0, len(urls)):
    headlines.append(scrape_headline(urls[i]))
    summaries.append(summarize(urls[i]))
    statuses.append(fakeNews(urls[i]))
  return render_template("feed.html", urls = urls, headlines=headlines, summaries=summaries, statuses=statuses)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/contact")
def contact():
  return render_template("contact.html")

def scrape_headline(url):
  page = urllib.request.urlopen(url)
  soup = BeautifulSoup(page, 'html.parser')
  return soup.find_all('h1')[0].getText()

def scrape_article(url):
  page = urllib.request.urlopen(url)
  soup = BeautifulSoup(page, 'html.parser')
  para = soup.find_all('p')
  output = ""
  for paragraph in para:
    output += paragraph.getText()
  return output

def scrape_google(url):
  Client = urllib.request.urlopen(url)
  xml_page = Client.read()
  Client.close()
  soup_page = BeautifulSoup(xml_page,"xml")
  news_list = soup_page.findAll("item")
  links = list()
  for news in news_list:
    links.append(news.link.text)
  return links[0:20]

def summarize(url, number = 5):
  parser = HtmlParser.from_url(url, Tokenizer("english"))
  stemmer = Stemmer("english")
  summarizer = Summarizer(stemmer)
  summarizer.stop_words = get_stop_words("english")
  return " ".join(str(i) for i in summarizer(parser.document, number))

def fakeNews(url):
  if url.__contains__("https://"):
    url = url[8:-1]
  if url.__contains__("http://"):
    url = url[7:-1]
  browser = webdriver.Chrome("static/chromedriver.exe")
  browser.get("http://www.fakenewsai.com")
  element = browser.find_element_by_id("url")
  element.send_keys(url)
  button = browser.find_element_by_id("submit")
  button.click()
  time.sleep(1)
  site = "" + browser.page_source
  result = ""
  if(site[site.index("opacity: 1")-10] == "e"):
    result = "Fake News"
  else:
    result = "Real News"
  browser.quit()
  return result

if __name__ == "__main__":
  # app.jinja_env.cache = {}
  # app.run(debug=True, threaded=True)
  serve(app, host = '0.0.0.0', port = 8080)