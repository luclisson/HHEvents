from selenium.webdriver.common.by import By
from base_scraper import BaseScraper
from event import Event
import time
import logging
import re

class DocksScraper(BaseScraper):
    DATE_REGEX = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
    TIME_REGEX = re.compile(r"(\d{2}:\d{2})")

    def __init__(self, driver, page_type="docks"):
        self.page_type = page_type
        location = "Docks Freiheit36" if page_type == "docks" else "Prinzenbar"
        super().__init__(
            driver=driver,
            source_name=location
        )
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
            logging.error(f"Fehler bei der Paginierung auf Seite {current_page}: {str(e)}")
            return False

    def parse_event(self, container) -> Event:
        try:
            title = container.find_element(By.CSS_SELECTOR, 'h5.card-title').text.strip()
            link_element = container.find_element(By.CSS_SELECTOR, 'a.btn-link')
            link = link_element.get_attribute('href')
            price = link_element.text.strip()
            date_text = container.find_element(By.CSS_SELECTOR, 'p.card-text').text.strip()
            
            # Datum und Zeit Separieren
            date_match = self.DATE_REGEX.search(date_text)
            time_match = self.TIME_REGEX.search(date_text)
            
            event_date = date_match.group(1) if date_match else "01.01.1970"
            time = time_match.group(1) if time_match else "20:00"

            try:
                img_url = container.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            except Exception:
                img_url = None

            return Event(
                source_url=self.driver.current_url,
                title=title,
                link=link,
                event_date=event_date,
                time=time,
                category="Konzert",
                location=self.location,
                price=price,
                img_url=img_url
            )
        except Exception as e:
            logging.error(f"Fehler beim Parsen eines Events: {str(e)}")
            return None
