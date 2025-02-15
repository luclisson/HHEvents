document.addEventListener('DOMContentLoaded', () => {
    // Referenzen auf wichtige HTML-Elemente
    const splashScreen = document.querySelector('.splash-screen'); // Splash-Screen-Element
    const mainContent = document.querySelector('.main-content');  // Hauptinhalt der Seite
    const video = document.getElementById('intro-video');         // Video im Splash-Screen
    const eventContainer = document.getElementById('event-container'); // Container für Event-Kacheln

    // Versteckt den Splash-Screen, wenn das Video endet
    video.onended = () => {
        splashScreen.style.opacity = '0'; // Sanftes Ausblenden
        setTimeout(() => {
            splashScreen.classList.add('hidden'); // Vollständiges Entfernen des Splash-Screens
            mainContent.classList.remove('hidden'); // Hauptinhalt anzeigen
        }, 500); // Zeit für den Übergang (CSS-Transition)
    };
    
    // Öffnet oder schließt Details in Event-Kacheln bei Klick
    eventContainer.addEventListener('click', function(e) {
        const tile = e.target.closest('.event-tile'); // Findet die angeklickte Kachel
        if (tile) {
            tile.classList.toggle('active'); // Aktiviert/Deaktiviert die Kachel
            const details = tile.querySelector('.event-details');
            if (details) {
                details.style.maxHeight = tile.classList.contains('active') 
                    ? `${details.scrollHeight}px`  // Zeigt Details an (Höhe dynamisch)
                    : null;                         // Versteckt Details (Höhe zurücksetzen)
            }
        }
    });

    // Filtert Events nach Kategorie bei Klick auf einen Filter-Button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelector('.filter-btn.active').classList.remove('active'); // Entfernt aktive Klasse vom vorherigen Button
            this.classList.add('active'); // Aktiviert den aktuellen Button
            filterEvents(this.dataset.category); // Filtert Events basierend auf der Kategorie
        });
    });

    // Generiert Events beim Laden der Seite
    generateEvents(); // Erstellt Events basierend auf API-Daten

    /**
     * Fetches events from the API and adds them to the event container.
     */
    async function generateEvents() {
        try {
            const response = await fetch('http://localhost:3000/fetchData');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            data.forEach((event, i) => {
                console.log(event)
                const tile = document.createElement('div'); // Erstellt eine neue Event-Kachel
                tile.className = 'event-tile';
                const category = event.category;
                tile.dataset.category = category.toLowerCase(); // Speichert die Kategorie für die Filterung
                console.log(event.img_url)
                tile.innerHTML = `
                    <div class="event-header">
                        <span class="event-category">${category}</span>
                        ${i % 5 === 0 ? '<div class="featured-badge">Featured</div>' : ''} <!-- Markiert jedes 5. Event -->
                        <h3 class="event-title">${event.title}</h3>
                        <time class="event-date">${event.fetchdata[0].date} at ${event.fetchdata[0].time} o'clock</time>
                    </div>
                    <div class="event-details">
                        <div class="detail-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <span class="event-location">${event.location}</span>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-tag"></i>
                            <span class="event-price">Ab ${event.fetchdata[0].price}€</span>
                        </div>
                        <div class="expandable-details">
                            <p>${event.description}</p>
                            
                            <a href="${event.link}" class="event-link-button">original source</a>
                            <img src="${event.img_url}" alt="event picture" width="200" height="200">

                            <button class="more-info">view less</button>
                        </div>
                    </div>
                `;
                eventContainer.appendChild(tile); // Fügt die Kachel in den Container ein
            });
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    }

    /**
     * Filtert Events basierend auf der ausgewählten Kategorie.
     * @param {string} category - Die Kategorie, nach der gefiltert werden soll.
     */
    function filterEvents(category) {
        document.querySelectorAll('.event-tile').forEach(tile => {
            tile.style.display = category === 'alle' || tile.dataset.category === category 
                ? 'block'   // Zeigt Kachel an, wenn sie zur Kategorie passt oder "Alle" gewählt ist
                : 'none';   // Versteckt Kachel sonst
        });
    }
});