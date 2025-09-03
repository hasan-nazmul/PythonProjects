from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get('https://www.rokomari.com/book/author/8822/')
driver.implicitly_wait(5)

book_hrefs = driver.find_elements(By.CSS_SELECTOR, 'img[src$=".png"]')

for links in book_hrefs:
    print(links.get_attribute('alt'))

time.sleep(10)
driver.quit()