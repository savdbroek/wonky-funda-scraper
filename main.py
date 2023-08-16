import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import os

# Constants
URL = "YOUR_FUNDA_SEARCH_URL"
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
DISCORD_ID = "YOUR_DISCORD_ID"
JSON_FILE = "links.json"

# Set up Chrome options
chrome_options = Options()

# Set the window position off-screen
chrome_options.add_argument("--window-position=-3200,-3200")

# Initialize Chrome driver with the options
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the URL
driver.get(URL)

# Extract all listings
listings = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="search-result-item"]')

new_links = []

for listing in listings:
    link = listing.find_element(By.CSS_SELECTOR, 'a[data-test-id="object-image-link"]').get_attribute('href')
    if link not in new_links:
        new_links.append(link)

# Load existing links from the JSON file
try:
    # Check if the file is empty
    if os.path.getsize(JSON_FILE) == 0:
        existing_links = []
    else:
        with open(JSON_FILE, 'r') as file:
            existing_links = json.load(file)
except FileNotFoundError:
    existing_links = []

# Filter out the links that are already in the JSON file
new_links = [link for link in new_links if link not in existing_links]

for link in new_links:
    listing = driver.find_element(By.CSS_SELECTOR, f'a[href="{link}"]').find_element(By.XPATH, "./..")
    image_url = listing.find_element(By.CSS_SELECTOR, 'img').get_attribute('srcset').split(' ')[0]
    street_name = listing.find_element(By.CSS_SELECTOR, 'h2[data-test-id="street-name-house-number"]').text
    postal_city = listing.find_element(By.CSS_SELECTOR, 'div[data-test-id="postal-code-city"]').text
    price = listing.find_element(By.CSS_SELECTOR, 'p[data-test-id="price-sale"]').text
    details = listing.find_elements(By.CSS_SELECTOR, 'ul > li')
    
    # Adjusting for the presence of specific keywords
    first_detail = details[0].text
    if first_detail == "Nieuw":
        living_space = details[1].text
        property_space = details[2].text
        bedrooms = details[3].text
        energy_label = details[4].text.strip()
    elif first_detail == "Blikvanger" and details[1].text == "Nieuw":
        living_space = details[2].text
        property_space = details[3].text
        bedrooms = details[4].text
        energy_label = details[5].text.strip()
    elif first_detail == "Verkocht onder voorbehoud":
        living_space = details[1].text
        property_space = details[2].text
        bedrooms = details[3].text
        energy_label = details[4].text.strip()
    else:
        living_space = details[0].text
        property_space = details[1].text
        bedrooms = details[2].text
        energy_label = details[3].text.strip()

    embed = {
        "title": street_name,
        "url": link,
        "description": f"**{price}**\n\n{postal_city}\n🏠: {living_space}\n🏡: {property_space}\n🛏️: {bedrooms}\n⚡: {energy_label}",
        "color": 16753920, # This sets the embed color to orange
        "image": {"url": image_url}
    }

    # Send the message to Discord with user tags in the content field
    requests.post(WEBHOOK_URL, json={"content": f"{DISCORD_ID}", "embeds": [embed]})

driver.quit()

# Update the JSON file with the new links
with open(JSON_FILE, 'w') as file:
    json.dump(existing_links + new_links, file)

print(f"Found {len(new_links)} new links.")
