# docks_scraper.py
from selenium.webdriver.common.by import By
from base_scraper import BaseScraper
from event import Event
import time
import logging
import re

class DocksScraper(BaseScraper):
    DATE_REGEX = re.compile(r"(\d{1,2}\.\d{1,2}\.\d{4})")

    def __init__(self, driver, page_type="docks"):
        location = "Docks Freiheit36" if page_type == "docks" else "Prinzenbar"
        super().__init__(driver=driver, source_name=location)
        self.location = location

    def click_next_page(self, current_page: int) -> bool:
        try:
            page_links = self.driver.find_elements(By.CSS_SELECTOR, "ul.pagination li.page-item")
            next_page = current_page + 1
            if next_page <= len(page_links):
                next_page_li = page_links[next_page - 1]
                next_page_link = next_page_li.find_element(By.CSS_SELECTOR, "a.page-link")
                self.driver.execute_script("arguments[0].click();", next_page_link)
                time.sleep(2)
                return True
            return False
        except Exception as e:
            logging.error(f"Paginierungsfehler: {str(e)}")
            return False

    def parse_event(self, container) -> Event:
        try:
            title = container.find_element(By.CSS_SELECTOR, 'h5.card-title').text.strip()
            link_element = container.find_element(By.CSS_SELECTOR, 'a.btn-link')
            
            meta_text = container.find_element(
                By.CSS_SELECTOR, 'p.card-text'
            ).text.strip()
            
            # Kategorie und Datum extrahieren
            if "|" in meta_text:
                category, date_str = map(str.strip, meta_text.split("|", 1))
            else:
                category = "Veranstaltung"
                date_str = meta_text
                
            date_match = self.DATE_REGEX.search(date_str)
            event_date = date_match.group(1) if date_match else "01.01.1970"

            return Event(
                source_url=self.driver.current_url,
                title=title,
                link=link_element.get_attribute('href'),
                event_date=event_date,
                time="To be announced",
                category=category,
                location=self.location,
                price=link_element.text.strip(),
                img_url=self._get_image_url(container)
            )
        except Exception as e:
            logging.error(f"Parse-Fehler: {str(e)}")
            return None

    def _get_image_url(self, container):
        try:
            return container.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        except Exception:
            return None
