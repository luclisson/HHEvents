from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from event import Event
import logging
import re
import time

class HHgegenrechtsScraper(BaseScraper):
    def __init__(self, driver):
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

    def _dismiss_cookie_banner(self):
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))
            )
            cookie_button.click()
            time.sleep(0.5)
        except TimeoutException:
            pass

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
                    lambda d: len(d.find_elements(*self.container_selector)) > current_count
                )
                time.sleep(1)
                
            except TimeoutException:
                logging.info("Keine weiteren Events verfügbar")
                break
            except Exception as e:
                logging.warning(f"Ladefehler: {str(e)}")
                break

    def parse_event(self, container) -> Event:
        try:
            # Datum
            date_element = container.find_element(By.CSS_SELECTOR, "div.callout_date")
            date_str = self._clean_date(date_element.get_attribute("textContent"))
            
            # Titel und Link
            title_element = container.find_element(By.CSS_SELECTOR, "h2.entry-title a")
            title = title_element.get_attribute("textContent")
            link = title_element.get_attribute("href")

            # Zeit
            time_str = date_str
            try:
                time_element = container.find_element(By.CSS_SELECTOR, "span.decm_date")
                time_str = f"{date_str} {time_element.get_attribute("textContent")}"
            except Exception:
                pass

            # Kategorien
            categories = []
            seen_cats = set()
            for cat in container.find_elements(By.CSS_SELECTOR, "span[class^='decm_categories'] a"):
                cat_text = cat.get_attribute("textContent")
                if cat_text and cat_text not in seen_cats:
                    categories.append(cat_text)
                    seen_cats.add(cat_text)

            # Beschreibung
            description = ""
            try:
                desc_element = container.find_element(By.CSS_SELECTOR, "div.decm-show-data-display-block")
                description = desc_element.text.strip()[:500]
            except Exception:
                pass

            # Bild
            img_url = None
            try:
                img = container.find_element(By.CSS_SELECTOR, "img.act-thumbnail")
                img_url = img.get_attribute("src").split("?")[0]
            except Exception:
                pass

            return Event(
                source=self.source_name,
                source_url=self.driver.current_url,
                title=title,
                link=link,
                event_date=self._clean_date(time_str),
                event_type=", ".join(categories) if categories else "Vortrag",
                location=self._parse_location(title),
                description=description,
                price=None,
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
        return False
