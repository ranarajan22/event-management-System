let currentIndex = 0;

function showSlides() {
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;

    // Move to the next slide
    currentIndex++;
    if (currentIndex >= totalSlides) {
        currentIndex = 0;
    }

    // Calculate the offset for sliding effect
    const offset = -currentIndex * 100; // Each slide is 100% width
    const slidesContainer = document.querySelector('.slides');
    slidesContainer.style.transform = `translateX(${offset}%)`;
}

// Show the first slide initially
document.addEventListener('DOMContentLoaded', () => {
    showSlides();
    setInterval(showSlides, 3000); // Change slide every 3 seconds
});


function moveSlides(direction) {
    const slides = document.querySelector('.events-cards');
    const totalSlides = document.querySelectorAll('.event').length;
    const slideWidth = document.querySelector('.event').offsetWidth;

    // Update current index based on direction
    currentIndex += direction;

    // Loop back to the start or end
    if (currentIndex < 0) {
        currentIndex = totalSlides - 1; // Go to last slide
    } else if (currentIndex >= totalSlides) {
        currentIndex = 0; // Go to first slide
    }

    // Calculate the offset for sliding effect
    const offset = -currentIndex * slideWidth;
    slides.style.transform = `translateX(${offset}px)`;
}
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}
//toggle profile
function toggleProfile() {
    var profileDropdown = document.getElementById("profile-dropdown");
    if (profileDropdown.style.display === "none" || profileDropdown.style.display === "") {
        profileDropdown.style.display = "block";
    } else {
        profileDropdown.style.display = "none";
    }
}

// Optional: Hide dropdown if clicked outside
window.onclick = function(event) {
    var profileDropdown = document.getElementById("profile-dropdown");
    if (event.target.id !== "profile-link" && !profileDropdown.contains(event.target)) {
        profileDropdown.style.display = "none";
    }
};