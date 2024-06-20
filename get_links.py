import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://www.hope1842.com/'

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request to the webpage with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <a> tags (which define hyperlinks)
    links = soup.find_all('a')

    # Open a file to write the links to
    with open('links.txt', 'w') as file:
        for link in links:
            href = link.get('href')
            if href:  # Check if the href attribute exists
                file.write(href + '\n')

    print("Links have been successfully extracted and written to 'links.txt'")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
