from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import nltk
nltk.download('punkt')

import numpy as np

from bs4 import BeautifulSoup
import urllib.request

import json
import requests

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
  site = 'https://us-central1-fake-news-ai.cloudfunctions.net/detect/'
  payload = {'url': url}
  headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5',
              'Connection': 'keep-alive', 'Content-Length': '103', 'Content-type': 'application/json; charset=utf-8',
              'DNT': '1', 'Host': 'us-central1-fake-news-ai.cloudfunctions.net', 'Origin': 'http://www.fakenewsai.com',
              'Referer': 'http://www.fakenewsai.com/', 'TE': 'Trailers',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
  response_json = requests.post(site, data=json.dumps(payload), headers=headers).text
  response = json.loads(response_json)
  is_fake = int(response['fake'])
  if is_fake == 0:
    return 'Real'
  elif is_fake == 1:
    return 'Fake'
  else:
    return 'N/A'

if __name__ == "__main__":
  serve(app, host = '0.0.0.0', port = 8080)