from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from docks_scraper import DocksScraper
from uebelundgefaehrlich_scraper import UebelUndGefaehrlichScraper
from hhgegenrechts_scraper import HHgegenrechtsScraper as hhgege
import logging
import json
from event import Event
from typing import List, Dict

def load_existing_events(filename: str) -> List[Dict]:
    """Lade vorhandene Events als JSON-Array"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Datei {filename} nicht gefunden. Neuanlage erfolgt.")
        return []
    except json.JSONDecodeError:
        print("Ungültiges JSON-Format. Starte mit leerer Liste.")
        return []

def _is_valid_event(event: Event) -> bool:
    """Prüfe obligatorische Felder"""
    required_fields = [
        event.source_url,
        event.title,
        event.link,
        event.event_date,
        event.time,
        event.category
    ]
    return all(required_fields) and len(event.title.strip()) > 3

def save_new_events(filename: str, new_events: List[Event], existing_events: List[Dict]) -> List[Dict]:
    """Speichere Events als JSON-Array mit Duplikatsprüfung"""
    existing_tuples = {tuple(sorted(e.items())) for e in existing_events}
    updated_events = existing_events.copy()
    new_count = 0

    for event in new_events:
        if event and _is_valid_event(event):
            event_dict = event.to_dict()
            event_tuple = tuple(sorted(event_dict.items()))
            
            if event_tuple not in existing_tuples:
                updated_events.append(event_dict)
                existing_tuples.add(event_tuple)
                new_count += 1
                logging.info(f"Neues Event: {event.title}")
            else:
                logging.debug(f"Duplikat übersprungen: {event.title}")

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(updated_events, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Speicherfehler: {str(e)}")
    
    print(f"{new_count} neue Events hinzugefügt. Gesamt: {len(updated_events)}")
    return updated_events

def main():
    logging.basicConfig(level=logging.INFO)
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

    try:
        json_filename = "all_events.json"
        existing_events = load_existing_events(json_filename)

        # Scrape Docks
        docks_scraper = DocksScraper(driver)
        docks_events = docks_scraper.scrape("https://docksfreiheit36.de/docks/")

        # Scrape Prinzenbar
        prinzenbar_scraper = DocksScraper(driver, page_type="prinzenbar")
        prinzenbar_events = prinzenbar_scraper.scrape("https://docksfreiheit36.de/prinzenbar/")

        # Scrape Uebel & Gefährlich
        uebel_scraper = UebelUndGefaehrlichScraper(driver)
        uebel_events = uebel_scraper.scrape("https://www.uebelundgefaehrlich.com/veranstaltungen/")

        # Scrape Hamburg gegen Rechts
        hhgr_scraper = hhgege(driver)
        hhgr_events = hhgr_scraper.scrape("https://vernetztgegenrechts.hamburg/veranstaltungen-2/")

        # Kombiniere und filtere Events
        all_events = docks_events + prinzenbar_events + uebel_events + hhgr_events
        unique_events = []
        seen = set()
        
        for event in all_events:
            if event:
                event_data = event.to_dict()
                event_key = (event_data['link'], event_data['event_date'], event_data['time'])
                if event_key not in seen:
                    unique_events.append(event)
                    seen.add(event_key)

        # Speichere Ergebnisse
        updated = save_new_events(json_filename, unique_events, existing_events)

        # Statistik
        print("\n=== Scraping-Statistik ===")
        print(f"Docks Events: {len(docks_events)}")
        print(f"Prinzenbar Events: {len(prinzenbar_events)}")
        print(f"Uebel & Gefährlich Events: {len(uebel_events)}")
        print(f"Hamburg gegen Rechts Events: {len(hhgr_events)}")
        print(f"Eindeutige Events gesamt: {len(updated)}")

    except Exception as e:
        logging.error(f"Kritischer Fehler: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
