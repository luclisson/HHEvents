import json
from datetime import datetime

class Event:
    DATE_FORMAT = "%d.%m.%Y"  # Standard-Datumsformat

    def __init__(self, source: str, source_url: str, title: str, link: str, 
                 event_date: str, event_type: str, price: str = None, img_url: str = None):
        """Initialisiert ein Event-Objekt mit den wichtigsten Attributen."""
        self.source = source
        self.source_url = source_url
        self.title = title
        self.link = link
        self.event_date = self._parse_date(event_date)
        self.event_type = event_type
        self.price = price
        self.img_url = img_url
        self.scraped_at = datetime.now().isoformat()  # Zeitpunkt des Scrapings

    def _parse_date(self, date_str: str) -> str:
        """Standardisiert das Datumsformat. Gibt das ursprüngliche Datum zurück,
        falls das Parsing fehlschlägt."""
        try:
            return datetime.strptime(date_str, self.DATE_FORMAT).isoformat()
        except ValueError:
            return date_str  # Fallback zu Originaldatum

    def to_dict(self):
        """Konvertiert das Event-Objekt in ein Dictionary."""
        return {
            'source': self.source,
            'source_url': self.source_url,
            'title': self.title,
            'link': self.link,
            'event_date': self.event_date,
            'event_type': self.event_type,
            'price': self.price,
            'img_url': self.img_url,
            'scraped_at': self.scraped_at
        }

    def save_to_json(self, filename: str):
        """Speichert das Event in einer JSON-Datei (eine Zeile pro Event)."""
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.to_dict(), ensure_ascii=False) + '\n')

    async def save_to_db(self, supabase_client):
        """Speichert das Event in einer Supabase-Datenbank.
        
        :param supabase_client: Ein Supabase-Client für die Datenbankinteraktion."""
        try:
            await supabase_client.from_('events').insert(self.to_dict())
            print(f"Event '{self.title}' erfolgreich in die Datenbank eingefügt.")
        except Exception as e:
            print(f"Fehler beim Speichern von '{self.title}' in der Datenbank: {str(e)}")

    def __repr__(self):
        """Gibt eine lesbare Darstellung des Event-Objekts zurück (für Debugging)."""
        return (f"Event(title='{self.title}', date='{self.event_date}', "
                f"type='{self.event_type}', price='{self.price}', img_url='{self.img_url}')")