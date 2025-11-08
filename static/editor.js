/**
 * Editor Page JavaScript
 * Handles creating and editing journal entries
 */

const API_BASE_URL = '/api';
let currentEntryId = null;

// Initialize editor on page load
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    currentEntryId = urlParams.get('id');
    
    if (currentEntryId) {
        loadEntry(currentEntryId);
        document.getElementById('editor-title').textContent = 'Edit Entry';
        document.getElementById('submit-btn').textContent = 'Update Entry';
        document.getElementById('delete-section').style.display = 'block';
    }
    
    setupFormHandlers();
});

/**
 * Load entry for editing
 */
async function loadEntry(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/entries/${id}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch entry');
        }
        
        const entry = await response.json();
        populateForm(entry);
        
    } catch (error) {
        console.error('Error loading entry:', error);
        showMessage('Failed to load entry. Please try again.', 'error');
    }
}

/**
 * Populate form with entry data
 */
function populateForm(entry) {
    document.getElementById('destination').value = entry.destination || '';
    document.getElementById('start-date').value = entry.start_date || '';
    document.getElementById('end-date').value = entry.end_date || '';
    document.getElementById('description').value = entry.description || '';
    document.getElementById('highlights').value = entry.highlights || '';
    document.getElementById('photo-links').value = entry.photo_links || '';
}

/**
 * Setup form event handlers
 */
function setupFormHandlers() {
    const form = document.getElementById('entry-form');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveEntry();
    });
    
    // Delete button
    const deleteBtn = document.getElementById('delete-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', async () => {
            await deleteEntry();
        });
    }
    
    // Date validation
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    
    startDateInput.addEventListener('change', validateDates);
    endDateInput.addEventListener('change', validateDates);
}

/**
 * Validate that end date is after start date
 */
function validateDates() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    
    if (startDate && endDate && new Date(endDate) < new Date(startDate)) {
        document.getElementById('end-date').setCustomValidity('End date must be after start date');
    } else {
        document.getElementById('end-date').setCustomValidity('');
    }
}

/**
 * Save entry (create or update)
 */
async function saveEntry() {
    const formData = {
        destination: document.getElementById('destination').value,
        start_date: document.getElementById('start-date').value,
        end_date: document.getElementById('end-date').value,
        description: document.getElementById('description').value,
        highlights: document.getElementById('highlights').value,
        photo_links: document.getElementById('photo-links').value
    };
    
    // Validate required fields
    if (!formData.destination || !formData.start_date || !formData.end_date) {
        showMessage('Please fill in all required fields', 'error');
        return;
    }
    
    try {
        const url = currentEntryId 
            ? `${API_BASE_URL}/entries/${currentEntryId}`
            : `${API_BASE_URL}/entries`;
        
        const method = currentEntryId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to save entry');
        }
        
        const result = await response.json();
        showMessage(currentEntryId ? 'Entry updated successfully!' : 'Entry created successfully!', 'success');
        
        // Redirect to journals page after a short delay
        setTimeout(() => {
            window.location.href = '/journals';
        }, 1500);
        
    } catch (error) {
        console.error('Error saving entry:', error);
        showMessage(error.message || 'Failed to save entry. Please try again.', 'error');
    }
}

/**
 * Delete entry
 */
async function deleteEntry() {
    if (!confirm('Are you sure you want to delete this entry? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/entries/${currentEntryId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete entry');
        }
        
        showMessage('Entry deleted successfully!', 'success');
        
        // Redirect to journals page after a short delay
        setTimeout(() => {
            window.location.href = '/journals';
        }, 1500);
        
    } catch (error) {
        console.error('Error deleting entry:', error);
        showMessage('Failed to delete entry. Please try again.', 'error');
    }
}

/**
 * Show message to user
 */
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    // Auto-hide success messages
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
    }
}
