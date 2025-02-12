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

def scrape_tunnel_events(url):
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
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-8.MuiGrid-grid-md-9"))
        )
        num_events = len(event_containers)
        print(f"Anzahl der gefundenen Event-Container: {num_events}")

        events_data = []  # Liste zum Speichern aller Event-Daten

        # Durchlaufe alle gefundenen Event-Container
        for index, container in enumerate(event_containers, 1):
            try:
                # Extrahiere den HTML-Inhalt des Containers mit BeautifulSoup
                html_content = container.get_attribute('outerHTML')
                soup = BeautifulSoup(html_content, 'html.parser')

                event_data = {}

                # Titel extrahieren
                title_element = soup.find('h2', class_='event-title')
                if title_element:
                    event_data['title'] = title_element.text.strip()

                # Ticket-Link extrahieren
                ticket_button = soup.find('a', class_='no-after')
                if ticket_button:
                    event_data['ticket_link'] = ticket_button.get('href')

                # Datum und Uhrzeit extrahieren
                date_time_pattern = r'(\d{1,2}\.\s*\w+\s*\d{4}).*?(\d{2}:\d{2})'
                date_time_match = re.search(date_time_pattern, soup.text, re.DOTALL)
                if date_time_match:
                    event_data['date'] = date_time_match.group(1).strip()
                    event_data['time'] = date_time_match.group(2).strip()

                # Ort extrahieren
                location_pattern = r'📍(.+)'
                location_match = re.search(location_pattern, soup.text)
                if location_match:
                    event_data['location'] = location_match.group(1).strip()
                else:
                    docks_match = re.search(r'DOCKS.*Hamburg', soup.text)
                    if docks_match:
                        event_data['location'] = docks_match.group(0).strip()

                # Künstler extrahieren
                artists = []
                artist_elements = soup.find_all('p', string=lambda text: '★' in text if text else False)
                for element in artist_elements:
                    artists.extend([artist.strip() for artist in element.text.split('★') if artist.strip()])
                event_data['artists'] = list(set(artists))

                # Facebook-Event-Link extrahieren
                fb_link_element = soup.find('a', string=lambda text: 'Facebook' in text if text else False)
                if fb_link_element:
                    event_data['facebook_link'] = fb_link_element.get('href')

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
url = 'https://www.tunnel.de/'

# Führe die Scraping-Funktion aus
scrape_tunnel_events(url)
