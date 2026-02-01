// Global variables
let map;
let markers = [];
let markerClusterGroup;
let allLocations = [];

// Initialize map on page load
document.addEventListener('DOMContentLoaded', function () {
    initMap();
    fetchLocations();
    setupEventListeners();
});

// Initialize Leaflet map
function initMap() {
    // Center map on Poland
    map = L.map('map').setView([52.0693, 19.4803], 6);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    // Initialize marker cluster group
    markerClusterGroup = L.markerClusterGroup({
        chunkedLoading: true,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        zoomToBoundsOnClick: true
    });

    map.addLayer(markerClusterGroup);
}

// Fetch locations from API
function fetchLocations() {
    updateResultsCount('Ładowanie...');

    fetch('/api/map/locations/?page_size=10000')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle DRF paginated response format
            const locations = data.results || data;
            allLocations = locations;
            displayLocations(locations);
            updateResultsCount(`Znaleziono ${locations.length} ośrodków`);
        })
        .catch(error => {
            console.error('Error fetching locations:', error);
            updateResultsCount('Błąd ładowania danych');
        });
}

// Display locations on map
function displayLocations(locations) {
    // Clear existing markers
    markerClusterGroup.clearLayers();
    markers = [];

    // Add markers for each location
    locations.forEach(location => {
        const marker = L.marker([location.lat, location.lng])
            .bindPopup(createPopupContent(location));

        markers.push(marker);
        markerClusterGroup.addLayer(marker);
    });

    // Fit map to show all markers if there are any
    if (locations.length > 0) {
        const bounds = markerClusterGroup.getBounds();
        if (bounds.isValid()) {
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    }
}

// Create popup content for marker
function createPopupContent(location) {
    const diseases = location.treatedDiseases
        .split(',')
        .map(d => d.trim())
        .filter(d => d.length > 0);

    const diseaseTags = diseases
        .map(disease => `<span class="disease-tag">${disease}</span>`)
        .join('');

    return `
        <div class="popup-header">
            ${location.department}
        </div>
        <div class="popup-body">
            <div class="popup-row">
                <div class="popup-label">Leczone choroby:</div>
                <div class="popup-diseases">
                    ${diseaseTags}
                </div>
            </div>
            <div class="popup-row">
                <div class="popup-label">Adres:</div>
                <div class="popup-value">${location.address}</div>
            </div>
            <div class="popup-row">
                <div class="popup-label">Telefon:</div>
                <div class="popup-value">${location.phone.replace(/\n/g, '<br>')}</div>
            </div>
        </div>
    `;
}

// Setup event listeners for filters
function setupEventListeners() {
    const searchInput = document.getElementById('search-input');
    const diseaseFilter = document.getElementById('disease-filter');
    const resetButton = document.getElementById('reset-filters');

    // Search input with debounce
    let searchTimeout;
    searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            applyFilters();
        }, 300);
    });

    // Disease filter
    diseaseFilter.addEventListener('change', function () {
        applyFilters();
    });

    // Reset filters button
    resetButton.addEventListener('click', function () {
        searchInput.value = '';
        diseaseFilter.value = '';
        applyFilters();
    });
}

// Apply filters to locations
function applyFilters() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase().trim();
    const diseaseFilter = document.getElementById('disease-filter').value.toLowerCase().trim();

    let filteredLocations = allLocations;

    // Filter by search term (department name)
    if (searchTerm) {
        filteredLocations = filteredLocations.filter(location =>
            location.department.toLowerCase().includes(searchTerm)
        );
    }

    // Filter by disease
    if (diseaseFilter) {
        filteredLocations = filteredLocations.filter(location =>
            location.treatedDiseases.toLowerCase().includes(diseaseFilter)
        );
    }

    // Update map
    displayLocations(filteredLocations);

    // Update results count
    updateResultsCount(`Znaleziono ${filteredLocations.length} ośrodków`);
}

// Update results count display
function updateResultsCount(text) {
    const resultsCount = document.getElementById('results-count');
    if (resultsCount) {
        resultsCount.textContent = text;
    }
}
