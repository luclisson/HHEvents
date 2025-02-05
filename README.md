# HHEvents

# Hamburg Events Hub

[![CI Pipeline](https://github.com/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-repo/actions)

## 🚀 Getting Started

7. **Umgebung einrichten:**
```
cp .env.example .env
docker-compose up -d
```

8. **Datenpipeline starten:**
```
# Scrapy Spider ausführen
cd packages/scraping
scrapy crawl eventbrite -O events.json
```

## 🛠️ Tech Stack
- Frontend: Next.js 14, TypeScript, MapLibre
- Backend: Node.js, PostgreSQL, Redis
- DevOps: Docker, GitHub Actions

## 📅 Scrum Prozess
- Sprint Planning: Montag 10:00
- Daily Standup: Täglich 15:00
- Sprint Review: Freitag 12:00

## 🔍 Datenquellen
| Quelle               | Methode        | Update-Intervall |
|----------------------|----------------|-------------------|
| Eventbrite           | Scrapy + API   | Stündlich         |
| Konzerte.de          | Puppeteer      | Täglich           |
| Stadt Hamburg Open Data | API       | Wöchentlich       |

## 📈 Nächste Schritte
- [ ] CI/CD Pipeline einrichten
- [ ] Sentry für Error Tracking
- [ ] i18n für internationale Nutzer
```

## 💡 Erweiterungsideen
- KI-basierte Personalisierung (Apache PredictionIO)
- Ticket-Preisvergleich mit Web Scraping
- Realtime Demo-Tracking über Twitter API
- Barrierefreiheits-Check für Locations
- Event-Empfehlungssystem (kollaboratives Filtern)

Bei konkreten Fragen zur Implementierung einzelner Komponenten oder Anpassungen an eure speziellen Anforderungen stehe ich gerne für weitere Details zur Verfügung! 🚀

Citations:
[1] https://rossum.ai/blog/best-data-extraction-tools/
[2] https://multilogin.com/blog/web-scraping-techniques/
[3] https://atlan.com/data-pipeline-architecture/
[4] https://legacy.reactjs.org/docs/faq-structure.html
[5] https://5ly.co/blog/best-web-app-tech-stack/
[6] https://www.joshwcomeau.com/react/file-structure/
[7] https://www.launchnotes.com/blog/how-to-implement-scrum-a-step-by-step-guide
[8] https://thedigitalprojectmanager.com/projects/pm-methodology/scrum-methodology-complete-guide/
[9] https://www.cisin.com/coffee-break/awesome-tips-to-use-agile-scrum-methodology-in-web-development.html
[10] https://airbyte.com/top-etl-tools-for-sources/top-data-extraction-tools
[11] https://www.matillion.com/learn/blog/how-to-build-a-data-pipeline
[12] https://www.aha.io/roadmapping/guide/agile/how-to-implement-scrum
[13] https://zistemo.com/blog/key-strategies-for-effective-scrumming-project-management/
[14] https://steps.tn/how-to-use-scrum-in-web-development/
[15] https://learn.microsoft.com/en-us/data-engineering/playbook/articles/pipeline-reliability
[16] https://apify.com
[17] https://www.promptcloud.com/blog/the-ultimate-guide-to-web-scraping-tools-techniques-and-use-cases/
[18] https://www.ascend.io/blog/data-pipeline-best-practices/
[19] https://www.projectpro.io/article/data-pipeline-tools/946
[20] https://www.imperva.com/learn/application-security/data-scraping/
[21] https://airbyte.com/data-engineering-resources/data-pipeline-architecture
[22] https://www.lokad.com/data-extraction-pipeline/
[23] https://en.wikipedia.org/wiki/Web_scraper
[24] https://www.montecarlodata.com/blog-data-engineering-pipeline-guide/
[25] https://forage.ai/web-data-extraction-services/
[26] https://www.octoparse.com/blog/introduction-to-web-scraping-techniques-and-tools
[27] https://www.youtube.com/watch?v=_bIJoOriBxA
[28] https://www.developerway.com/posts/react-project-structure
[29] https://www.reddit.com/r/reactjs/comments/153vjsf/react_folder_structure_best_practice_s/
[30] https://www.reddit.com/r/programming/comments/1f9v0mk/best_tech_stack_for_web_development_in_2025/
[31] https://www.reddit.com/r/react/comments/123tobn/what_are_some_good_ways_to_structure_react/
[32] https://blog.webdevsimplified.com/2022-07/react-folder-structure/
[33] https://medium.com/codex/my-2025-tech-stack-tools-tech-im-using-this-year-ca06af68b8da
[34] https://www.youtube.com/watch?v=8n_uPCQS0lM
[35] https://www.robinwieruch.de/react-tech-stack/
[36] https://maxrozen.com/guidelines-improve-react-app-folder-structure
[37] https://www.nobledesktop.com/classes-near-me/blog/best-web-development-stacks
[38] https://scrimba.com/articles/react-project-structure/
[39] https://www.index.dev/blog/essential-tools-full-stack-development
[40] https://www.huptechweb.com/agile-scrum-for-web-development/
[41] https://fabrity.com/blog/how-to-implement-scrum-in-10-steps/
[42] https://www.planview.com/resources/guide/what-is-scrum/scrum-best-practices-teams/
[43] https://www.scrum.org/resources/blog/working-web-development-company-using-scrum
[44] https://www.forecast.app/blog/implementation-of-scrum-7-steps
[45] https://www.altexsoft.com/whitepapers/agile-project-management-best-practices-and-methodologies/
[46] https://de.linkedin.com/advice/3/how-can-you-use-scrum-front-end-development-skills-web-development-udiwf?lang=de
[47] https://www.atlassian.com/agile/scrum
[48] https://www.scrum.org/resources/agile-project-management-scrum-developer-best-practices
[49] https://www.brightlabs.com.au/insights/scrum-methodology-in-web-development
[50] https://www.nimblework.com/agile/scrum-methodology/
[51] https://learn.microsoft.com/en-us/azure/devops/boards/best-practices-agile-project-management?view=azure-devops
[52] https://www.promptcloud.com/blog/what-is-data-scraping-techniques-tools-and-use-cases/
[53] https://www.integrate.io/blog/data-extraction-tools/
[54] https://research.aimultiple.com/scraping-techniques/
[55] https://www.robinwieruch.de/react-folder-structure/
[56] https://www.imaginarycloud.com/blog/tech-stack-software-development
[57] https://dev.to/itswillt/folder-structures-in-react-projects-3dp8
[58] https://dev.to/rayenmabrouk/best-tech-stack-for-startups-in-2025-5h2l
[59] https://www.projektron.de/en/blog/details/scrum-software-development-3592/
[60] https://www.knowledgehut.com/blog/agile/great-scrum-master-tips-best-practices
