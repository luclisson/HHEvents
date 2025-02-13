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

    // Generiert Beispiel-Events beim Laden der Seite
    generateEvents(20); // Erstellt 20 Events

    /**
     * Erstellt eine bestimmte Anzahl von Events und fügt sie dem Event-Container hinzu.
     * @param {number} amount - Anzahl der zu generierenden Events.
     */
    async function generateEvents(amount) {
        const response = await fetch('http://localhost:3000/fetchData',{
        method: 'GET'
        });
        const data = await response.json();
        
        console.log(data)
        const categories = ['Musik', 'Kunst', 'Sport', 'Essen']; // Kategorien für Events
        const locations = [
            'Elbphilharmonie', 'Reeperbahn', 'Planten un Blomen',
            'HafenCity', 'Alsterpavillon', 'St. Pauli Theater'
        ]; // Veranstaltungsorte

        for (let i = 0; i < amount; i++) {
            const tile = document.createElement('div'); // Erstellt eine neue Event-Kachel
            tile.className = 'event-tile';
            const category = categories[i % categories.length];  // Rotiert durch die Kategorien
            tile.dataset.category = category.toLowerCase();      // Speichert die Kategorie für die Filterung

            tile.innerHTML = `
                <div class="event-header">
                    <span class="event-category">${category}</span>
                    ${i % 5 === 0 ? '<div class="featured-badge">Featured</div>' : ''} <!-- Markiert jedes 5. Event -->
                    <h3 class="event-title">Event #${i + 1}</h3> <!--  -->
                    <time class="event-date">${randomDate()}</time> <!-- Zufälliges Datum -->
                </div>
                <div class="event-details">
                    <div class="detail-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <span class="event-location">${locations[i % locations.length]}</span> <!-- Veranstaltungsort -->
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-tag"></i>
                        <span class="event-price">Ab ${Math.floor(Math.random() * 50) + 10}€</span> <!-- Zufälliger Preis -->
                    </div>
                    <div class="expandable-details">
                        <p>Lorem ipsum dolor sit amet...</p> <!-- Platzhaltertext -->
                        <button class="more-info">Tickets buchen</button> <!-- Buchungsbutton -->
                    </div>
                </div>
            `;
            eventContainer.appendChild(tile); // Fügt die Kachel in den Container ein
        }
    }

    /**
     * Generiert ein zufälliges Datum in den nächsten 30 Tagen.
     * @returns {string} - Formatiertes Datum im deutschen Format.
     */
    function randomDate() {
        const date = new Date();
        date.setDate(date.getDate() + Math.floor(Math.random() * 30)); // Zufälliger Tag in den nächsten 30 Tagen
        return date.toLocaleDateString('de-DE', { 
            day: '2-digit',
            month: 'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
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