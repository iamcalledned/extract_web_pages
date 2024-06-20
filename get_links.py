from playwright.sync_api import sync_playwright

def extract_links(url):
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Go to the webpage
        print("Opening the webpage...")
        page.goto(url)

        # Wait for the page to load and the necessary elements to appear
        print("Waiting for the page to load...")
        page.wait_for_timeout(10000)  # Wait for 10 seconds for the page to fully load
        
        # Print the page title to confirm that the page has loaded
        print("Page title:", page.title())

        # Find all <a> tags (which define hyperlinks)
        links = page.query_selector_all("a")

        # Print out the links found
        print("Found links:")
        for link in links:
            href = link.get_attribute("href")
            print(href)

        # Open a file to write the links to
        with open("links.txt", "w") as file:
            for link in links:
                href = link.get_attribute("href")
                if href:  # Check if the href attribute exists
                    file.write(href + "\n")

        # Close the browser
        browser.close()

    print("Links have been successfully extracted and written to 'links.txt'")

# URL of the webpage to scrape
url = "https://www.hope1842.com/"

# Extract links from the webpage
extract_links(url)

