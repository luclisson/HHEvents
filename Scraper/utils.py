import json
from event import Event
import logging

def load_existing_events(filename: str) -> set:
    """Lade vorhandene Events aus einer JSON-Datei."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            event_dicts = [json.loads(line) for line in f]  # Lese jedes JSON-Objekt aus einer eigenen Zeile
            existing_events = {tuple(sorted(d.items())) for d in event_dicts}  # Konvertiere dicts in tuples
    except FileNotFoundError:
        existing_events = set()  # Erstelle eine leere Menge, wenn die Datei nicht existiert
        print(f"Datei {filename} nicht gefunden. Starte mit leerer Menge.")
    except json.JSONDecodeError:
        print("Die JSON-Datei ist leer oder ungültig. Starte mit einer leeren Menge.")
        existing_events = set()
    return existing_events

def save_new_events(filename: str, new_events: list[Event], existing_events: set):
    """Speichere nur neue Events in einer JSON-Datei."""
    new_count = 0
    try:
        with open(filename, 'a', encoding='utf-8') as f:  # Verwende 'a' für anhängen
            for event in new_events:
                if event:  # Stelle sicher, dass das Event nicht None ist
                    event_dict = event.to_dict()
                    event_tuple = tuple(sorted(event_dict.items()))  # Konvertiere in Tupel
                    if event_tuple not in existing_events:
                        json.dump(event_dict, f, ensure_ascii=False)  # Speichere dict
                        f.write('\n')  # Füge eine neue Zeile hinzu
                        existing_events.add(event_tuple)  # Füge Tupel zur Menge hinzu
                        new_count += 1
                        logging.info(f"Neues Event gespeichert: {event.title}")
    except Exception as e:
        logging.error(f"Fehler beim Speichern von Events: {str(e)}")
    print(f"Gespeichert {new_count} neue Events in {filename}.")
    return existing_events
