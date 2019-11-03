# import urllib
# import urllib2

# url =  "https://www.nytimes.com/2019/11/02/opinion/sunday/instagram-social-media.html"
# data = {
#         "url" : url 
#        }

# encoded_data = urllib.urlencode(data)
# content = urllib2.urlopen("http://www.fakenewsai.com",
#         encoded_data)
# print content.readlines()

# import mechanize
# br = mechanize.Browser()
# br.open("http://www.fakenewsai.com")
# br.select_form(nr=0)
# br.form['url'] = 'https://www.nytimes.com/2019/11/02/opinion/sunday/instagram-social-media.html'
# req = br.submit()
# print(req.read())

# from selenium.webdriver.support.ui import Select
# from selenium import webdriver
# driver = webdriver.Chrome()
# element = driver.find_element_by_id("url")
# element.send_keys("https://www.nytimes.com/2019/11/02/opinion/sunday/instagram-social-media.html")
# driver.find_element_by_id("submit").click()

# import requests
# import time
# url = "http://www.fakenewsai.com"
# payload = {'url':'https://www.nytimes.com/2019/11/02/opinion/sunday/instagram-social-media.html'}
# r = requests.get(url, params=payload)
# with open("requests_results.html", "wb") as f:
#     f.write(r.content)

# import requests
# from bs4 import BeautifulSoup

# data = {
#     'url': 'https://www.nytimes.com/2019/11/02/opinion/sunday/instagram-social-media.html'
# }

# url = "http://www.fakenewsai.com"
# url = "https://us-central1-fake-news-ai.cloudfunctions.net/detect"
# response = requests.post(url, data=data)
# doc = BeautifulSoup(response.text, 'html.parser')

# # Grab all of the rows
# h2_tags = doc.find_all('h2')

# # Let's print the first 5
# for h2_tag in h2_tags:
#     print(h2_tag.text.strip())

# print(doc.text)

from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://www.fakenewsai.com')
element = browser.find_element_by_id("url")
element.send_keys("https://www.nytimes.com/2019/11/02/opinion/sunday/instagram-social-media.html")
button = browser.find_element_by_id("submit")
button.click()
