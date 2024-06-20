from playwright.sync_api import sync_playwright
import time
import csv
from urllib.parse import urljoin

def extract_links(url):
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        
        # Create a new page with a specific user agent
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        # Retry mechanism for navigating to the URL
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Opening the webpage... Attempt {attempt + 1}")
                page.goto(url, wait_until="domcontentloaded", timeout=60000)  # Wait for the page to load fully
                
                # Wait for an element that is only present on the actual page
                page.wait_for_selector("a", timeout=60000)
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

        # Find all <a> tags (which define hyperlinks) on the main page
        try:
            main_links = page.query_selector_all("a")
        except Exception as e:
            print(f"Failed to find links on the main page: {e}")
            browser.close()
            return

        # Extract href attributes from the main page links
        main_page_links = []
        for link in main_links:
            href = link.get_attribute("href")
            if href and not href.startswith('#'):  # Filter out invalid URLs
                full_url = urljoin(url, href)  # Resolve relative URLs
                main_page_links.append(full_url)

        print(f"Found {len(main_page_links)} links on the main page.")

        # Open a CSV file to write the links to
        with open("links.csv", "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Original Link", "Child Links"])

            # Visit each link found on the main page and extract additional links
            for main_link in main_page_links:
                child_links = set()  # Use a set to avoid duplicates
                try:
                    print(f"Processing link: {main_link}")
                    page.goto(main_link, wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_selector("a", timeout=60000)

                    # Find all <a> tags on the child page
                    child_page_links = page.query_selector_all("a")
                    for link in child_page_links:
                        href = link.get_attribute("href")
                        if href and not href.startswith('#') and href not in main_page_links:  # Avoid duplicates and invalid URLs
                            full_url = urljoin(main_link, href)  # Resolve relative URLs
                            child_links.add(full_url)

                    # Write the original link and its child links to the CSV file
                    csvwriter.writerow([main_link, "; ".join(child_links)])
                    print(f"Child links for {main_link}: {len(child_links)} found.")

                except Exception as e:
                    print(f"Failed to process link {main_link}: {e}")

        print("Links have been successfully extracted and written to 'links.csv'")

        # Close the browser
        browser.close()

# URL of the webpage to scrape
url = "https://www.hope1842.com/"

# Extract links from the webpage
extract_links(url)
