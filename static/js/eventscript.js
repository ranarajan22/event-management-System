// Function to display events from local storage categorized
function displayEventsByCategory() {
    const eventsList = document.getElementById('eventsList');
    eventsList.innerHTML = ''; // Clear existing events

    const events = JSON.parse(localStorage.getItem('events')) || [];
    const categories = ['Workshops', 'Seminars', 'Conferences'];

    categories.forEach(category => {
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'category';
        categoryDiv.innerHTML = `<h3>${category}</h3><div class="events-container"></div>`;
        
        const eventsContainer = categoryDiv.querySelector('.events-container');

        events.forEach(event => {
            if (event.category === category) {
                const eventCard = document.createElement('div');
                eventCard.className = 'event';
                eventCard.innerHTML = `
                    <img src="/images/image1.jpeg" alt="${event.title}" class="event-image">
                    <h4>${event.title}</h4>
                    <p>Date: ${event.date}</p>
                    <p>Location: ${event.location}</p>
                    <button class="register-button">Register</button>
                `;
                eventsContainer.appendChild(eventCard);
            }
        });

        eventsList.appendChild(categoryDiv);
    });
}

// Display events on load
document.addEventListener('DOMContentLoaded', displayEventsByCategory);
function searchEvents() {
    const input = document.getElementById('searchBar').value.toLowerCase().trim();
    const eventsSection = document.getElementById('eventsSection');
    const events = eventsSection.getElementsByClassName('event');
    
    clearHighlights(events);
    
    if (input === '') {
        for (let i = 0; i < events.length; i++) {
            events[i].style.display = ''; // Show all events
        }
        return;
    }

    let foundAny = false;

    for (let i = 0; i < events.length; i++) {
        const event = events[i];
        const title = event.getElementsByTagName('h4')[0];
        const description = event.getElementsByTagName('p')[2];

        const titleText = title.innerText.toLowerCase();
        const descriptionText = description.innerText.toLowerCase();

        if (titleText.includes(input) || descriptionText.includes(input)) {
            event.style.display = ''; // Show event
            highlightMatch(title, input);
            highlightMatch(description, input);
            foundAny = true;
        } else {
            event.style.display = 'none'; // Hide event
        }
    }

    if (!foundAny) {
        alert('No events found matching your search criteria.');
    }
}

function highlightMatch(element, searchString) {
    const regex = new RegExp(`(${searchString})`, 'gi');
    element.innerHTML = element.innerHTML.replace(regex, '<span class="highlight">$1</span>');
}

function clearHighlights(events) {
    for (let i = 0; i < events.length; i++) {
        const title = events[i].getElementsByTagName('h4')[0];
        const description = events[i].getElementsByTagName('p')[2];

        title.innerHTML = title.innerHTML.replace(/<span class="highlight">(.*?)<\/span>/g, '$1');
        description.innerHTML = description.innerHTML.replace(/<span class="highlight">(.*?)<\/span>/g, '$1');
    }
}
