/**
 * Home Page JavaScript
 * Handles displaying journal entry summaries and statistics
 */

const API_BASE_URL = '/api';

// Fetch and display entries on page load
document.addEventListener('DOMContentLoaded', () => {
    loadEntriesSummary();
});

/**
 * Load and display entry summaries and statistics
 */
async function loadEntriesSummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/entries`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch entries');
        }
        
        const entries = await response.json();
        
        // Update statistics
        updateStatistics(entries);
        
        // Display recent entries (limit to 6)
        displayEntriesSummary(entries.slice(0, 6));
        
    } catch (error) {
        console.error('Error loading entries:', error);
        displayError('Failed to load entries. Please try again later.');
    }
}

/**
 * Update statistics section
 */
function updateStatistics(entries) {
    // Total entries
    document.getElementById('total-entries').textContent = entries.length;
    
    // Unique destinations
    const uniqueDestinations = new Set(entries.map(entry => entry.destination));
    document.getElementById('destinations-count').textContent = uniqueDestinations.size;
    
    // Latest trip
    if (entries.length > 0) {
        document.getElementById('latest-trip').textContent = entries[0].destination;
    } else {
        document.getElementById('latest-trip').textContent = 'No trips yet';
    }
}

/**
 * Display entry summaries in grid
 */
function displayEntriesSummary(entries) {
    const container = document.getElementById('entries-summary');
    
    if (entries.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No Entries Yet</h3>
                <p>Start documenting your travels!</p>
                <a href="/editor" class="btn btn-primary">Create Your First Entry</a>
            </div>
        `;
        return;
    }
    
    container.innerHTML = entries.map(entry => createEntryCard(entry)).join('');
}

/**
 * Create an entry card HTML
 */
function createEntryCard(entry) {
    const highlights = entry.highlights ? entry.highlights.split('\n').filter(h => h.trim()) : [];
    const highlightsList = highlights.slice(0, 3).map(h => `<li>${escapeHtml(h)}</li>`).join('');
    
    const photoLinks = entry.photo_links ? entry.photo_links.split('\n').filter(p => p.trim()) : [];
    const firstPhoto = photoLinks.length > 0 ? `<img src="${escapeHtml(photoLinks[0])}" alt="${escapeHtml(entry.destination)}" class="entry-photo" onerror="this.style.display='none'">` : '';
    
    const startDate = new Date(entry.start_date).toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
    });
    const endDate = new Date(entry.end_date).toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
    });
    
    return `
        <div class="entry-card" onclick="window.location.href='/editor?id=${entry.id}'">
            <h4>${escapeHtml(entry.destination)}</h4>
            <div class="entry-date">${startDate} - ${endDate}</div>
            ${entry.description ? `<p>${escapeHtml(entry.description.substring(0, 100))}${entry.description.length > 100 ? '...' : ''}</p>` : ''}
            ${highlightsList ? `<div class="entry-highlights"><ul>${highlightsList}</ul></div>` : ''}
            ${firstPhoto}
        </div>
    `;
}

/**
 * Display error message
 */
function displayError(message) {
    const container = document.getElementById('entries-summary');
    container.innerHTML = `
        <div class="empty-state">
            <h3>Error</h3>
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
