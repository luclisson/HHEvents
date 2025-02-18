import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
import os
import sys

# Add the parent folder (Scraper) to the search path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from base_scraper import BaseScraper
from event import Event

# Mock class to test BaseScraper
class MockScraper(BaseScraper):
    def click_next_page(self, current_page: int) -> bool:
        return False

    def parse_event(self, container) -> Event:
        title = container.find_element(By.TAG_NAME, "h2").text
        return Event(
            source_url="https://example.com",
            title=title,
            link="https://example.com/event",
            event_date="2025-01-01",
            time="00:00",
            category="Test Category",
            location="Test Location",
            price="Free",
            img_url=None
        )

    def scrape(self, url: str) -> list[Event]:
        events = []
        containers = self.wait.until(
            EC.presence_of_all_elements_located(self.container_selector)
        )
        for container in containers:
            event = self.parse_event(container)
            events.append(event)
        return events

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Erstellen Sie ein einzigartiges temporäres Verzeichnis
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    yield driver
    driver.quit()
    
    # Bereinigen Sie das temporäre Verzeichnis nach dem Test
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass

def test_base_scraper_scrape(driver):
    html_content = """
    <html>
        <body>
            <div class="col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-12 mb-4">
                <h2>Event 1</h2>
            </div>
            <div class="col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-12 mb-4">
                <h2>Event 2</h2>
            </div>
        </body>
    </html>
    """

    # Load the HTML mock-up directly into the driver
    driver.get("data:text/html;charset=utf-8," + html_content)
    
    # Initialize the Mock-Scraper
    scraper = MockScraper(driver=driver, source_name="Test Source")
    
    # Execute the scraping
    events = scraper.scrape("dummy_url")
    
    # Assertions
    assert len(events) == 2  
    assert events[0].title == "Event 1"
    assert events[1].title == "Event 2"

if __name__ == "__main__":
    pytest.main([__file__])
