# Web Scraping Task — CodeAlpha Internship
# Scrape book data from http://books.toscrape.com/

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL of the site
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

# List to store scraped data
all_books = []

# Loop through first 5 pages (can be changed)
for page in range(1, 6):
    url = base_url.format(page)
    print(f"Scraping page {page}: {url}")
    
    # Send HTTP request to the page
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve page:", page)
        continue

    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all book containers
    books = soup.find_all('article', class_='product_pod')
    
    # Extract details from each book
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text.strip()[2:]  # Remove '£'
        rating = book.p['class'][1]  # Rating is in class name, e.g., "star-rating Three"
        
        # Append data as a dictionary
        all_books.append({
            'Title': title,
            'Price (£)': float(price),
            'Rating': rating
        })

    # Pause between requests (to avoid hammering the server)
    time.sleep(1)

# Create DataFrame from collected data
df = pd.DataFrame(all_books)

# Show sample data
print(df.head())

# Save to CSV
df.to_csv("CodeAlpha_WebScraping_Books.csv", index=False)
print("\n Scraping complete! Data saved to 'CodeAlpha_WebScraping_Books.csv'")
