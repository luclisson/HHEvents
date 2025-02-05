# Hamburg Events Hub

![Hamburg Skyline](https://example.com/hamburg-skyline.jpg)

[![CI Pipeline](https://github.com/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-repo/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

Hamburg Events Hub ist eine zentrale Plattform, die alle Events in Hamburg an einem Ort zusammenführt. Unser Ziel ist es, Hamburgern und Besuchern einen umfassenden Überblick über das vielfältige Veranstaltungsangebot der Stadt zu bieten.

## 🎉 Features

- Aggregation von Events aus verschiedenen Quellen (Eventbrite, Tunnel.de, Übel und Gefährlich, etc.)
- Interaktive Karte mit Event-Locations
- Filtermöglichkeiten nach Datum, Kategorie und Entfernung
- Personalisierte Event-Empfehlungen
- Echtzeit-Updates für spontane Veranstaltungen

## 🛠️ Tech Stack

### Frontend:
- Next.js 14 (React)
- TypeScript
- Zustand für State Management
- MapLibre GL JS für Kartendarstellung
- Shadcn UI für UI-Komponenten
- Framer Motion für Animationen

### Backend:
- Node.js mit Express
- PostgreSQL + PostGIS für Geodaten
- Redis für Caching
- Strapi CMS für manuelle Event-Einträge
- Elasticsearch für Suchfunktionalität

### DevOps:
- Docker & Docker Compose
- GitHub Actions für CI/CD

## 🚀 Getting Started

1. **Repository klonen:**
git clone https://github.com/your-repo/hamburg-events-hub.git
cd hamburg-events-hub


2. **Umgebungsvariablen einrichten:**
cp .env.example .env

Fülle die notwendigen Werte in der `.env` Datei aus.

3. **Docker-Container starten:**
docker-compose up -d


4. **Abhängigkeiten installieren und Entwicklungsserver starten:**

npm install
npm run dev


5. **Datenpipeline starten:**
cd packages/scraping
scrapy crawl eventbrite -O events.json

## 📂 Projektstruktur
hamburg-events/
├── apps/
│ ├── frontend/ # Next.js App
│ │ ├── src/
│ │ │ ├── features/
│ │ │ ├── lib/
│ │ │ └── styles/
│ └── backend/ # Express API
├── packages/
│ ├── database/ # Prisma Schema
│ ├── scraping/ # Scrapy Spiders
│ └── cms/ # Strapi Customizations
├── infrastructure/
│ ├── docker/
│ └── terraform/
└── README.md



## 🔍 Datenquellen

| Quelle               | Methode        | Update-Intervall |
|----------------------|----------------|-------------------|
| Eventbrite           | Scrapy + API   | Stündlich         |
| Tunnel.de            | Puppeteer      | Täglich           |
| Übel und Gefährlich  | API            | Täglich           |
| Stadt Hamburg Open Data | API         | Wöchentlich       |

## 📅 Scrum Prozess

- **Product Owner:** Lykka
- **Scrum Master:** Tim
- **Entwicklungsteam:** Zoe, Luc

**Sprint-Zyklus:**
- Sprint Planning: Montag 10:00 Uhr
- Daily Standup: Täglich 15:00 Uhr
- Sprint Review: Freitag 12:00 Uhr
- Sprint-Länge: 2 Wochen

**Tools:**
- Jira für Backlog Management
- FigJam für Retrospektiven
- GitHub Projects für Task Tracking

## 📈 Nächste Schritte

- [ ] CI/CD Pipeline einrichten
- [ ] Sentry für Error Tracking implementieren
- [ ] i18n für internationale Nutzer einführen
- [ ] Performance-Optimierung für mobile Endgeräte
- [ ] Benutzer-Authentifizierung und Profilerstellung

## 💡 Erweiterungsideen

- KI-basierte Personalisierung mit Apache PredictionIO
- Ticket-Preisvergleich mit Web Scraping
- Realtime Demo-Tracking über Twitter API
- Barrierefreiheits-Check für Locations
- Event-Empfehlungssystem basierend auf kollaborativem Filtern

## 👥 Mitwirkende

- Tim - Scrum Master & Backend-Entwicklung
- Lykka - Product Owner & UX Design
- Zoe - Frontend-Entwicklung
- Luc - Datenintegration & DevOps

Wir freuen uns über Beiträge! Bitte lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md) für Details zu unserem Code of Conduct und dem Prozess für das Einreichen von Pull Requests.

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Details finden Sie in der [LICENSE](LICENSE) Datei.

---

Erstellt mit ❤️ in Hamburg




