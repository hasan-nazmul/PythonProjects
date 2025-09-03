from bs4 import BeautifulSoup
import requests

with open('index.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

for article in soup.find_all('article', class_='book'):
    print(article.h3.text)
