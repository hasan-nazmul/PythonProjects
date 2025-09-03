from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import booking.constants as const
import time

class Booking(webdriver.Chrome):
    def __init__(self):
        super().__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def land_first_page(self):
        self.implicitly_wait(10)
        self.get(const.BASE_URL)

    def change_currency(self, currency):
        try:
            currency_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
                )
            )
        except:
            currency_element = self.find_element(
                By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'
            )
        currency_element.click()

        try:
            selected_currency_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//*[text()='{currency}']"))
            )
        except:
            selected_currency_element = self.find_element(
                By.XPATH, f"//*[text()='{currency}']"
            )
        
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):

        try:
            search_field = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.NAME, 'ss'))
            )
        except:
            search_field = self.find_element(By.NAME, 'ss')
        search_field.clear()
        search_field.send_keys(place_to_go)
        time.sleep(2)
        try:
            first_result = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]'))
            )
        except:
            first_result = self.find_element(By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]')
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        while True:
            try:
                check_in_element = self.find_element(
                    By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]'
                )
                check_in_element.click()
            except:
                next_month_button = self.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Next month"]'
                )
                next_month_button.click()
            else:
                break

        while True:
            try:
                check_out_element = self.find_element(
                    By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]'
                )
                check_out_element.click()
            except:
                next_month_button = self.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Next month"]'
                )
                next_month_button.click()
            else:
                break
            