from bs4 import BeautifulSoup
import requests

url = 'https://www.rokomari.com/search?term=saimum+series&search_type=ALL&page=1'

source = requests.get(url).text

soup = BeautifulSoup(source, 'lxml')

for item in soup.find_all('div', class_='book-img'):
    print(item.img['alt'])
