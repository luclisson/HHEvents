document.addEventListener('DOMContentLoaded', () => {
    // Elementreferenzen
    const splashScreen = document.querySelector('.splash-screen');
    const mainContent = document.querySelector('.main-content');
    const video = document.getElementById('intro-video');
    const eventContainer = document.getElementById('event-container');

    // Splashscreen-Animation
    video.onended = () => {
        splashScreen.style.opacity = '0';
        setTimeout(() => {
            splashScreen.classList.add('hidden');
            mainContent.classList.remove('hidden');
        }, 500);
    };

    // Event-Detailanzeige
    eventContainer.addEventListener('click', function(e) {
        const tile = e.target.closest('.event-tile');
        if (tile) {
            tile.classList.toggle('active');
            const details = tile.querySelector('.event-details');
            if (details) {
                details.style.maxWidth = tile.classList.contains('active') 
                    ? '100%' 
                    : '0';
            }
        }
    });

    // Filterlogik
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelector('.filter-btn.active').classList.remove('active');
            this.classList.add('active');
            filterEvents(this.dataset.category);
        });
    });

    // Eventgenerierung
    async function generateEvents() {
        try {
            const response = await fetch('http://localhost:3000/fetchData');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            console.log(data)
            console.log(`length: ${data.length}`)
            let counter = 1;
            data.forEach(event => {
                if(typeof(event)!= 'string'){
                    console.log(`counter: ${counter}`)
                counter++;
                const tile = document.createElement('div');
                tile.className = 'event-tile';
                
                // Kategorien-Mapping
                try{
                    const originalCategories = event.category.split(',')
                    .map(c => c.trim().toLowerCase());
                
                const mappedCategories = new Set();
                
                originalCategories.forEach(cat => {
                    if (cat === 'konzert') {
                        mappedCategories.add('konzert');
                    } else if (['club event', 'party'].includes(cat)) {
                        mappedCategories.add('party');
                    } else if (cat === 'demonstration') {
                        mappedCategories.add('demonstration');
                    } else if ([
                        'workshop', 
                        'podiumsgespräch', 
                        'fortbildung', 
                        'kundgebung', 
                        'lesung'
                    ].includes(cat)) {
                        mappedCategories.add('demokratie');
                    }
                });
                
                tile.dataset.category = Array.from(mappedCategories).join(' ');
                }catch(error){
                    console.error('error with category', error)
                }
                

                tile.innerHTML = `
                    <div class="event-header">
                        <span class="event-category">${event.category}</span>
                        <h3 class="event-title">${event.title}</h3>
                        <time class="event-date">${event.fetchdata[0].date} um ${event.fetchdata[0].time} Uhr</time>
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
                            <a href="${event.link}" class="event-link-button">Link zum Event</a>
                            <img src="${event.img_url}" alt="Event-Bild">
                            <button class="more-info">Weniger anzeigen</button>
                        </div>
                    </div>
                `;
                eventContainer.appendChild(tile);
                }
                
            });
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    }

    // Filterfunktion
    function filterEvents(selectedCategory) {
        document.querySelectorAll('.event-tile').forEach(tile => {
            const categories = tile.dataset.category.split(' ');
            const showTile = selectedCategory === 'alle' || categories.includes(selectedCategory);
            tile.style.display = showTile ? 'block' : 'none';
        });
    }

    // Initialisierung
    generateEvents();
});
