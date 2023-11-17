"""Download metadata from the target site"""
import os
import re

import requests
from requests.exceptions import RequestException

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Define a dictionary to store name replacements
name_replacements = {
    'oma': 'Omaha',
    'baltimore-md': 'Baltimore',
    'western-ny': 'Western New York',
    'kansas-city': 'Kansas City',
    'las-vegas': 'Las Vegas',
    'los-angeles': 'Los Angeles',
    'new-england': 'New England',
    'new-orleans': 'New Orleans',
    'san-antonio': 'San Antonio',
    'san-deigo': 'San Diego',
    'san-francisco': 'San Francisco',
    'south-africa': 'South Africa',
    'st-louis': 'St. Louis',
    'hampton-roads': 'Hampton Roads',
    'washington-dc': 'Washington DC',
    'west-virginia': 'West Virginia'
}

# Define a dictionary to store link-to-text replacements
link_replacements = {
    'https://www.linkedin.com/groups/12489570/': 'Raleigh/Durham',
    'http://bitpdx.org/': 'Portland',
    'https://bit-twincities.org/': 'Twin Cities',
}

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# Load the webpage
driver.get("https://foundation.blacksintechnology.net/chapters/")

# Wait for the page to load (you may need to adjust the wait time)
driver.implicitly_wait(10)  # Wait for up to 10 seconds for the page to load

print(f"# {driver.title}")

# Create a dictionary to store unique links and their corresponding anchor text
unique_links = {}

# Find all anchor elements on the page
anchor_elements = driver.find_elements(By.TAG_NAME, "a")

for element in anchor_elements:
    link = element.get_attribute("href")
    text = element.text

    if link and not link.startswith("mailto:") and text == "Chapter Page":
        # Define a regular expression pattern to match "bit-" or "blacks-in-technology-" followed by a name
        pattern = re.compile(r'(bit|blacks-in-technology|blacksintech)-?([^/]+)')
        match = pattern.search(link)
        if match:
            # If the pattern is matched, replace "Chapter Page" with the matched name
            name = match.group(2)

            # Check if the name is in the dictionary and replace it if necessary
            if name in name_replacements:
                name = name_replacements[name]

            text = text.replace("Chapter Page", name.title())

        # If the pattern is not matched, replace "Chapter Page" with something else
        else:

            # If the pattern is not matched, check if there's a link replacement in the dictionary
            if link in link_replacements:
                text = link_replacements[link]
            else:
                # If no replacement is found, replace "Chapter Page" with the link itself
                text = link

        # Add the link and modified anchor text to the dictionary
        unique_links[link] = text

# Print the unique links and their corresponding anchor text
print("\n|Chapter|Link|")
print("|----|----|")
for link, text in unique_links.items():
    print(f"|[{text}]({link})|[{link}]({link})|")

# Close the browser
driver.close()
