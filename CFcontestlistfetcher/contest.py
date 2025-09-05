from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
url = 'https://codeforces.com/contests'

driver.get(url)

contest_titles = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located(
        (By.XPATH, "//tr[@data-contestid]//td")
    )
)

for contest_title in contest_titles:
    print(contest_title.text)