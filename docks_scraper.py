from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import re
import time
import logging

def scrape_docks_events(url):
    # Konfiguration des Edge-Browsers
    edge_options = Options()
    # edge_options.add_argument("--headless")  # Optional: Headless-Modus aktivieren

    # Einrichten des Edge-Treibers mit automatischer Verwaltung
    service = Service(EdgeChromiumDriverManager(log_level=logging.INFO).install())
    driver = webdriver.Edge(service=service, options=edge_options)

    print(f"Starte Web-Scraping von: {url}")
    driver.get(url)  # Öffnet die angegebene URL im Browser

    try:
        # Einrichten eines WebDriverWait-Objekts für explizites Warten (max. 30 Sekunden)
        wait = WebDriverWait(driver, 30)

        # Definition einer Funktion zum Scrollen bis zum Ende der Seite
        def scroll_to_bottom():
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Warte 2 Sekunden, damit neue Inhalte geladen werden können
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        # Führe das Scrollen aus
        scroll_to_bottom()
        print("Scrolling abgeschlossen.")

        # Suche nach allen Event-Containern auf der Seite
        event_containers = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.col-xxl-4.col-xl-4.col-lg-4.col-md-6.col-12.mb-4"))
        )
        num_events = len(event_containers)
        print(f"Anzahl der gefundenen Event-Container: {num_events}")

        events_data = []  # Liste zum Speichern aller Event-Daten

        # Durchlaufe alle gefundenen Event-Container
        for index, container in enumerate(event_containers, 1):
            try:
                event_data = {}

                # Titel extrahieren
                title_element = container.find_element(By.CSS_SELECTOR, 'h5.card-title')
                if title_element:
                    event_data['title'] = title_element.text.strip()

                # Ticket-Link extrahieren
                ticket_link_element = container.find_element(By.CSS_SELECTOR, 'a.btn-link')
                if ticket_link_element:
                    event_data['ticket_link'] = ticket_link_element.get_attribute('href')
                    event_data['ticket_price'] = ticket_link_element.text.strip()

                # Datum extrahieren
                date_element = container.find_element(By.CSS_SELECTOR, 'p.card-text')
                if date_element:
                    date_text = date_element.text.strip()
                    parts = date_text.split('|')
                    if len(parts) > 1:
                        event_data['event_type'] = parts[0].strip()
                        event_data['date'] = parts[1].strip()
                    else:
                        event_data['date'] = date_text  # Fallback if no '|' is found

                events_data.append(event_data)  # Speichere die Daten des Events

            except Exception as e:
                print(f"Fehler beim Extrahieren von Event {index}: {str(e)}")

        # Ausgabe aller gesammelten Events
        for event in events_data:
            print("\n--- Event ---")
            for key, value in event.items():
                print(f"{key}: {value}")

    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}")

    finally:
        print("Schließe den Browser...")
        driver.quit()

# URL der zu scrapenden Website
url = 'https://docksfreiheit36.de/docks/'

# Führe die Scraping-Funktion aus
scrape_docks_events(url)
