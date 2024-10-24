from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

# Function to scrape and download the first image from DuckDuckGo for a given player
def scrape_and_download_first_image(name, photo_type, context, download_dir):
    # Build the search query from the parameters
    query = f"'{name}' '{photo_type}' '{context}'"
    
    # Set up headless ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Prepare the query string for DuckDuckGo image search
    formatted_query = '+'.join(query.split())
    driver.get(f"https://duckduckgo.com/?q={formatted_query}&iax=images&ia=images")
    
    # Wait for the image results to load and find the first image
    wait = WebDriverWait(driver, 10)
    try:
        first_image = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img.tile--img__img')))
        image_url = first_image.get_attribute('src')
        print(f"Image URL for {name}: {image_url}")
        
        # Download the image
        download_image(image_url, os.path.join(download_dir, f"{name.replace(' ', '_')}.jpg"))
    
    except Exception as e:
        print(f"Error occurred for {name}: {e}")
    finally:
        driver.quit()


def download_image(image_url, download_path):
    try:
        img_data = requests.get(image_url).content
        with open(download_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Image successfully downloaded to {download_path}")
    except Exception as e:
        print(f"Failed to download image: {e}")


# Function to process a list of players
def process_player_list(player_names, photo_type, context, download_dir):
    for name in player_names:
        scrape_and_download_first_image(name, photo_type, context, download_dir)


# Usage example
if __name__ == '__main__':
    # List of player names
    player_names = ["Daniel Jones", "Tom Brady", "Patrick Mahomes"]
    
    # Parameters for the search query
    photo_type = "headshot"
    context = "nfl"
    
    # Directory to save the images
    download_dir = os.path.join(os.getcwd(), "player_images")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Call the function to process the list of players
    process_player_list(player_names, photo_type, context, download_dir)

