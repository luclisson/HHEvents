from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from event import Event
import logging
import re
import time
import datetime

class HHgegenrechtsScraper(BaseScraper):
    DATE_RANGE_REGEX = re.compile(
        r"(\d{2}\.\d{2})\.?\s*-\s*(\d{2}\.\d{2})\.?"
    )
    TIME_REGEX = re.compile(r"(\d{2}:\d{2})")

    def __init__(self, driver):
        self.current_year = datetime.datetime.now().year
        super().__init__(
            driver=driver,
            source_name="HH gegen Rechts",
            container_selector=(By.CSS_SELECTOR, "article.act-post")
        )
        self.max_load_attempts = 1
        self.loaded_pages = set()

    def scrape(self, url):
        self.driver.get(url)
        self._dismiss_cookie_banner()
        self._load_all_events()
        return super().scrape(url)


    def _load_all_events(self):
        last_count = 0
        for _ in range(self.max_load_attempts):
            try:
                current_count = len(self.driver.find_elements(*self.container_selector))
                if current_count == last_count:
                    break
                last_count = current_count
                load_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ecs-ajax_load_more:not(.disabled)"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", load_button)
                self.driver.execute_script("arguments[0].click();", load_button)
                self.wait.until(
                    lambda d: len(d.find_elements(*self.container_selector)) > 
                    current_count and 
                    d.execute_script("return document.readyState") == "complete")
                
                time.sleep(1)
            except TimeoutException:
                logging.info("Keine weiteren Events verfügbar")
                break
            except Exception as e:
                logging.warning(f"Ladefehler: {str(e)}")
                break

                """Function: Loads paginated content via AJAX
           Special Notes:
           - Uses JavaScript click for reliability
           - Tracks loaded pages to prevent duplicates
           - Implements safety counter (max_load_attempts)
           - Detects failed loads through container count"""

    def parse_event(self, container) -> Event:
        try:
            date_element = container.find_element(By.CSS_SELECTOR, "div.callout_date")
            raw_date = date_element.get_attribute("textContent") 
            
            # Jahr hinzufügen
            match = self.DATE_RANGE_REGEX.match(raw_date)
            if match:
                start = f"{match.group(1).strip('. ')}.{self.current_year}"
                end = f"{match.group(2).strip('. ')}.{self.current_year}"
                formatted_date = f"{start} - {end}"
            else:
                formatted_date = f"{raw_date.strip('. ')}.{self.current_year}"

            # Zeit Extraktion
            time_element = container.find_element(By.CSS_SELECTOR, "span.decm_date")
            event_time = time_element.get_attribute("textContent")

            # Titel und Link
            title_element = container.find_element(By.CSS_SELECTOR, "h2.entry-title a")
            title = title_element.get_attribute("textContent")
            link = title_element.get_attribute("href")

            # Kategorien
            categories = []
            seen_cats = set()
            for cat in container.find_elements(By.CSS_SELECTOR, "span[class^='decm_categories'] a"):
                cat_text = cat.get_attribute("textContent")
                if cat_text and cat_text not in seen_cats:
                    categories.append(cat_text)
                    seen_cats.add(cat_text)

            # Bild
            img_url = None
            try:
                img = container.find_element(By.CSS_SELECTOR, "img.act-thumbnail")
                img_url = img.get_attribute("src").split("?")[0]
            except Exception:
                pass

            return Event(
                source_url=self.driver.current_url,
                title=title.strip(),
                link=link,
                event_date=formatted_date,
                time=event_time,
                category=", ".join(categories) if categories else "Vortrag",
                location=self._parse_location(title),
                img_url=img_url
            )
        except Exception as e:
            logging.error(f"Parsefehler: {str(e)}")
            return None

    def _clean_date(self, date_str: str) -> str:
        return re.sub(r"\s+", " ", date_str).replace("Uhr", "").strip(" ,-")

    def _parse_location(self, title: str) -> str:
        locations = {
            "harburg": "Harburg, Hamburg",
            "altona": "Altona, Hamburg",
            "st. pauli": "St. Pauli, Hamburg",
            "wandsbek": "Wandsbek, Hamburg",
            "fuhlsbüttel": "Gedenkstätte Fuhlsbüttel, Hamburg",
            "bergedorf": "Bergedorf, Hamburg",
            "eimsbüttel": "Eimsbüttel, Hamburg"
        }
        lower_title = title.lower()
        for keyword, location in locations.items():
            if keyword in lower_title:
                return location
        return "Hamburg"

    def click_next_page(self, current_page: int) -> bool:
        logging.info(f"Current page: {current_page}")
        return False
