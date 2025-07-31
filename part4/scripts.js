// Change this to your actual API base URL
const API_BASE_URL = "https://your-api-url";

// Helper: Get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Helper: Set cookie
function setCookie(name, value, days = 1) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = `${name}=${value || ""}${expires}; path=/`;
}

// Helper: Parse query parameter from URL
function getQueryParam(key) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(key);
}

// ---- LOGIN PAGE ----
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = loginForm.elements['email'].value;
            const password = loginForm.elements['password'].value;
            try {
                const response = await fetch(`${API_BASE_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                if (response.ok) {
                    const data = await response.json();
                    setCookie("token", data.access_token, 1);
                    window.location.href = "index.html";
                } else {
                    const errorDiv = document.getElementById('login-error');
                    errorDiv.textContent = "Login failed: " + (await response.text());
                }
            } catch (e) {
                const errorDiv = document.getElementById('login-error');
                errorDiv.textContent = "Login error. Please try again.";
            }
        });
    }
});

// ---- INDEX PAGE ----
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('places-list')) {
        const loginLink = document.getElementById('login-link');
        const token = getCookie('token');

        if (!token) {
            if (loginLink) loginLink.style.display = 'inline-block';
        } else {
            if (loginLink) loginLink.style.display = 'none';
        }

        fetchPlaces();

        document.getElementById('price-filter').addEventListener('change', filterPlaces);
    }
});

let placesCache = [];

async function fetchPlaces() {
    const token = getCookie('token');
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const places = await response.json();
            placesCache = places;
            displayPlaces(places);
        } else {
            document.getElementById('places-list').textContent = "Failed to fetch places.";
        }
    } catch {
        document.getElementById('places-list').textContent = "Error fetching places.";
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = "";
    places.forEach(place => {
        const card = document.createElement('div');
        card.className = "place-card";
        card.innerHTML = `
            <div>
                <strong>${place.name}</strong><br>
                $${place.price_per_night} per night
            </div>
            <button class="details-button" onclick="window.location='place.html?id=${place.id}'">View Details</button>
        `;
        card.setAttribute('data-price', place.price_per_night);
        container.appendChild(card);
    });
}

function filterPlaces() {
    const price = document.getElementById('price-filter').value;
    Array.from(document.querySelectorAll('.place-card')).forEach(card => {
        const cardPrice = parseFloat(card.getAttribute('data-price'));
        if (price === "all" || cardPrice <= parseFloat(price)) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });
}

// ---- PLACE DETAILS PAGE ----
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('place-details')) {
        const addReviewSection = document.getElementById('add-review');
        const loginLink = document.getElementById('login-link');
        const token = getCookie('token');
        if (!token) {
            if (loginLink) loginLink.style.display = 'inline-block';
            if (addReviewSection) addReviewSection.style.display = 'none';
        } else {
            if (loginLink) loginLink.style.display = 'none';
            if (addReviewSection) addReviewSection.style.display = 'block';
        }
        const placeId = getQueryParam('id');
        fetchPlaceDetails(placeId);

        // Add review redirect
        const addReviewLink = document.getElementById('add-review-link');
        if (addReviewLink) {
            addReviewLink.addEventListener('click', (e) => {
                e.preventDefault();
                window.location = `add_review.html?id=${placeId}`;
            });
        }
    }
});

async function fetchPlaceDetails(placeId) {
    const token = getCookie('token');
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            document.getElementById('place-details').textContent = "Failed to fetch place details.";
        }
    } catch {
        document.getElementById('place-details').textContent = "Error loading place details.";
    }
}

function displayPlaceDetails(place) {
    const details = document.getElementById('place-details');
    details.innerHTML = `
        <div class="place-details">
            <h2>${place.name}</h2>
            <div class="place-info">Host: ${place.host_name} | $${place.price_per_night} per night</div>
            <div class="place-info">${place.description}</div>
            <div class="place-info">Amenities: ${place.amenities.join(', ')}</div>
            <h3>Reviews</h3>
            <div id="reviews-list"></div>
        </div>
    `;
    const reviewsList = details.querySelector('#reviews-list');
    if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {
            const r = document.createElement('div');
            r.className = "review-card";
            r.innerHTML = `<strong>${review.user_name}</strong> - Rating: ${review.rating}<br>${review.comment}`;
            reviewsList.appendChild(r);
        });
    } else {
        reviewsList.innerHTML = "<em>No reviews yet.</em>";
    }
}

// ---- ADD REVIEW PAGE ----
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = getCookie('token');
        if (!token) {
            window.location = "index.html";
            return;
        }
        const placeId = getQueryParam('id');
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const comment = reviewForm.elements['review'].value;
            const rating = reviewForm.elements['rating'].value;
            try {
                const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ comment, rating })
                });
                const msg = document.getElementById('review-message');
                if (response.ok) {
                    msg.style.color = "green";
                    msg.textContent = "Review submitted successfully!";
                    reviewForm.reset();
                } else {
                    msg.style.color = "red";
                    msg.textContent = "Failed to submit review.";
                }
            } catch {
                const msg = document.getElementById('review-message');
                msg.style.color = "red";
                msg.textContent = "Error submitting review.";
            }
        });
    }
});
