import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_page_data(driver):
    """
    Scrapes all team cards. It now scrolls each individual card into view before
    extracting its text to ensure all data is captured, even for cards
    that are initially off-screen ("below the fold").
    """
    teams_on_page = []
    try:
        parent_container_locator = (By.CSS_SELECTOR, "div.grid.gap-6")
        child_card_locator = (By.CSS_SELECTOR, "div.card-hover")
        wait = WebDriverWait(driver, 20)

        print("Waiting for main content container...")
        parent_container = wait.until(EC.presence_of_element_located(parent_container_locator))
        
        print("Scrolling container into view...")
        driver.execute_script("arguments[0].scrollIntoView(true);", parent_container)
        time.sleep(0.5)

        print("Explicitly waiting for child cards to become VISIBLE...")
        wait.until(EC.visibility_of_element_located(child_card_locator))
        time.sleep(1)
        
        team_cards = driver.find_elements(*child_card_locator)
        print(f"Found {len(team_cards)} team cards. Iterating and scraping each one...")

        # === THE CRITICAL FIX FOR MISSING ROWS ===
        for i, card in enumerate(team_cards):
            try:
                # 1. Scroll the specific card we're about to process into the middle of the screen.
                # This ensures it is fully visible before we try to get its text content.
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", card)
                time.sleep(0.2) # A tiny pause to let the browser settle after scrolling.

                # 2. Now that the card is visible, extract its data.
                team_id = card.find_element(By.XPATH, ".//span[contains(text(), 'Team ID:')]/following-sibling::span").text
                team_name = card.find_element(By.TAG_NAME, "h3").text
                university_name = card.find_element(By.TAG_NAME, "p").text
                coach = card.find_element(By.XPATH, ".//span[contains(text(), 'Coach:')]/following-sibling::span").text
                status = card.find_element(By.XPATH, ".//span[contains(text(), 'ICPC Status:')]/following-sibling::span").text
                
                # Check for empty text which can indicate a scraping issue
                if not team_id or not team_name:
                    print(f"Warning: Scraped empty data for card #{i+1}, retrying scroll.")
                    time.sleep(0.5)
                    # You could add retry logic here if needed, but the scroll usually solves it.
                    continue

                team_info = {
                    "Team Name": team_name, "University": university_name, "Team ID": team_id,
                    "Coach": coach, "ICPC Status": status
                }
                teams_on_page.append(team_info)
            except NoSuchElementException:
                print(f"Warning: Could not find all expected elements in card #{i+1}. Skipping.")
                continue
    
    except TimeoutException:
        print("Timed out during the waiting process. Assuming this is an empty page.")

    return teams_on_page


def scrape_icpc_teams_by_url_pagination():
    base_url = "https://icpc.bubt.edu.bd/teams.php?category=all&search="
    driver = webdriver.Chrome()
    driver.maximize_window()
    all_teams_data = []
    seen_team_ids = set()
    page_number = 1

    try:
        while True:
            current_url = f"{base_url}&page={page_number}"
            print(f"\n--- Scraping Page {page_number} ---")
            driver.get(current_url)
            page_data = scrape_page_data(driver)
            
            if not page_data:
                print("No data found on page. Reached the end of the results.")
                break 
            
            first_team_id_on_page = page_data[0]['Team ID']
            if first_team_id_on_page in seen_team_ids:
                print(f"Detected duplicate team ID ({first_team_id_on_page}). Stopping scrape.")
                break

            all_teams_data.extend(page_data)
            for team in page_data:
                seen_team_ids.add(team['Team ID'])
            
            page_number += 1
            time.sleep(1) 

    finally:
        print("\nClosing the browser.")
        driver.quit()

    if not all_teams_data:
        print("No data was scraped in total. CSV file will not be created.")
        return

    csv_file_name = "icpc_teams_all_complete.csv"
    csv_headers = ["Team Name", "University", "Team ID", "Coach", "ICPC Status"]
    
    try:
        print(f"\nWriting {len(all_teams_data)} total entries to {csv_file_name}...")
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(all_teams_data)
        print(f"Successfully saved all data to {csv_file_name}")
    except IOError:
        print(f"Error: Could not write to the file {csv_file_name}.")

if __name__ == "__main__":
    scrape_icpc_teams_by_url_pagination()