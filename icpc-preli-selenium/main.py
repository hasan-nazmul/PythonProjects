import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def scrape_multiple_pages(url, csv_filename):
    """
    Scrape team data from multiple pages until the next button is disabled
    """
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    
    # Set implicit wait
    driver.implicitly_wait(10)

    try:
        # Navigate to the webpage
        print(f"Navigating to: {url}")
        driver.get(url)
        
        all_team_data = []
        page_number = 1
        
        while True:
            print(f"\n=== Scraping Page {page_number} ===")
            
            # Wait explicitly for tbody to be present
            wait = WebDriverWait(driver, 15)
            tbody = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
            
            # Get all tr elements within tbody
            tr_elements = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            print(f"Found {len(tr_elements)} team rows on page {page_number}")
            
            # Process each table row on current page
            page_data = process_page_data(tr_elements, page_number)
            all_team_data.extend(page_data)
            
            # Check if next button is disabled
            next_button = driver.find_element(By.CSS_SELECTOR, 
                'button[aria-label="Go to next page"]')
            
            if "Mui-disabled" in next_button.get_attribute("class"):
                print("Next button is disabled. Reached the last page.")
                break
            else:
                # Click next button and wait for page to load
                print("Moving to next page...")
                next_button.click()
                time.sleep(2)  # Wait for page to load
                page_number += 1
        
        # Save all data to CSV
        save_to_csv(all_team_data, csv_filename)
        print(f"\nTotal {len(all_team_data)} teams scraped from {page_number} pages")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        # Close the browser
        driver.quit()

def process_page_data(tr_elements, page_number):
    """
    Process team data from a single page
    """
    page_data = []
    
    for index, tr in enumerate(tr_elements):
        try:
            # Get all td elements in the row
            td_elements = tr.find_elements(By.TAG_NAME, "td")
            
            # Extract rank from first td
            rank = ""
            if len(td_elements) > 0:
                rank = td_elements[0].text.strip()
            
            # Extract team and university from second td
            team_name = ""
            university_name = ""
            
            if len(td_elements) > 1:
                second_td = td_elements[1]
                
                # Extract team name from strong tag
                try:
                    team_strong = second_td.find_element(By.TAG_NAME, "strong")
                    team_name = team_strong.text.strip()
                except:
                    print(f"  No strong tag found in row {index + 1} on page {page_number}")
                
                # Extract university name from div tag
                try:
                    university_div = second_td.find_element(By.TAG_NAME, "div")
                    university_name = university_div.text.strip()
                except:
                    print(f"  No div tag found in row {index + 1} on page {page_number}")
            
            # Extract solve count and penalty from third td
            solve_count = ""
            penalty = ""
            
            if len(td_elements) > 2:
                third_td = td_elements[2]
                
                # Find the main div in third td
                try:
                    main_div = third_td.find_element(By.TAG_NAME, "div")
                    
                    # Find all divs inside the main div
                    inner_divs = main_div.find_elements(By.TAG_NAME, "div")
                    
                    if len(inner_divs) >= 1:
                        # First inner div: solve count
                        solve_count = inner_divs[0].text.strip()
                    
                    if len(inner_divs) >= 2:
                        # Second inner div: penalty (remove brackets)
                        penalty_text = inner_divs[1].text.strip()
                        # Remove brackets using regex
                        penalty = re.sub(r'[\(\)\[\]]', '', penalty_text)
                        
                except Exception as e:
                    print(f"  Error extracting solve/penalty from row {index + 1} on page {page_number}: {str(e)}")
            
            # Extract other columns if they exist
            other_columns = []
            if len(td_elements) > 3:
                for td_index in range(3, len(td_elements)):
                    other_columns.append(td_elements[td_index].text.strip())
            
            # Create data row
            team_data = {
                'rank': rank,
                'team_name': team_name,
                'university': university_name,
                'solved': solve_count,
                'penalty': penalty,
                'page': page_number,
                'other_columns': other_columns
            }
            
            page_data.append(team_data)
            
            print(f"  Processed: Rank {rank} | {team_name} | Solved: {solve_count} | Penalty: {penalty}")
            
        except Exception as e:
            print(f"Error processing row {index + 1} on page {page_number}: {str(e)}")
    
    return page_data

def save_to_csv(all_team_data, csv_filename):
    """
    Save all team data to CSV file
    """
    if not all_team_data:
        print("No data to save!")
        return
    
    # Determine maximum number of other columns
    max_other_columns = max(len(team['other_columns']) for team in all_team_data)
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create headers for other columns
        other_headers = [f'Column_{i+1}' for i in range(max_other_columns)]
        
        # Write header row
        headers = ['Rank', 'Team Name', 'University', 'Solved', 'Penalty', 'Page'] + other_headers
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        
        # Write data rows
        for team in all_team_data:
            row_data = [
                team['rank'],
                team['team_name'],
                team['university'],
                team['solved'],
                team['penalty'],
                team['page']
            ]
            
            # Add other columns, pad with empty strings if needed
            other_cols = team['other_columns'] + [''] * (max_other_columns - len(team['other_columns']))
            row_data.extend(other_cols)
            
            csv_writer.writerow(row_data)
    
    print(f"All data successfully saved to {csv_filename}")

# Alternative version with explicit page navigation
def scrape_with_page_numbers(url, csv_filename):
    """
    Version that shows current page number during scraping
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    try:
        driver.get(url)
        all_team_data = []
        page_number = 1
        
        while True:
            print(f"\n=== Scraping Page {page_number} ===")
            
            # Wait for table to load
            wait = WebDriverWait(driver, 15)
            tbody = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
            
            # Get current page number from pagination (if available)
            try:
                current_page_element = driver.find_element(By.CSS_SELECTOR, 
                    '.MuiPaginationItem-page.Mui-selected')
                current_page = current_page_element.text
                print(f"Current page according to pagination: {current_page}")
            except:
                print(f"Scraping page {page_number}")
            
            # Scrape current page
            tr_elements = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            page_data = process_page_data(tr_elements, page_number)
            all_team_data.extend(page_data)
            
            # Check next button
            next_button = driver.find_element(By.CSS_SELECTOR, 
                'button[aria-label="Go to next page"]')
            
            if "Mui-disabled" in next_button.get_attribute("class"):
                print("Reached the last page!")
                break
            
            # Click next button
            print("Clicking next button...")
            next_button.click()
            
            # Wait for page to load
            time.sleep(3)
            page_number += 1
        
        # Save data
        save_to_csv(all_team_data, csv_filename)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

# Robust version with better error handling
def scrape_robust_multiple_pages(url, csv_filename):
    """
    More robust version with better error handling and retry mechanism
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)

    try:
        driver.get(url)
        all_team_data = []
        page_number = 1
        max_retries = 3
        
        while True:
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    print(f"\n=== Scraping Page {page_number} (Attempt {retry_count + 1}) ===")
                    
                    # Wait for page to load completely
                    wait = WebDriverWait(driver, 20)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
                    
                    # Scrape current page
                    tr_elements = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
                    if tr_elements:
                        page_data = process_page_data(tr_elements, page_number)
                        all_team_data.extend(page_data)
                        success = True
                        print(f"Successfully scraped page {page_number}")
                    else:
                        print(f"No data found on page {page_number}")
                        retry_count += 1
                        time.sleep(2)
                        
                except Exception as e:
                    print(f"Error scraping page {page_number}: {str(e)}")
                    retry_count += 1
                    time.sleep(2)
            
            if not success:
                print(f"Failed to scrape page {page_number} after {max_retries} attempts")
                break
            
            # Check if next button is disabled
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 
                    'button[aria-label="Go to next page"]')
                
                if "Mui-disabled" in next_button.get_attribute("class"):
                    print("Next button is disabled. Reached the last page.")
                    break
                else:
                    # Click next button
                    print("Moving to next page...")
                    next_button.click()
                    time.sleep(3)  # Wait for page load
                    page_number += 1
                    
            except Exception as e:
                print(f"Error navigating to next page: {str(e)}")
                break
        
        # Save all data
        save_to_csv(all_team_data, csv_filename)
        print(f"\nScraping completed! Total: {len(all_team_data)} teams from {page_number} pages")
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    # Replace with your target URL
    target_url = "https://bapsoj.org/contests/icpc-preliminary-dhaka-site-2024/standings"
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Choose the function you want to use:
    
    # Option 1: Basic multi-page scraping
    csv_filename = f"standings_multiple_pages_{timestamp}.csv"
    scrape_multiple_pages(target_url, csv_filename)
    
    # Option 2: Version with page numbers
    # csv_filename = f"standings_with_pages_{timestamp}.csv"
    # scrape_with_page_numbers(target_url, csv_filename)
    
    # Option 3: Robust version with retries
    # csv_filename = f"standings_robust_{timestamp}.csv"
    # scrape_robust_multiple_pages(target_url, csv_filename)