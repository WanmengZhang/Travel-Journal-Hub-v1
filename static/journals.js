/**
 * Journals Page JavaScript
 * Handles displaying and managing journal entries list
 */

const API_BASE_URL = '/api';
let allEntries = [];

// Load entries on page load
document.addEventListener('DOMContentLoaded', () => {
    loadJournals();
    setupSearchFilter();
});

/**
 * Load all journal entries
 */
async function loadJournals() {
    try {
        const response = await fetch(`${API_BASE_URL}/entries`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch entries');
        }
        
        allEntries = await response.json();
        displayJournals(allEntries);
        
    } catch (error) {
        console.error('Error loading journals:', error);
        displayError('Failed to load journals. Please try again later.');
    }
}

/**
 * Display journals in the list
 */
function displayJournals(entries) {
    const container = document.getElementById('journals-list');
    const noJournalsDiv = document.getElementById('no-journals');
    
    if (entries.length === 0) {
        container.style.display = 'none';
        noJournalsDiv.style.display = 'block';
        return;
    }
    
    container.style.display = 'flex';
    noJournalsDiv.style.display = 'none';
    
    container.innerHTML = entries.map(entry => createJournalItem(entry)).join('');
}

/**
 * Create a journal item HTML
 */
function createJournalItem(entry) {
    const startDate = new Date(entry.start_date).toLocaleDateString('en-US', { 
        month: 'long', 
        day: 'numeric', 
        year: 'numeric' 
    });
    const endDate = new Date(entry.end_date).toLocaleDateString('en-US', { 
        month: 'long', 
        day: 'numeric', 
        year: 'numeric' 
    });
    
    const highlights = entry.highlights ? entry.highlights.split('\n').filter(h => h.trim()) : [];
    const highlightsList = highlights.length > 0 
        ? `<div class="journal-highlights">
             <h5>Highlights</h5>
             <ul class="highlights-list">
               ${highlights.map(h => `<li>${escapeHtml(h)}</li>`).join('')}
             </ul>
           </div>`
        : '';
    
    const photoLinks = entry.photo_links ? entry.photo_links.split('\n').filter(p => p.trim()) : [];
    const photosHtml = photoLinks.length > 0
        ? `<div class="journal-photos">
             ${photoLinks.map(link => `<img src="${escapeHtml(link)}" alt="Photo" class="journal-photo" onerror="this.style.display='none'">`).join('')}
           </div>`
        : '';
    
    return `
        <div class="journal-item">
            <div class="journal-header">
                <div>
                    <h3 class="journal-title">${escapeHtml(entry.destination)}</h3>
                    <div class="journal-dates">${startDate} - ${endDate}</div>
                </div>
                <div class="journal-actions">
                    <button class="btn btn-small btn-primary" onclick="editEntry(${entry.id})">Edit</button>
                    <button class="btn btn-small btn-danger" onclick="confirmDelete(${entry.id})">Delete</button>
                </div>
            </div>
            ${entry.description ? `<div class="journal-content">${escapeHtml(entry.description)}</div>` : ''}
            ${highlightsList}
            ${photosHtml}
        </div>
    `;
}

/**
 * Edit entry - navigate to editor
 */
function editEntry(id) {
    window.location.href = `/editor?id=${id}`;
}

/**
 * Confirm and delete entry
 */
async function confirmDelete(id) {
    if (!confirm('Are you sure you want to delete this journal entry? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/entries/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete entry');
        }
        
        // Reload journals
        await loadJournals();
        
    } catch (error) {
        console.error('Error deleting entry:', error);
        alert('Failed to delete entry. Please try again.');
    }
}

/**
 * Setup search filter
 */
function setupSearchFilter() {
    const searchInput = document.getElementById('search-input');
    
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        
        const filteredEntries = allEntries.filter(entry => 
            entry.destination.toLowerCase().includes(searchTerm) ||
            (entry.description && entry.description.toLowerCase().includes(searchTerm)) ||
            (entry.highlights && entry.highlights.toLowerCase().includes(searchTerm))
        );
        
        displayJournals(filteredEntries);
    });
}

/**
 * Display error message
 */
function displayError(message) {
    const container = document.getElementById('journals-list');
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
