from playwright.sync_api import sync_playwright
import time

def extract_links(url):
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Retry mechanism for navigating to the URL
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Opening the webpage... Attempt {attempt + 1}")
                page.goto(url, wait_until="load", timeout=60000)  # Wait for the page to load fully
                print("Page loaded successfully.")
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(5)
                else:
                    print("Max retries reached. Exiting.")
                    browser.close()
                    return
        
        # Print the page title to confirm that the page has loaded
        try:
            print("Page title:", page.title())
        except Exception as e:
            print(f"Failed to retrieve the page title: {e}")

        # Print the HTML content to verify rendering
        try:
            print("Rendered HTML content:")
            content = page.content()
            print(content[:1000])  # Print first 1000 characters for brevity
        except Exception as e:
            print(f"Failed to retrieve page content: {e}")

        # Find all <a> tags (which define hyperlinks)
        try:
            links = page.query_selector_all("a")
        except Exception as e:
            print(f"Failed to find links on the page: {e}")
            browser.close()
            return

        # Print out the links found
        print("Found links:")
        for link in links:
            try:
                href = link.get_attribute("href")
                if href:
                    print(href)
            except Exception as e:
                print(f"Failed to get href attribute from a link: {e}")

        # Open a file to write the links to
        try:
            with open("links.txt", "w") as file:
                for link in links:
                    href = link.get_attribute("href")
                    if href:  # Check if the href attribute exists
                        file.write(href + "\n")
            print("Links have been successfully extracted and written to 'links.txt'")
        except Exception as e:
            print(f"Failed to write links to file: {e}")

        # Close the browser
        browser.close()

# URL of the webpage to scrape
url = "https://www.hope1842.com/"

# Extract links from the webpage
extract_links(url)