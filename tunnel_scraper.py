# Importieren der benötigten Selenium-Module und Funktionen
from selenium import webdriver  # Hauptmodul für die Browsersteuerung
from selenium.webdriver.edge.service import Service  # Dienst für den Edge-Treiber
from selenium.webdriver.edge.options import Options  # Optionen für den Edge-Browser
from selenium.webdriver.common.by import By  # Lokalisierungsstrategien für Elemente
from selenium.webdriver.support.ui import WebDriverWait  # Explizites Warten auf Elemente
from selenium.webdriver.support import expected_conditions as EC  # Bedingungen für das Warten
from webdriver_manager.microsoft import EdgeChromiumDriverManager  # Automatische Verwaltung des Edge-Treibers
import time  # Für Verzögerungen

def scrape_tunnel_events(url):
    # Konfiguration des Edge-Browsers
    edge_options = Options()
    # edge_options.add_argument("--headless")  # Auskommentiert: Würde den Browser im Hintergrund ausführen

    # Einrichten des Edge-Treibers mit automatischer Verwaltung
    service = Service(EdgeChromiumDriverManager().install())
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
                # Scrolle bis zum Ende der Seite
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Warte 2 Sekunden, damit neue Inhalte geladen werden können
                
                # Überprüfe, ob neue Inhalte geladen wurden
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # Wenn keine neuen Inhalte geladen wurden, beende das Scrollen
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

        # Durchlaufe alle gefundenen Event-Container
        for index, container in enumerate(event_containers, 1):
            try:
                # Versuche, das Titelelement innerhalb des Containers zu finden
                title_element = container.find_element(By.CSS_SELECTOR, "h2.event-title")
                title = title_element.text.strip()  # Extrahiere den Text und entferne Leerzeichen
                print(f"Titel {index}: {title}")
            except Exception as e:
                # Wenn ein Fehler auftritt, gib eine Fehlermeldung aus
                print(f"Fehler beim Extrahieren des Titels für Event {index}: {str(e)}")

    except Exception as e:
        # Fange alle unerwarteten Fehler ab und gib sie aus
        print(f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}")

    finally:
        # Stelle sicher, dass der Browser immer geschlossen wird, auch wenn Fehler auftreten
        print("Schließe den Browser...")
        driver.quit()

# URL der zu scrapenden Website
url = 'https://www.tunnel.de/'

# Führe die Scraping-Funktion aus
scrape_tunnel_events(url)
# In diesem Beispiel haben wir die Funktion `scrape_tunnel_events` erstellt, die das Web-Scraping von Event-Informationen auf der Tunnel-Website durchführt.
# Wir verwenden das Selenium-Modul, um den Edge-Browser zu steuern und die dynamisch geladenen Inhalte zu erfassen.