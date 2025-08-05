// Utility: get a cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// Utility: set cookie
function setCookie(name, value, days=1) {
  const d = new Date();
  d.setTime(d.getTime() + (days*24*60*60*1000));
  document.cookie = `${name}=${value}; expires=${d.toUTCString()}; path=/`;
}

// Utility: delete cookie
function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

// ---------------------------
// SHOW LOGIN/LOGOUT BUTTON LOGIC (GLOBAL)
// ---------------------------
function showAuthLinks() {
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  const token = getCookie('token');
  if (loginLink && logoutLink) {
    if (token) {
      loginLink.style.display = 'none';
      logoutLink.style.display = 'inline-block';
    } else {
      loginLink.style.display = 'inline-block';
      logoutLink.style.display = 'none';
    }
  }
}

// Run on every page load
document.addEventListener('DOMContentLoaded', () => {
  showAuthLinks();

  // ---------------------------
  // LOGOUT LOGIC
  // ---------------------------
  const logoutLink = document.getElementById('logout-link');
  if (logoutLink) {
    logoutLink.addEventListener('click', (e) => {
      e.preventDefault();
      deleteCookie('token');
      showAuthLinks();
      window.location.href = 'login.html';
    });
  }

  // ---------------------------
  // LOGIN LOGIC
  // ---------------------------
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const errorDiv = document.getElementById('login-error');
      errorDiv.textContent = "";
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          setCookie('token', data.access_token);
          showAuthLinks();
          window.location.href = 'index.html';
        } else {
          const err = await response.json();
          errorDiv.textContent = 'Login failed: ' + (err.msg || response.statusText);
        }
      } catch (error) {
        errorDiv.textContent = 'Login failed: ' + error.message;
      }
    });
    return;
  }

  // ---------------------------
  // SIGNUP PAGE
  // ---------------------------
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const errorDiv = document.getElementById('signup-error');
      const successDiv = document.getElementById('signup-success');
      errorDiv.textContent = "";
      successDiv.textContent = "";

      const firstName = document.getElementById('first-name').value.trim();
      const lastName = document.getElementById('last-name').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirm-password').value;

      if (password !== confirmPassword) {
        errorDiv.style.color = "red";
        errorDiv.textContent = "Passwords do not match.";
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/users/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            first_name: firstName, last_name: lastName, email, password
          })
        });

        if (response.ok) {
          successDiv.style.color = "green";
          successDiv.textContent = "Account created! You can now log in.";
          signupForm.reset();
        } else {
          const err = await response.json();
          errorDiv.style.color = "red";
          errorDiv.textContent = 'Signup failed: ' + (err.msg || response.statusText);
        }
      } catch (error) {
        errorDiv.style.color = "red";
        errorDiv.textContent = 'Signup failed: ' + error.message;
      }
    });
    return;
  }

  // ---------------------------
  // INDEX PAGE (PLACES LIST)
  // ---------------------------
  if (document.getElementById('places-list')) {
    fetch('http://127.0.0.1:5000/api/v1/places/')
      .then(response => response.json())
      .then(places => {
        displayPlaces(places);

        // Setup price filter
        const priceSelect = document.getElementById('max-price');
        priceSelect.addEventListener('change', () => {
          const selected = priceSelect.value;
          let filtered = places;
          if (selected !== 'All') {
            const max = parseFloat(selected);
            filtered = places.filter(place => place.price <= max);
          }
          displayPlaces(filtered);
        });
      })
      .catch(error => {
        document.getElementById('places-list').innerHTML = `<p>Error loading places: ${error.message}</p>`;
      });
    return;
  }

  // ---------------------------
  // PLACE DETAILS PAGE
  // ---------------------------
  if (document.getElementById('place-details')) {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    showAuthLinks();

    // PATCH: If placeId is missing, show error and stop.
    if (!placeId) {
      document.getElementById('place-details').innerHTML = '<p>Error: No place selected. Please use a valid link to this page.</p>';
      return;
    }

    fetchPlaceDetails(token, placeId);

    // Add review logic
    const reviewFormSection = document.getElementById('review-form');
    if (token && reviewFormSection) {
      reviewFormSection.style.display = 'block';
      setupReviewForm(token, placeId);
    } else if (reviewFormSection) {
      reviewFormSection.style.display = 'none';
    }
    return;
  }

  // ---------------------------
  // ADMIN DASHBOARD
  // ---------------------------
  if (document.getElementById('amenities-list')) {
    const token = getCookie('token');
    if (!token) window.location.href = 'login.html';

    // Fetch amenities
    async function fetchAmenities() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/amenities/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const amenities = await response.json();
          displayAmenities(amenities);
        }
      } catch (error) {}
    }

    function displayAmenities(amenities) {
      const list = document.getElementById('amenities-list');
      list.innerHTML = '';
      amenities.forEach(amenity => {
        const li = document.createElement('li');
        li.innerHTML = `
          <strong>${amenity.name}</strong> - ${amenity.description || ''}
          <button class="details-button" onclick="deleteAmenity('${amenity.id}')">Delete</button>
        `;
        list.appendChild(li);
      });
    }

    window.deleteAmenity = async function (amenityId) {
      const token = getCookie('token');
      if (!token) return;
      try {
        const resp = await fetch(`http://127.0.0.1:5000/api/v1/amenities/${amenityId}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (resp.ok) {
          fetchAmenities();
        }
      } catch (error) {}
    };

    const addAmenityForm = document.getElementById('add-amenity-form');
    const adminMsg = document.getElementById('admin-message');
    addAmenityForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      adminMsg.textContent = '';
      const token = getCookie('token');
      if (!token) return;
      const name = document.getElementById('amenity-name').value;
      const desc = document.getElementById('amenity-desc').value;
      try {
        const resp = await fetch('http://127.0.0.1:5000/api/v1/amenities/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ name, description: desc })
        });
        if (resp.ok) {
          addAmenityForm.reset();
          adminMsg.style.color = "green";
          adminMsg.textContent = "Amenity added!";
          fetchAmenities();
        } else {
          const err = await resp.json();
          adminMsg.style.color = "red";
          adminMsg.textContent = err.msg || "Error adding amenity";
        }
      } catch (error) {
        adminMsg.style.color = "red";
        adminMsg.textContent = error.message;
      }
    });

    fetchAmenities();
    return;
  }
});

// ---------------------------
// Helper: Get place ID from URL params
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// --- Place rendering and price filter for index.html ---

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';
  if (!places.length) {
    placesList.innerHTML = '<p>No places found.</p>';
    return;
  }
  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.innerHTML = `
      <h2>${place.name}</h2>
      <div class="place-desc">${place.description ? place.description.slice(0,80) + (place.description.length>80 ? "..." : "") : ""}</div>
      <p>Location: ${place.location || 'Unknown'}</p>
      <p>Price per night: $${place.price || 0}</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
    `;
    placesList.appendChild(card);
  });
}

// ---------------------------
// Fetch place details
async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });
    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
      displayReviews(place.reviews || []);
    } else {
      document.getElementById('place-details').innerHTML = '<p>Error loading place details.</p>';
    }
  } catch (error) {
    document.getElementById('place-details').innerHTML = `<p>Error: ${error.message}</p>`;
  }
}

// Render place details
function displayPlaceDetails(place) {
  if (document.getElementById('place-title')) {
    document.getElementById('place-title').textContent = place.name;
  }
  const detailsDiv = document.getElementById('place-details');
  detailsDiv.innerHTML = `
    <p><strong>Host:</strong> ${place.host || 'N/A'}</p>
    <p><strong>Location:</strong> ${place.location || place.city || place.address || 'Unknown'}</p>
    <p><strong>Country:</strong> ${place.country || 'Unknown'}</p>
    <p><strong>Price per night:</strong> $${place.price || place.price_per_night || 0}</p>
    <p><strong>Description:</strong> ${place.description || ''}</p>
    <p><strong>Amenities:</strong> ${Array.isArray(place.amenities) ? place.amenities.join(', ') : (place.amenities || '')}</p>
  `;
}

// Render reviews
function displayReviews(reviews) {
  const reviewsDiv = document.getElementById('reviews-list');
  if (!reviewsDiv) return;
  reviewsDiv.innerHTML = '';
  if (!reviews.length) {
    reviewsDiv.innerHTML = '<p>No reviews yet.</p>';
    return;
  }
  reviews.forEach(review => {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `
      <strong>${review.user_name || 'Anonymous'}:</strong>
      <p>${review.text || review.comment}</p>
      <p>Rating: ${renderStars(review.rating)}</p>
    `;
    reviewsDiv.appendChild(card);
  });
}

// Render stars for rating (e.g., ★★★☆☆)
function renderStars(rating) {
  rating = Number(rating) || 0;
  let stars = '';
  for (let i = 1; i <= 5; i++) {
    stars += i <= rating ? '★' : '☆';
  }
  return stars;
}

// Setup review form on place.html
function setupReviewForm(token, placeId) {
  const reviewForm = document.getElementById('review-form');
  const messageDiv = document.getElementById('review-message');
  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    messageDiv.textContent = "";
    const comment = document.getElementById('comment').value;
    const rating = document.getElementById('rating').value;
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ text: comment, rating })
      });
      if (response.ok) {
        reviewForm.reset();
        messageDiv.style.color = "green";
        messageDiv.textContent = "Review submitted successfully!";
        fetchPlaceDetails(token, placeId); // refresh reviews
      } else {
        const err = await response.json();
        messageDiv.style.color = "red";
        messageDiv.textContent = (err.msg || "Failed to submit review");
      }
    } catch (error) {
      messageDiv.style.color = "red";
      messageDiv.textContent = error.message;
    }
  });
}
