from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import booking.constants as const
import time

def get_plus_button():
    """Robust function to find the plus button"""
    selectors = [
        "[data-testid*='plus']",
        "[aria-label*='increase']",
        "[title*='add']",
        "button:has(svg[viewBox*='24'])",  # CSS :has() if supported
        # Add more fallback selectors
    ]

    driver = webdriver.Chrome()  # or your driver of choice
    driver.get(const.BASE_URL)  # Replace with your target URL
    
    for selector in selectors:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            print(f"Found plus button with selector: {selector}")
        except:
            continue
    
    raise Exception("Plus button not found with any selector")

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
            
    def seat_booking(self, adults, children, rooms):

        try:
            selection_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[aria-label^="Number of travelers and rooms."]')
                )
            )
            selection_element.click()
        except:
            print("Exception occurred")
        adults_value_element = self.find_element(
            By.ID, 'group_adults'
        )
        adults_value = int(adults_value_element.get_attribute('value'))

        increase_adults_button = self.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]'
        )
        decrease_adults_button = self.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]'
        )

        while adults_value != adults:
            if adults_value < adults:
                increase_adults_button.click()
                adults_value += 1
            elif adults_value > adults:
                decrease_adults_button.click()
                adults_value -= 1

        # children_value_element = self.find_element(
        #     By.ID, 'group_children'
        # )
        # children_value = int(children_value_element.get_attribute('value'))

        # increase_children_button = self.find_element(
        #     By.CSS_SELECTOR, 'button[aria-label="Increase number of Children"]'
        # )
        # decrease_children_button = self.find_element(
        #     By.CSS_SELECTOR, 'button[aria-label="Decrease number of Children"]'
        # )

        # while children_value != children:
        #     if children_value < children:
        #         increase_children_button.click()
        #         children_value += 1
        #     elif children_value > children:
        #         decrease_children_button.click()
        #         children_value -= 1

        # rooms_value_element = self.find_element(
        #     By.ID, 'group_rooms'
        # )
        # rooms_value = int(rooms_value_element.get_attribute('value'))

        # increase_rooms_button = self.find_element(
        #     By.CSS_SELECTOR, 'button[aria-label="Increase number of Rooms"]'
        # )
        # decrease_rooms_button = self.find_element(
        #     By.CSS_SELECTOR, 'button[aria-label="Decrease number of Rooms"]'
        # )

        # while rooms_value != rooms:
        #     if rooms_value < rooms:
        #         increase_rooms_button.click()
        #         rooms_value += 1
        #     elif rooms_value > rooms:
        #         decrease_rooms_button.click()
        #         rooms_value -= 