
# Hamburg Events Hub

Hamburg Events

[CI Pipeline
[License: MIT

## 📌 Inhaltsverzeichnis
- [Über das Projekt](#über-das-projekt)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Projektstruktur](#projektstruktur)
- [Datenquellen](#datenquellen)
- [Scrum Prozess](#scrum-prozess)
- [Nächste Schritte](#nächste-schritte)
- [Erweiterungsideen](#erweiterungsideen)
- [Mitwirkende](#mitwirkende)
- [Lizenz](#lizenz)

## 🌟 Über das Projekt

Hamburg Events Hub ist eine zentrale Plattform, die alle Events in Hamburg an einem Ort zusammenführt. Unser Ziel ist es, Hamburgern und Besuchern einen umfassenden Überblick über das vielfältige Veranstaltungsangebot der Stadt zu bieten. Der Fokus liegt auf einer effizienten Datenaggregation und einer benutzerfreundlichen Oberfläche.

## 🎉 Features

- **Event-Aggregation:** Automatisiertes Scraping von Events aus verschiedenen Quellen wie Docks.de, Übel und Gefährlich und HH gegen Rechts.
- **Datenbankintegration:** Speicherung der Events in einer PostgreSQL-Datenbank mit Supabase als Backend.
- **Echtzeit-Daten:** Tägliche Updates der Event-Daten.
- **Interaktive Oberfläche:** Übersichtliche Darstellung der Events mit Filtermöglichkeiten.
- **Datenexport:** Möglichkeit, Events als JSON-Datei herunterzuladen.

## 🛠️ Tech Stack

### Frontend:
- **HTML/CSS/JavaScript**: Klassisches Frontend für die Event-Darstellung.
- **Framer Motion**: Animationen für interaktive Elemente.

### Backend:
- **Supabase**: PostgreSQL-Datenbank mit API-Unterstützung.
- **Selenium & BeautifulSoup**: Web-Scraping für Event-Daten.

### DevOps:
- **Docker Compose**: Containerisierung von Services.
- **GitHub Actions**: Automatisierte Tests und Deployment.

## 🚀 Getting Started

1. **Repository klonen:**
```bash
git clone https://github.com/your-repo/hamburg-events-hub.git
cd hamburg-events-hub
```

2. **Umgebungsvariablen einrichten:**
```bash
cp env.json.example env.json
```
Fülle die notwendigen Werte in der `env.json` Datei aus (z. B. Supabase API-Schlüssel).

3. **Abhängigkeiten installieren:**
```bash
npm install
pip install -r requirements.txt
```

4. **Datenbank einrichten:**
```bash
docker-compose up -d
```

5. **Scraper starten:**
```bash
python Scraper/main.py
```

6. **Frontend starten (optional):**
Öffne die Datei `UI/index.html` im Browser.

## 📂 Projektstruktur

```
HamburgEvents/
├── Scraper/                 # Python-basierte Scraper
│   ├── base_scraper.py      # Basisklasse für alle Scraper
│   ├── docks_scraper.py     # Scraper für Docks Freiheit36
│   ├── hhgegenrechts_scraper.py  # Scraper für HH gegen Rechts
│   ├── uebelundgefaehrlich_scraper.py  # Scraper für Übel & Gefährlich
│   └── main.py              # Hauptskript zum Starten aller Scraper
├── UI/                      # Frontend-Dateien
│   ├── assets/              # Bilder und Videos
│   │   ├── image/           # Bilderordner
│   │   └── video/           # Videosordner
│   ├── index.html           # Hauptseite des Frontends
│   ├── script.js            # JavaScript-Funktionen fürs Frontend
│   └── style.css            # CSS-Styling fürs Frontend
├── all_events.json          # Gespeicherte Event-Daten (JSON)
├── env.json                 # Umgebungsvariablen (z. B. Supabase API-Schlüssel)
└── README.md                # Dokumentation des Projekts
```

## 🔍 Datenquellen

| Quelle               | Methode        | Update-Intervall |
|----------------------|----------------|-------------------|
| Docks.de             | Selenium       | Täglich           |
| Übel und Gefährlich  | Selenium       | Täglich           |
| HH gegen Rechts      | Selenium       | Täglich           |

## 📅 Scrum Prozess

**Teamrollen:**
- Product Owner: Tim
- Scrum Master: Lykka, Zoe, Luc (Im Wechsel)
- Entwicklungsteam: Tim, Lykka, Zoe, Luc

**Sprint-Zyklus:**
- Sprint Planning: 10:00 Uhr
- Daily Standup: Täglich 10:00 Uhr (Discord)
- Sprint Review & Retro: Zum Wechsel

**Tools:**
- GitHub Projects für Task Management.
- Google Docs für Dokumentation.

## 📈 Nächste Schritte

1. Optimierung der Scraping-Skripte:
    - Fehlerbehandlung verbessern.
    - Performance optimieren.
2. Integration von Supabase:
    - Automatische Speicherung der Daten in PostgreSQL.
3. Erweiterung des Frontends:
    - Filteroptionen hinzufügen (z. B. nach Datum oder Kategorie).
4. CI/CD einrichten:
    - Automatisierte Tests und Deployments mit GitHub Actions.

## 💡 Erweiterungsideen

1. Hinzufügen weiterer Datenquellen:
    - Eventbrite API oder Stadt Hamburg Open Data.
2. Benutzerprofile:
    - Personalisierte Event-Empfehlungen basierend auf Interessen.
3. Mobile App:
    - React Native oder Flutter App zur mobilen Nutzung.

## 👥 Mitwirkende

| Name  | Rolle                    |
|-------|--------------------------|
| Tim   | Backend                  |
| Lykka | UX/UI Design             |
| Zoe   | Frontend Entwicklung     |
| Luc   | Datenintegration & DevOps|

Wir freuen uns über Beiträge! Bitte lesen Sie die [CONTRIBUTING.md](CONTRIBUTING.md) Datei, um mehr über den Beitragprozess zu erfahren.

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die [LICENSE](LICENSE) Datei für Details.

---

Erstellt mit ❤️ in Hamburg.

