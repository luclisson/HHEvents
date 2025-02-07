const { DOMParser } = require('xmldom');
const fetch = require('node-fetch');

const feedUrls = [
    'https://investor.eventbrite.com/rss/pressrelease.aspx',
    'https://www.rss-verzeichnis.de/freizeit-unterhaltung-und-bekleidung/veranstaltungen/118330-eventpicker-veranstaltungen-im-umkreis-finden',
    'https://www.eventbrite.com/',
    'https://feedfry.com/rss/11efe4785bf85274aca3d8f330f65163'
];

async function fetchRssFeed(url) {
    try {
        const response = await fetch(url);
        const contentType = response.headers.get('content-type');
        
        if (!contentType || !contentType.includes('xml')) {
            console.warn(`Skipping non-RSS URL: ${url}`);
            return [];
        }

        const text = await response.text();
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(text, 'text/xml');
        const items = xmlDoc.getElementsByTagName('item');
        
        return Array.from(items).map(item => ({
            title: item.getElementsByTagName('title')[0]?.textContent || 'No Title',
            link: item.getElementsByTagName('link')[0]?.textContent || 'No Link',
            pubDate: item.getElementsByTagName('pubDate')[0]?.textContent || 'No Date'
        }));
    } catch (error) {
        console.error(`Error fetching ${url}:`, error.message);
        return [];
    }
}

async function fetchAllFeeds() {
    const results = await Promise.all(feedUrls.map(url => fetchRssFeed(url)));
    const flatResults = results.flat();
    console.table(flatResults);
}

fetchAllFeeds();