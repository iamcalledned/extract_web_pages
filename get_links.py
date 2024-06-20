from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL of the webpage to scrape
url = 'https://www.hope1842.com/'

# Open the webpage
driver.get(url)

# Print the page title to confirm that the page has loaded
print("Page title:", driver.title)

# Find all <a> tags (which define hyperlinks)
links = driver.find_elements(By.TAG_NAME, 'a')

# Print out the links found
print("Found links:")
for link in links:
    href = link.get_attribute('href')
    print(href)

# Open a file to write the links to
with open('links.txt', 'w') as file:
    for link in links:
        href = link.get_attribute('href')
        if href:  # Check if the href attribute exists
            file.write(href + '\n')

# Close the browser
driver.quit()

print("Links have been successfully extracted and written to 'links.txt'")
