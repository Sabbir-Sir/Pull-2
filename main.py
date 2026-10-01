import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

header = {"User-Agent": "Mozilla/5.0"}

url = "https://quotes.toscrape.com/page/10/"
#start from page 10 so the scraper works backwards.

all_quotes = []

while url:
    print(f"Scraping: {url}")
    #displays the current page being scraped, making it easier to track progress.

    response = requests.get(url, headers=header, timeout=10)
    #added a timeout so the program doesn't wait forever for a response.

    if response.status_code != 200:
        print("Page not found!")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")
    #finds all quote containers on each page so every quote is collected.

    for quote in quotes:
        quote_tag = quote.find("span", class_="text")

        if quote_tag:
            quote_text = quote_tag.get_text(strip=True)
        else:
            quote_text = "N/A"

        author_tag = quote.find("small", class_="author")

        if author_tag:
            author = author_tag.get_text(strip=True)
        else:
            author = "N/A"

        all_quotes.append({
            "Quote": quote_text,
            "Author": author
        })

    previous = soup.find("li", class_="previous")

    if previous:
        previous_link = previous.find("a")["href"]
        url = urljoin(url, previous_link)
    else:
        url = None

df = pd.DataFrame(all_quotes, columns=["Quote", "Author"])

print(f"Total Quotes Scraped: {len(df)}")

df.to_csv("Reverse_Pagination_Quotes.csv", index=False)
#daves the scraped quotes into a CSV file without adding DataFrame index numbers.
