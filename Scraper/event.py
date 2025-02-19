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
        source_url: str,
        title: str,
        link: str,
        event_date: str,  # Format: DD.MM.YYYY
        time: str,        # Format: HH:MM
        category: str,
        location: Optional[str] = None,    
        price: Optional[str] = None,
        img_url: Optional[str] = None
    ):
        """
        Initialisiert ein Event-Objekt mit Location-Unterstützung
        
        :param location: Veranstaltungsort (z.B. "Ballsaal, Hamburg")
        """
        self.source_url = source_url
        self.title = title.strip()
        self.link = link
        self.event_date = self._parse_date(event_date)
        self.time = time
        self.category = category
        self.location = location.strip() if location else None  # Pflichtfeld
        self.price = self._parse_price(price)
        self.img_url = img_url
        self.scraped_at = datetime.now().isoformat()

    def _parse_date(self, date_str: str) -> str:
        """Verarbeitet verschiedene Datumsformate"""
        cleaned_date = date_str.split(',')[0].strip()
        
        for fmt in self.DATE_FORMATS:
            try:
                dt = datetime.strptime(cleaned_date, fmt)
                return dt.isoformat()
            except ValueError:
                continue
        
        # If no format matches, try to parse as German date format
        try:
            dt = datetime.strptime(cleaned_date, "%d.%m.%Y")
            return dt.strftime("%d.%m.%Y")  # Instead of dt.isoformat()

        except ValueError:
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
            'source_url': self.source_url,
            'title': self.title,
            'link': self.link,
            'event_date': self.event_date,
            'time': self.time,
            'category': self.category,
            'location': self.location,
            'price': self.price,
            'img_url': self.img_url,
            'scraped_at': self.scraped_at
        }

    def save_to_json(self, filename: str):
        """Speichert das Event in einer JSON-Datei"""
        with open(filename, 'a', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)
            f.write('\n')

    def __repr__(self):
        return (
            f"<Event("
            f"title={self.title!r}, "
            f"date={self.event_date}, "
            f"time={self.time}, "
            f"category={self.category!r}, "
            f"location={self.location!r}, "
            f"price={self.price})>"
        )

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return self.link == other.link and self.event_date == other.event_date and self.time == other.time
