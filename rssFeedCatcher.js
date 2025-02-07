const { DOMParser } = require('xmldom'); // Verwenden Sie xmldom für XML-Parsing
const fetch = require('node-fetch'); // Importieren Sie node-fetch für fetch

const feedUrls = [
    'https://investor.eventbrite.com/rss/pressrelease.aspx',
    'https://www.rss-verzeichnis.de/freizeit-unterhaltung-und-bekleidung/veranstaltungen/118330-eventpicker-veranstaltungen-im-umkreis-finden',
    'https://www.eventbrite.com/', // ACHTUNG: Ist keine RSS-URL
    'https://feedfry.com/rss/11efe4785bf85274aca3d8f330f65163'
];

async function fetchRssFeed(url) {
    try {
        const response = await fetch(url);
        const text = await response.text();

        // Prüfen, ob es sich um HTML handelt (eventbrite.com liefert HTML)
        if (url === 'https://www.eventbrite.com/') {
            console.warn("Eventbrite.com ist keine RSS-Feed-URL. Überspringe...");
            return [];
        }

        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(text, 'text/xml'); // text/xml erzwingen
        const items = xmlDoc.getElementsByTagName('item'); // getElementsByTagName nutzen
        return Array.from(items).map(item => ({
            title: item.getElementsByTagName('title')[0]?.textContent || 'Kein Titel', // getElementsByTagName nutzen
            link: item.getElementsByTagName('link')[0]?.textContent || 'Kein Link', // getElementsByTagName nutzen
            pubDate: item.getElementsByTagName('pubDate')[0]?.textContent || 'Kein Datum' // getElementsByTagName nutzen
        }));
    } catch (error) {
        console.error(`Fehler beim Abrufen von ${url}:`, error);
        return [];
    }
}

async function fetchAllFeeds() {
    const results = await Promise.all(feedUrls.map(url => fetchRssFeed(url)));
    const flatResults = results.flat();
    console.table(flatResults);
}

fetchAllFeeds();
