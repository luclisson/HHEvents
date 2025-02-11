import requests
from bs4 import BeautifulSoup

def scrape_tunnel_events(url):
    print(f"Starte Web-Scraping von: {url}")
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Verbindung zur Webseite erfolgreich hergestellt.")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finde alle Event-Container
        event_containers = soup.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-8 MuiGrid-grid-md-9')
        print(f"Anzahl der gefundenen Event-Container: {len(event_containers)}")

        for container in event_containers:
            print("--- Neues Event ---")
            # Extrahiere den Titel des Events
            title_element = container.find('h2', class_='event-title')
            if title_element:
                title = title_element.text.strip()
                print(f"Titel gefunden: {title}")
            else:
                title = "Kein Titel gefunden"
                print("Kein Titel gefunden.")

            # Extrahiere den Link zum Eventbrite-Ticket
            ticket_link = container.find('a', href=lambda href: href and "eventbrite.de" in href)
            if ticket_link:
                ticket_url = ticket_link['href']
                print(f"Eventbrite Ticket URL gefunden: {ticket_url}")
            else:
                ticket_url = "Kein Ticketlink gefunden"
                print("Kein Ticketlink gefunden")
            
            # Extrahiere den Link zur Facebook-Veranstaltung
            facebook_link = container.find('a', href=lambda href: href and "facebook.com/events" in href)
            if facebook_link:
                facebook_url = facebook_link['href']
                print(f"Facebook Event URL gefunden: {facebook_url}")
            else:
                facebook_url = "Kein Facebooklink gefunden"
                print("Kein Facebooklink gefunden")

            # Extrahiere das Datum aus dem Event-Text
            event_div = container.find('div', class_='event')
            if event_div:
                event_text = event_div.get_text(separator='\n').strip()
                date_line = next((line for line in event_text.split('\n') if "Februar" in line or "März" in line or "April" in line), None)
                date = date_line if date_line else "Kein Datum gefunden"
                print(f"Datum gefunden: {date}")
            else:
                date = "Kein Datum gefunden"
                print("Kein Datum gefunden.")

            # Gib die extrahierten Informationen aus
            print(f"Titel: {title}")
            print(f"Datum: {date}")
            print(f"Eventbrite Ticket URL: {ticket_url}")
            print(f"Facebook Event URL: {facebook_url}")
            print("---")
    else:
        print(f"Fehler beim Abrufen der Seite. Statuscode: {response.status_code}")

# URL der Tunnel-Website
url = 'https://www.tunnel.de'

# Führe das Scraping aus
scrape_tunnel_events(url)
