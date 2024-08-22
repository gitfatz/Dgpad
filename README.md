This script provides a tool to scrape articles from a sitemap, process them into structured data, and save them as JSON files. It leverages Python's dataclasses, BeautifulSoup, and requests libraries to achieve this.

Overview
The script performs the following steps:

Fetch Data: Downloads the content from a given URL.
Parse Sitemaps: Extracts sitemap URLs from an index sitemap.
Extract Article URLs: Retrieves article URLs from each sitemap.
Scrape Articles: Fetches and parses individual articles, extracting metadata and content.
Save Articles: Saves the collected article data into JSON files, organized by month and year.
Requirements
Python 3.x
Libraries: dataclasses, requests, beautifulsoup4, lxml
You can install the required libraries using pip:

bash
Copy code
pip install requests beautifulsoup4 lxml
Code Breakdown
Data Models
Article: A dataclass that represents an article with various metadata fields such as url, title, keywords, and full_text.
Functions
fetch_data(url): Fetches the content from the provided URL and returns it as text. Raises an exception if the request fails.

save_articles(articles_list): Saves a list of Article instances to a JSON file. The file is named based on the publication date of the articles.

Classes
SitemapParser: Parses sitemaps to get URLs for monthly sitemaps and individual articles.

get_monthly_sitemap_urls(): Retrieves URLs of monthly sitemaps from the index sitemap.
get_article_urls(sitemap_url): Extracts article URLs from a given sitemap.
ArticleScraper: Scrapes and processes individual articles.

scrape_article(article_url): Fetches and parses an article's content and metadata from the given URL.
Main Execution
main(): Coordinates the scraping process:
Initializes the SitemapParser and retrieves monthly sitemap URLs.
For each sitemap, retrieves article URLs and scrapes the articles.
Saves the scraped articles to JSON files.
Usage
To run the script, simply execute it using Python:

bash
Copy code
python script_name.py
Replace script_name.py with the name of the file containing the script.

Notes
Ensure that the index_url in SitemapParser is correctly set to the sitemap index you want to scrape.
The script assumes a certain structure in the article metadata and HTML. Adjustments may be needed for different sites or formats.
The script currently fetches up to 10,000 articles. Modify the max_articles variable in the main() function if needed.
Error Handling
The script includes basic error handling for network issues and parsing errors. If an error occurs during data fetching or parsing, it will be printed to the console, and processing will continue with the next item.

Contributing
Contributions and improvements are welcome! Feel free to submit issues or pull requests to enhance the script's functionality or adapt it to different use cases.
