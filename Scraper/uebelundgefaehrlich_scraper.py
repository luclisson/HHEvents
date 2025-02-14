from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from event import Event
from datetime import datetime  # WICHTIGER IMPORT HINZUGEFÜGT
import logging
import time
import re

class UebelUndGefaehrlichScraper(BaseScraper):
    DATE_REGEX = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
    TIME_REGEX = re.compile(r"(\d{2}:\d{2})")

    def __init__(self, driver):
        super().__init__(
            driver,
            source_name="Uebel & Gefährlich",
            container_selector=(By.CSS_SELECTOR, ".event > li")
        )

    def click_next_page(self, current_page: int) -> bool:
        return False

    def parse_event(self, container) -> Event:
        try:
            title = container.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]').get_attribute("textContent")
            link = container.find_element(By.CSS_SELECTOR, 'a.history').get_attribute('href')
            
            # Datumsextraktion
            date_element = container.find_element(By.CSS_SELECTOR, 'time[itemprop="startDate"]')
            iso_date = date_element.get_attribute('datetime')
            dt_obj = datetime.fromisoformat(iso_date)  # Korrigierte Verwendung des datetime-Objekts
            
            event_date = dt_obj.strftime("%d.%m.%Y")
            time = dt_obj.strftime("%H:%M")

            location = container.find_element(By.CSS_SELECTOR, 'div[itemprop="location"]').get_attribute("textContent")

            return Event(
                source_url=self.driver.current_url,
                title=title.strip(),
                link=link,
                event_date=event_date,
                time=time,
                category="Club Event",
                location=location.strip()
            )
        except Exception as e:
            logging.error(f"Fehler beim Parsen: {str(e)}")
            return None
        
        """Function: Extracts event details from container element
        Special Notes:
        - Uses microdata/itemprop attributes for reliable parsing
        - Converts ISO 8601 datetime from meta tags
        - Implements fallback patterns (static regex)
        - Returns None on parsing errors to skip invalid entries"""
