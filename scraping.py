from bs4 import BeautifulSoup
import requests

html_oxford = 'http://www.facebook.com'
html_python = 'https://www.python.org'


html = requests.get(html_oxford)

soup = BeautifulSoup(html.text, features="html.parser")
titles = soup.find_all('title')
print(titles)
print(titles[0].text)

divs = soup.find_all('div')#, {'class': '_50f4 _50f7'})
print(divs)
print(divs[0].text)
