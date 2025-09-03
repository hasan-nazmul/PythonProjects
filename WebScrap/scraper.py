import requests
import os
import re
import json

# The base URL for the page we want to scrape
BASE_URL = "https://baatighar.com/shop/publisher/sheba-prokashani-1303/page/1"
# Directory to store the downloaded images
IMAGE_DIR = "book_covers"


def sanitize_filename(name):
    """
    Removes characters from a string that are invalid for filenames.
    """
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace(" ", "_")
    return name


def download_image(url, file_path):
    """
    Downloads an image from a URL and saves it to a specified path.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded: {os.path.basename(file_path)}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")


def fetch_book_data_from_remix_api(page_url):
    """
    Fetches book data from the website's Remix.js data-loading endpoint.
    This is achieved by appending a specific query parameter to the URL.
    """
    # --- THIS IS THE FINAL, CRITICAL CHANGE ---
    # Modern frameworks like Remix use special query parameters to fetch data.
    # By adding '?_data=...', we are asking the server for the JSON data for this page.
    api_url = f"{page_url}?_data=routes%2Fshop.publisher.%24slug"
    print(f"Attempting to fetch data from the true API endpoint: {api_url}")

    # We still include the headers the browser sends for this request.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        # We make the request to the modified API URL.
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        # The server will now respond with the correct JSON.
        data = response.json()

        books_data = []
        # The path to the product list within the JSON is 'products' -> 'data'
        product_list = data.get('products', {}).get('data', [])

        if not product_list:
            print("Could not find product list in the API response. The API structure might have changed.")
            return []

        for item in product_list:
            title = item.get('name')
            image_url = item.get('image_src')

            if title and image_url:
                books_data.append({'title': title, 'image_url': image_url})

        return books_data

    except requests.exceptions.RequestException as e:
        print(f"An HTTP error occurred: {e}")
        return []
    except json.JSONDecodeError:
        print("Failed to parse JSON from the API response. This is unexpected.")
        return []


if __name__ == '__main__':
    os.makedirs(IMAGE_DIR, exist_ok=True)

    # Use the new, correct API function
    books = fetch_book_data_from_remix_api(BASE_URL)

    if books:
        print(f"\n--- Found {len(books)} Books from API ---")
        for i, book in enumerate(books, 1):
            print(f"{i}. Title: {book['title']}")

            sanitized_title = sanitize_filename(book['title'])
            file_extension = os.path.splitext(book['image_url'])[1] or ".jpg"

            filename = f"{sanitized_title}{file_extension}"
            file_path = os.path.join(IMAGE_DIR, filename)

            print(f"   Downloading image from: {book['image_url']}")
            download_image(book['image_url'], file_path)
    else:
        print("No book data was fetched from the API.")