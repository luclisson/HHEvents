import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from Scraper.base_scraper import BaseScraper
from event import Event

# Mock-Klasse, um BaseScraper zu testen
class MockScraper(BaseScraper):
    def click_next_page(self, current_page: int) -> bool:
        # Beende nach der ersten Seite (keine Paginierung in diesem Test)
        return False

    def parse_event(self, container) -> Event:
        # Einfacher Mock für das Parsen eines Events
        title = container.find_element(By.TAG_NAME, "h2").text
        return Event(title=title, date="2025-01-01", location="Test Location", source=self.source_name)

@pytest.fixture(scope="module")
def driver():
    # Setze den Selenium WebDriver im Headless-Modus auf
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    service = Service("path/to/chromedriver")  # Pfad zu deinem ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_base_scraper_scrape(driver):
    # HTML-Mock-Daten für den Test
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

    # Lade die HTML-Mock-Daten in den WebDriver
    driver.get("data:text/html;charset=utf-8," + html_content)

    # Initialisiere den Mock-Scraper
    scraper = MockScraper(driver=driver, source_name="Test Source")

    # Führe das Scraping aus und überprüfe die Ergebnisse
    events = scraper.scrape("http://example.com")
    
    assert len(events) == 2  # Es sollten zwei Events gefunden werden
    
    assert events[0].title == "Event 1"
    assert events[0].date == "2025-01-01"
    assert events[0].location == "Test Location"
    
    assert events[1].title == "Event 2"
