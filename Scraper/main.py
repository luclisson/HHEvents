from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from docks_scraper import DocksScraper
from uebelundgefaehrlich_scraper import UebelUndGefaehrlichScraper
from hhgegenrechts_scraper import HHgegenrechtsScraper as hhgege
import logging
import json
from event import Event

def load_existing_events(filename: str) -> set:
    """Lade vorhandene Events aus einer JSON-Datei."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            event_dicts = [json.loads(line) for line in f]
            existing_events = {tuple(sorted(d.items())) for d in event_dicts}
    except FileNotFoundError:
        existing_events = set()
        print(f"Datei {filename} nicht gefunden. Starte mit leerer Menge.")
    except json.JSONDecodeError:
        print("Die JSON-Datei ist leer oder ungültig. Starte mit einer leeren Menge.")
        existing_events = set()
    return existing_events

def _is_valid_event(event: Event) -> bool:
    """Prüft Pflichtfelder gemäß Event-Klasse"""
    required_fields = [
        event.source_url,
        event.title,
        event.link,
        event.event_date,
        event.time,
        event.category
    ]
    return all(required_fields) and len(event.title) > 3

def save_new_events(filename: str, new_events: list[Event], existing_events: set):
    """Speichert nur neue Events in einer JSON-Datei."""
    new_count = 0
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            for event in new_events:
                if event and _is_valid_event(event):
                    event_dict = event.to_dict()
                    event_tuple = tuple(sorted(event_dict.items()))
                    if event_tuple not in existing_events:
                        json.dump(event_dict, f, ensure_ascii=False)
                        f.write('\n')
                        existing_events.add(event_tuple)
                        new_count += 1
                        logging.info(f"Neues Event gespeichert: {event.title}")
    except Exception as e:
        logging.error(f"Fehler beim Speichern von Events: {str(e)}")
    print(f"Gespeichert {new_count} neue Events in {filename}.")
    return existing_events

def main():
    logging.basicConfig(level=logging.INFO)
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

    try:
        json_filename = "all_events.json"
        existing_events = load_existing_events(json_filename)

        # Docks-Scraper
        docks_url = "https://docksfreiheit36.de/docks/"
        docks_scraper = DocksScraper(driver)
        docks_events = docks_scraper.scrape(docks_url)

        # Prinzenbar-Scraper
        prinzenbar_url = "https://docksfreiheit36.de/prinzenbar/"
        prinzenbar_scraper = DocksScraper(driver, page_type="prinzenbar")
        prinzenbar_events = prinzenbar_scraper.scrape(prinzenbar_url)

        # UebelUndGefaehrlich-Scraper
        uebelundgefaehrlich_url = "https://www.uebelundgefaehrlich.com/veranstaltungen/"
        uebelundgefaehrlich_scraper = UebelUndGefaehrlichScraper(driver)
        uebelundgefaehrlich_events = uebelundgefaehrlich_scraper.scrape(uebelundgefaehrlich_url)

        # Hamburg gegen Rechts Scraper
        hhgr_url = "https://vernetztgegenrechts.hamburg/veranstaltungen-2/"
        hhgr_scraper = hhgege(driver)
        hhgr_events = hhgr_scraper.scrape(hhgr_url)

        # Zusammenführen und Duplikate entfernen
        all_events = docks_events + prinzenbar_events + uebelundgefaehrlich_events + hhgr_events
        unique_events = []
        seen_events = set()
        duplicate_count = 0

        for event in all_events:
            if event:
                event_tuple = tuple(sorted(event.to_dict().items()))
                if event_tuple not in seen_events:
                    unique_events.append(event)
                    seen_events.add(event_tuple)
                else:
                    duplicate_count += 1

        print(f"Anzahl gefundener Duplikate: {duplicate_count}")
        valid_all_events = [event for event in unique_events if event is not None]
        updated_events = save_new_events(json_filename, valid_all_events, existing_events)

        # Ausgabe
        print(f"Gesamtanzahl gefundener Events (Docks): {len(docks_events)}")
        print(f"Gesamtanzahl gefundener Events (Prinzenbar): {len(prinzenbar_events)}")
        print(f"Gesamtanzahl gefundener Events (Uebel & Gefährlich): {len(uebelundgefaehrlich_events)}")
        print(f"Gesamtanzahl gefundener Events (Hamburg gegen Rechts): {len(hhgr_events)}")
        print(f"Gesamtanzahl aller Events: {len(valid_all_events)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
