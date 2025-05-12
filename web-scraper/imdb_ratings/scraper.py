import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from .models import Movie
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

logger = logging.getLogger(__name__)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

BASE_URL = 'https://www.imdb.com/search/title/?genres={genre}&start={start}&explore=title_type,genres'
MOVIE_BASE_URL = 'https://www.imdb.com/'


def fetch_page(url):
    try:
        #'https://www.imdb.com/search/title/?genres=action&start=1&explore=title_type,genres'
        # Set up Selenium WebDriver with headless mode and additional options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("start-maximized")  # Start maximized
        chrome_options.add_argument("disable-infobars")  # Disable infobars
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flags
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Set User-Agent

        driver = webdriver.Chrome(options=chrome_options)  # Ensure you have ChromeDriver installed

        
        # Update URL with query parameters
        driver.get(url)

        # Wait for the page to load fully
        time.sleep(5)

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup
    except Exception as e:
        logger.exception(f"Exception during fetch: {url}")
        return None


def parse_movies(soup, genre: str):
    try:
        parent_ul = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-e22973a9-0 khSCXM detailed-list-view ipc-metadata-list--base")

        # Find all <li> elements within the parent <ul>
        if parent_ul:
            movie_divs = parent_ul.find_all('li', class_="ipc-metadata-list-summary-item")
        else:
            movie_divs = []

        if not movie_divs:
            logger.info("No more movies found on this page.")
            return []

        for div in movie_divs:
            title = div.find("h3", class_="ipc-title__text").text.strip() if div.find("h3", class_="ipc-title__text") else ''
            title = re.sub(r'^\d+\.\s*', '', title) # Remove leading numbers and dots
            year = div.find("span", class_="sc-4b408797-8 iurwGb dli-title-metadata-item").text[0:4] if div.find("span", class_="sc-4b408797-8 iurwGb dli-title-metadata-item") else ''
            rating = div.find('span', class_='ipc-rating-star--rating').text.strip() if div.find('span', class_='ipc-rating-star--rating') else None
            summary = div.find('div', class_='ipc-html-content-inner-div').text.strip() if div.find_all('div', class_='ipc-html-content-inner-div') else ''
            movie_url = div.find('a', class_='ipc-title-link-wrapper').attrs['href'] if div.find('a', class_='ipc-title-link-wrapper') else None
            # If the movie URL exists, fetch the director and cast details
            
            if movie_url:
                directors = ''
                cast = ''
                logger.info(f"Parsing {len(movie_divs)} movies from page.")
                response = requests.get(MOVIE_BASE_URL + movie_url, headers=HEADERS)

                if response.status_code != 200:
                    logger.error(f"Failed to fetch movie page: {response.status_code}")
                else:
                    logger.info(f"Successfully fetched movie page: {response.status_code}")
                    # Parse the movie page 
                    movie_soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract director(s)
                    director_div = movie_soup.find('li', attrs={'data-testid': 'title-pc-principal-credit'})
                    directors = [a.text.strip() for a in director_div.find_all('a', class_='ipc-metadata-list-item__list-content-item')]  # Limit to top 5 directors
                    
                    # Extract cast
                    cast_div = movie_soup.find_all('li', attrs={'data-testid': 'title-pc-principal-credit'})[1]
                    cast = [a.text.strip() for a in cast_div.find_all('a', class_='ipc-metadata-list-item__list-content-item')]

            Movie.objects.update_or_create(
                title=title,
                defaults={
                    'release_year': year,
                    'imdb_rating': rating,
                    'plot_summary': summary,
                    'directors': ', '.join(directors),
                    'cast': ', '.join(cast),
                    'genre': genre,
                }
            )
    except Exception as e:
        logger.exception(f"Error parsing movie: {e}")


def scrape_movies(genre: str, max_pages: int = 5, concurrency: int = 5):
    """
    Scrape IMDb movies by genre using concurrency.
    :param genre: Genre or keyword (e.g., "comedy")
    :param max_pages: Number of result pages to scrape (each page has 50 results)
    :param concurrency: Number of threads to run concurrently
    """
    logger.info(f"Starting IMDb scrape for genre: {genre}")
    urls = [BASE_URL.format(genre=genre, start=1 + (i * 50)) for i in range(max_pages)]
    logger.info(f"Generated URLs: {urls}")

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_to_url = {executor.submit(fetch_page, url): url for url in urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                soup = future.result()
                if soup:
                    parse_movies(soup, genre)
            except Exception as e:
                logger.exception(f"Error processing URL {url}: {e}")

    logger.info(f"Scraping completed for genre: {genre}")
