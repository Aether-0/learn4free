import requests
from bs4 import BeautifulSoup, SoupStrainer
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
import logging
from functools import lru_cache
from urllib.parse import urljoin, urlparse, parse_qs
from fake_useragent import UserAgent
import re

ua = UserAgent()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

class CourseScraper:
    def __init__(self, max_workers: int = 30, search_term: Optional[str] = None):
        self.base_url = "https://coursekingdom.xyz"
        self.search_term = search_term
        self.headers = {
            'User-Agent': f'{ua.random}',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        self.session = requests.Session()
        self.max_workers = min(max(max_workers, 1), 30)
        self.session.headers.update(self.headers)

    @lru_cache(maxsize=1)
    def get_last_page_number(self) -> int:
        """Get the total number of pages with retry logic, considering search term."""
        if self.search_term:
            url = urljoin(self.base_url, f"/courses?search={self.search_term}")
        else:
            url = urljoin(self.base_url, "/courses")
        
        for attempt in range(3):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                last_page_link = soup.find('a', string='Last')
                if last_page_link:
                    href = last_page_link['href']
                    parsed = urlparse(href)
                    query_params = parse_qs(parsed.query)
                    return int(query_params.get('page', [1])[0])
                return 1
            except (requests.RequestException, ValueError) as e:
                logging.warning(f"Attempt {attempt + 1}/3 failed to get last page: {e}")
                time.sleep(2 ** attempt)
        logging.error("Failed to determine last page number, defaulting to 1")
        return 1

    def fetch_page(self, page: int) -> Optional[str]:
        """Fetch a single page's HTML content with retry logic, considering search term."""
        if self.search_term:
            if page == 1:
                url = urljoin(self.base_url, f"/courses?search={self.search_term}")
            else:
                url = urljoin(self.base_url, f"/courses?page={page}&search={self.search_term}")
        else:
            if page == 1:
                url = urljoin(self.base_url, "/courses")
            else:
                url = urljoin(self.base_url, f"/courses?page={page}")
        
        for attempt in range(3):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logging.warning(f"Attempt {attempt + 1}/3 failed for page {page}: {e}")
                time.sleep(2 ** attempt)
        logging.error(f"Failed to fetch page {page} after 3 attempts")
        return None

    def extract_course_details(self, course_soup) -> Dict:
        """Extract essential course information, including a cleanly formatted date."""
        course_data = {
            'title': None,
            'role': None,
            'image': None,
            'link': None,
            'course_link': None,
            'coupon_code': None,
            'page': None,
            'date': None
        }
        
        try:
            link_tag = course_soup.find('a')
            if link_tag and 'href' in link_tag.attrs:
                course_data['link'] = urljoin(self.base_url, link_tag['href'])
            
            title_tag = course_soup.find('h3')
            course_data['title'] = title_tag.get_text(strip=True) if title_tag else None
            
            role_tag = course_soup.find('span')
            course_data['role'] = role_tag.get_text(strip=True) if role_tag else None
            
            img_tag = course_soup.find('img')
            course_data['image'] = urljoin(self.base_url, img_tag['src']) if img_tag and 'src' in img_tag.attrs else None
            
            star_div = course_soup.find('div', class_='star')
            if star_div:
                date_span = star_div.find('span')
                if date_span:
                    raw_date = date_span.get_text()
                    # Clean date: replace non-breaking spaces, collapse multiple whitespace, strip
                    cleaned_date = raw_date.replace('\xa0', ' ').strip()
                    course_data['date'] = re.sub(r'\s+', ' ', cleaned_date)
            
            return course_data
        except Exception as e:
            logging.error(f"Error extracting course details: {e}")
            return course_data

    def extract_coupon_code(self, url: str) -> tuple[Optional[str], Optional[str]]:
        """Extract coupon code and clean course link from course URL."""
        try:
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser', parse_only=SoupStrainer('a', class_='boxed_btn'))
            
            for link in soup:
                href = link.get('href', '')
                if 'udemy.com' in href and 'couponCode' in href:
                    coupon_start = href.find('couponCode=') + len('couponCode=')
                    coupon_end = href.find('&', coupon_start)
                    coupon_code = href[coupon_start:] if coupon_end == -1 else href[coupon_start:coupon_end]
                    course_link = href[:coupon_end] if coupon_end != -1 else href
                    return coupon_code, course_link
            return None, None
        except requests.RequestException as e:
            logging.error(f"Error extracting coupon code from {url}: {e}")
            return None, None

    def scrape_page(self, page: int) -> List[Dict]:
        """Scrape all courses from a single page."""
        page_html = self.fetch_page(page)
        if not page_html:
            return []

        soup = BeautifulSoup(page_html, 'html.parser', parse_only=SoupStrainer('div', class_='single_courses'))
        courses = []
        
        for course in soup:
            course_data = self.extract_course_details(course)
            if course_data['link']:
                coupon_code, course_link = self.extract_coupon_code(course_data['link'])
                course_data['coupon_code'] = coupon_code
                course_data['course_link'] = course_link
            course_data['page'] = page
            if course_data['title']:
                courses.append(course_data)
        
        return courses

    def scrape_all_courses(self) -> List[Dict]:
        """Scrape all courses using concurrent requests with auto-detected last page."""
        last_page = self.get_last_page_number()
        logging.info(f"Scraping {last_page} pages with {self.max_workers} workers")
        
        all_courses = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.scrape_page, page): page 
                       for page in range(1, last_page + 1)}
            
            for future in as_completed(futures):
                page = futures[future]
                try:
                    courses = future.result()
                    all_courses.extend(courses)
                    logging.info(f"Page {page}/{last_page} - Total courses: {len(all_courses)}")
                except Exception as e:
                    logging.error(f"Page {page} failed: {e}")
        
        return sorted(all_courses, key=lambda x: x.get('page', 0))
