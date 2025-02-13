from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from event import Event
import logging
import time


class BaseScraper:
    def __init__(self, driver: WebDriver, source_name: str, container_selector = (By.CSS_SELECTOR, "div.col-xxl-4.col-xl-4.col-lg-4.col-md-6.col-12.mb-4")):
        self.driver = driver
        self.source_name = source_name
        self.wait = WebDriverWait(driver, 30)
        self.container_selector = container_selector

        """Function: Initializes base scraper with common configuration
           Special Notes: 
           - Container selector uses CSS by default for event containers
           - WebDriverWait set to 30s timeout for all child classes"""

    def scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            """Function: Automatically scrolls to page bottom to load dynamic content
           Special Notes:
           - Uses incremental height checks to detect end of page
           - Includes 2s pause between scrolls for content loading"""

    def click_next_page(self, current_page: int) -> bool:
        # Allgemeine Implementierung für Paginierung (wird von Kindklassen überschrieben)
        pass

    def parse_event(self, container) -> Event:
        # Muss in Kindklassen implementiert werden
        raise NotImplementedError

    def scrape(self, url: str) -> list[Event]:
        # Allgemeiner Scraping-Ablauf
        print(f"Starte das Scraping von {url}")
        
        self.driver.get(url)
        events = []
        
        current_page = 1  # Start auf Seite 1
        
        while True:
            print(f"Scraping Seite {current_page}...")
            
            containers = self.wait.until(
                EC.presence_of_all_elements_located(self.container_selector)
            )
            
            for index, container in enumerate(containers):
                try:
                    event = self.parse_event(container)
                    events.append(event)
                    print(f"[{current_page}-{index + 1}] Gefundenes Event: {event}")
                except Exception as e:
                    print(f"Fehler beim Parsen eines Events auf Seite {current_page}: {str(e)}")
            
            if not self.click_next_page(current_page):
                print("Keine weiteren Seiten gefunden. Beende das Scraping.")
                break
            
            current_page += 1
        
        return events
    
    """Function: Executes full scraping workflow
           Special Notes:
           - Implements automatic pagination loop
           - Tolerates individual event parsing errors
           - Logs progress with page/item numbers"""
