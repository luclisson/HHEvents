import json
from datetime import datetime
from typing import Optional, List

class Event:
    DATE_FORMATS = [
        "%Y-%m-%dT%H:%M",    # ISO-Format mit Zeit
        "%d.%m.%Y %H:%M",    # Deutsches Datumsformat
        "%Y-%m-%d",          # ISO-Datum ohne Zeit
        "%a %b %d %Y %H:%M:%S GMT%z"  # Fallback für komplexe Formate
    ]

    def __init__(
        self,
        source: str,
        source_url: str,
        title: str,
        link: str,
        event_date: str,
        event_type: str,
        location: str,  # Jetzt erforderlicher Parameter
        price: Optional[str] = None,
        img_url: Optional[str] = None,
        description: Optional[str] = None,
        external_links: Optional[List[str]] = None
    ):
        """
        Initialisiert ein Event-Objekt mit Location-Unterstützung
        
        :param location: Veranstaltungsort (z.B. "Ballsaal, Hamburg")
        """
        self.source = source
        self.source_url = source_url
        self.title = title.strip()
        self.link = link
        self.event_date = self._parse_date(event_date)
        self.event_type = event_type
        self.location = location.strip()  # Pflichtfeld
        self.price = self._parse_price(price)
        self.img_url = img_url
        self.description = description.strip() if description else None
        self.external_links = external_links or []
        self.scraped_at = datetime.now().isoformat()

    def _parse_date(self, date_str: str) -> str:
        """Verarbeitet verschiedene Datumsformate"""
        # Bereinige überflüssige Kommas
        cleaned_date = date_str.split(',')[0].strip()
        
        for fmt in self.DATE_FORMATS:
            try:
                dt = datetime.strptime(cleaned_date, fmt)
                return dt.isoformat()
            except ValueError:
                continue
        return cleaned_date  # Fallback

    def _parse_price(self, price_str: Optional[str]) -> Optional[float]:
        """Konvertiert Preisangaben in Float"""
        if not price_str:
            return None
            
        try:
            # Entferne Währungszeichen und unerwünschte Zeichen
            cleaned = ''.join(c for c in price_str if c.isdigit() or c in ['.', ','])
            if ',' in cleaned:
                return float(cleaned.replace(',', '.'))
            return float(cleaned)
        except ValueError:
            return None

    def to_dict(self):
     return {
        'source': self.source,
        'source_url': self.source_url,
        'title': self.title,
        'link': self.link,
        'event_date': self.event_date,
        'event_type': self.event_type,
        'location': self.location,
        'price': self.price,
        'img_url': self.img_url,
        'description': self.description,
        # Konvertiere Listen zu Tuples für Hashbarkeit
        'external_links': tuple(self.external_links) if self.external_links else None,
        'scraped_at': self.scraped_at
    }


    def save_to_json(self, filename: str):
        """Speichert das Event in einer JSON-Datei"""
        with open(filename, 'a', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)
            f.write('\n')

    async def save_to_db(self, supabase_client):
        """Speichert in Supabase-Datenbank"""
        try:
            response = await supabase_client.from_('events').insert(self.to_dict()).execute()
            if not response.error:
                print(f"Event '{self.title}' gespeichert")
            else:
                print(f"Datenbankfehler: {response.error.message}")
        except Exception as e:
            print(f"Kritischer Fehler: {str(e)}")

    def __repr__(self):
        return (
            f"<Event("
            f"title={self.title!r}, "
            f"date={self.event_date}, "
            f"type={self.event_type}, "
            f"location={self.location!r}, "
            f"price={self.price})>"
        )

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return self.link == other.link and self.event_date == other.event_date
