from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from event import Event
import logging
import time

class UebelUndGefaehrlichScraper(BaseScraper):
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
            logging.info("Versuche, Event-Informationen zu extrahieren...")
            
            # Extrahiere Basisinformationen aus dem Container
            try:
                title = container.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]').get_attribute("textContent")
                logging.info(f"Titel gefunden: {title}")
            except Exception as e:
                logging.error(f"Fehler beim Finden des Titels: {str(e)}")
                title = None
            
            try:
                link = container.find_element(By.CSS_SELECTOR, 'a.history').get_attribute('href')
                logging.info(f"Link gefunden: {link}")
            except Exception as e:
                logging.error(f"Fehler beim Finden des Links: {str(e)}")
                link = None
            
            try:
                date_element = container.find_element(By.CSS_SELECTOR, 'time[itemprop="startDate"]')
                date_text = f"{date_element.get_attribute('datetime')}, {date_element.text}"
                logging.info(f"Datum gefunden: {date_text}")
            except Exception as e:
                logging.error(f"Fehler beim Finden des Datums: {str(e)}")
                date_text = None
            
            try:
                location = container.find_element(By.CSS_SELECTOR, 'div[itemprop="location"]').get_attribute("textContent")
                logging.info(f"Ort gefunden: {location}")
            except Exception as e:
                logging.error(f"Fehler beim Finden des Ortes: {str(e)}")
                location = None

            if not all([title, link, date_text, location]):
                logging.error("Nicht alle erforderlichen Informationen gefunden. Event wird nicht gespeichert.")
                return None

            event = Event(
                source=self.source_name,
                source_url=self.driver.current_url,
                title=title,
                link=link,
                event_date=date_text,
                event_type=container.get_attribute('class').split()[0],
                location=location,
                price=None
            )

            # Debug-Ausgabe in eine Log-Datei schreiben
            with open("event_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"""
                {'='*40}
                Event-Dump:
                {event!r}
                Source URL: {self.driver.current_url}
                Container HTML: {container.get_attribute('outerHTML')[:200]}...
                {'='*40}
                """)
            
            return event

        except Exception as e:
            logging.error(f"Fehler beim Parsen: {str(e)}")
            with open("event_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"Fehlerhaftes Container-HTML: {container.get_attribute('outerHTML')[:500]}\n")
            return None
