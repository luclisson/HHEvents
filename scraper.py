from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
from HHgegenRechts import EventHHgegenRechts

# Setup Selenium WebDriver for Firefox
options = Options()
#options.add_argument("--headless")  # Run in headless mode (remove this if you want to see the browser)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

url = "https://vernetztgegenrechts.hamburg/veranstaltungen-2/"
driver.get(url)

# Wait until the page loads
wait = WebDriverWait(driver, 10)

# Extract the full page source and pass it to BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()  # Close the browser after extracting the data

# Now parse the fully loaded HTML with BeautifulSoup
rows = soup.find_all("div", class_="row")  # Each row represents an event

# Default values
description = "no description was found"
linkElement = "no link was found"
eventTimeStringValue = "no time was found :("
categories = ["no category was registered"]
# Iterate through the events
for i in range(len(rows)):
    try:
        event_content = rows[i].find("div", class_="decm-events-details")
        description = event_content.find("p", class_="decm-show-data-display-block ecs-excerpt")
        linkElement = event_content.find("a", class_="act-view-more et_pb_button et_pb_custom_button_icon et_pb_button_no_hover")
        eventTime = event_content.find("span", class_="decm_date")
        eventTitleH2 = event_content.select('h2[class^="entry-title"]')
        EventTitleValue = eventTitleH2[0].find("a").string

        if eventTime:
            eventTimeStringValue = eventTime.string

        eventCategoryElement = event_content.select('span[class^="decm_categories ecs_category_"]')
        if eventCategoryElement:
            categories = []  # Clear list if categories were detected
        for element in eventCategoryElement:
            aList = element.find_all("a")
            for a in aList:
                categories.append(a.text)

        event = EventHHgegenRechts(
            title=EventTitleValue,
            time=eventTimeStringValue,
            link=linkElement['href'],
            description=description.text if description else "No description available",
            categories=categories
        )

        print(event)
        print("----------------")

    except Exception as e:
        print(f"Error processing event {i}: {e}")
