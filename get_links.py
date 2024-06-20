from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")  # Set window size to ensure page elements load correctly
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL of the webpage to scrape
url = 'https://www.hope1842.com/'

# Open the webpage
print("Opening the webpage...")
try:
    driver.get(url)
except Exception as e:
    print(f"Failed to open the webpage: {e}")
    driver.quit()
    exit()

# Wait for the initial page to load and pass the bot protection
try:
    # Wait for the page to show a title other than "Just a moment..."
    print("Waiting for page to load...")
    WebDriverWait(driver, 60).until_not(EC.title_contains("Just a moment..."))
    
    # Additional wait to ensure all dynamic content loads
    print("Waiting for dynamic content to load...")
    time.sleep(10)  # Add a fixed wait time to ensure page loads fully

    print("Page loaded successfully.")
except Exception as e:
    print(f"An error occurred while loading the page: {e}")
    driver.quit()
    exit()

# Print the page title to confirm that the page has loaded
try:
    print("Page title:", driver.title)
except Exception as e:
    print(f"Failed to retrieve the page title: {e}")

# Find all <a> tags (which define hyperlinks)
try:
    links = driver.find_elements(By.TAG_NAME, 'a')
except Exception as e:
    print(f"Failed to find links on the page: {e}")
    driver.quit()
    exit()

# Print out the links found
print("Found links:")
for link in links:
    try:
        href = link.get_attribute('href')
        print(href)
    except Exception as e:
        print(f"Failed to get href attribute from a link: {e}")

# Open a file to write the links to
try:
    with open('links.txt', 'w') as file:
        for link in links:
            href = link.get_attribute('href')
            if href:  # Check if the href attribute exists
                file.write(href + '\n')
    print("Links have been successfully extracted and written to 'links.txt'")
except Exception as e:
    print(f"Failed to write links to file: {e}")

# Close the browser
driver.quit()

