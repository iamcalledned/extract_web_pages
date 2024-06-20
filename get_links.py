from requests_html import HTMLSession

# URL of the webpage to scrape
url = 'https://www.hope1842.com/'

# Create an HTML Session
session = HTMLSession()

# Use the session to get the page
response = session.get(url)

# Render the JavaScript
response.html.render(timeout=30)

# Find all <a> tags (which define hyperlinks)
links = response.html.find('a')

# Print out the links found
print("Found links:")
for link in links:
    href = link.attrs.get('href')
    print(href)

# Open a file to write the links to
with open('links.txt', 'w') as file:
    for link in links:
        href = link.attrs.get('href')
        if href:  # Check if the href attribute exists
            file.write(href + '\n')

print("Links have been successfully extracted and written to 'links.txt'")
