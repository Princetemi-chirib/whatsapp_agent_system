// API Configuration
const API_BASE_URL = 'https://web-production-8cec.up.railway.app/api';

// DOM Elements
const agentForm = document.getElementById('agentForm');
const agentsList = document.getElementById('agentsList');
const successModal = document.getElementById('successModal');
const errorModal = document.getElementById('errorModal');
const editModal = document.getElementById('editModal');
const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');

// Search and filter elements
const agentSearch = document.getElementById('agentSearch');
const zoneFilter = document.getElementById('zoneFilter');
const statusFilter = document.getElementById('statusFilter');

// Global variables
let allAgents = [];
let filteredAgents = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadAgents();
    setupFormHandling();
    setupSearchAndFilters();
});

// Load existing agents
async function loadAgents() {
    try {
        const response = await fetch(`${API_BASE_URL}/agents/`);
        if (response.ok) {
            allAgents = await response.json();
            filteredAgents = [...allAgents];
            displayAgents(filteredAgents);
        } else {
            throw new Error('Failed to load agents');
        }
    } catch (error) {
        console.error('Error loading agents:', error);
        agentsList.innerHTML = '<div class="error">Failed to load agents. Please try again later.</div>';
    }
}

// Display agents in the grid
function displayAgents(agents) {
    if (agents.length === 0) {
        agentsList.innerHTML = '<div class="no-agents">No agents found matching your search criteria.</div>';
        return;
    }

    const agentsHTML = agents.map(agent => `
        <div class="agent-card">
            <div class="agent-actions">
                <button class="agent-action-btn" onclick="editAgent('${agent.id}')" title="Edit Agent">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="agent-action-btn delete" onclick="deleteAgent('${agent.id}')" title="Delete Agent">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="agent-name">${agent.name}</div>
            <div class="agent-details">
                <div><i class="fas fa-id-badge"></i> ${agent.agent_id}</div>
                <div><i class="fas fa-phone"></i> ${agent.phone}</div>
                <div><i class="fas fa-envelope"></i> ${agent.email}</div>
                <div><i class="fas fa-circle" style="color: ${agent.status === 'active' ? '#28a745' : '#dc3545'}"></i> ${agent.status}</div>
                ${agent.zone ? `<div><i class="fas fa-map-marker-alt"></i> ${agent.zone}</div>` : ''}
                ${agent.experience_years ? `<div><i class="fas fa-clock"></i> ${agent.experience_years} years experience</div>` : ''}
                ${agent.rating ? `<div><i class="fas fa-star"></i> ${agent.rating}/5 rating</div>` : ''}
                ${agent.total_inspections ? `<div><i class="fas fa-home"></i> ${agent.total_inspections} inspections</div>` : ''}
                ${agent.specializations && agent.specializations.length > 0 ? 
                    `<div><i class="fas fa-tags"></i> ${agent.specializations.join(', ')}</div>` : ''}
            </div>
        </div>
    `).join('');

    agentsList.innerHTML = agentsHTML;
}

// Setup form handling
function setupFormHandling() {
    agentForm.addEventListener('submit', handleFormSubmit);
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    // Show loading state
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding Agent...';
    submitButton.disabled = true;
    
    try {
        const formData = new FormData(event.target);
        const agentData = {
            agent_id: formData.get('agent_id'),
            name: formData.get('name'),
            phone: formData.get('phone'),
            email: formData.get('email'),
            status: 'active',
            zone: formData.get('zone') || null,
            specializations: formData.getAll('specializations'),
            experience_years: formData.get('experience_years') ? parseInt(formData.get('experience_years')) : null,
            rating: formData.get('rating') ? parseFloat(formData.get('rating')) : null,
            total_inspections: formData.get('total_inspections') ? parseInt(formData.get('total_inspections')) : null
        };

        const response = await fetch(`${API_BASE_URL}/agents/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(agentData)
        });

        if (response.ok) {
            const result = await response.json();
            showSuccessModal(`Agent "${agentData.name}" added successfully!`);
            event.target.reset();
            loadAgents(); // Refresh the agents list
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to add agent');
        }
    } catch (error) {
        console.error('Error adding agent:', error);
        showErrorModal(`Failed to add agent: ${error.message}`);
    } finally {
        // Reset button state
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
    }
}

// Show success modal
function showSuccessModal(message) {
    successMessage.textContent = message;
    successModal.style.display = 'block';
}

// Show error modal
function showErrorModal(message) {
    errorMessage.textContent = message;
    errorModal.style.display = 'block';
}

// Close modal
function closeModal() {
    successModal.style.display = 'none';
    errorModal.style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target === successModal) {
        successModal.style.display = 'none';
    }
    if (event.target === errorModal) {
        errorModal.style.display = 'none';
    }
}

// Form validation
function validateForm() {
    const requiredFields = ['agent_id', 'name', 'phone', 'email'];
    const errors = [];

    requiredFields.forEach(field => {
        const input = document.getElementById(field);
        if (!input.value.trim()) {
            errors.push(`${field.replace('_', ' ')} is required`);
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    });

    // Phone number validation
    const phone = document.getElementById('phone').value;
    if (phone && !phone.match(/^\+[1-9]\d{1,14}$/)) {
        errors.push('Phone number must be in international format (e.g., +2348012345678)');
        document.getElementById('phone').classList.add('error');
    }

    // Email validation
    const email = document.getElementById('email').value;
    if (email && !email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        errors.push('Please enter a valid email address');
        document.getElementById('email').classList.add('error');
    }

    return errors;
}

// Add real-time validation
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            const errors = validateForm();
            if (errors.length > 0) {
                // Show validation errors
                console.log('Validation errors:', errors);
            }
        });
    });
});

// Auto-generate agent ID
document.getElementById('name').addEventListener('input', function() {
    const name = this.value.trim();
    const agentIdField = document.getElementById('agent_id');
    
    if (name && !agentIdField.value) {
        const agentId = 'agent_' + name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '') + '_' + Date.now().toString().slice(-4);
        agentIdField.value = agentId;
    }
});

// Phone number formatting
document.getElementById('phone').addEventListener('input', function() {
    let value = this.value.replace(/\D/g, '');
    if (value.length > 0 && !value.startsWith('+')) {
        value = '+' + value;
    }
    this.value = value;
});

// Setup search and filter functionality
function setupSearchAndFilters() {
    agentSearch.addEventListener('input', filterAgents);
    zoneFilter.addEventListener('change', filterAgents);
    statusFilter.addEventListener('change', filterAgents);
}

// Filter agents based on search and filters
function filterAgents() {
    const searchTerm = agentSearch.value.toLowerCase();
    const zoneFilterValue = zoneFilter.value;
    const statusFilterValue = statusFilter.value;

    filteredAgents = allAgents.filter(agent => {
        const matchesSearch = !searchTerm || 
            agent.name.toLowerCase().includes(searchTerm) ||
            agent.phone.toLowerCase().includes(searchTerm) ||
            agent.email.toLowerCase().includes(searchTerm) ||
            agent.agent_id.toLowerCase().includes(searchTerm);
        
        const matchesZone = !zoneFilterValue || agent.zone === zoneFilterValue;
        const matchesStatus = !statusFilterValue || agent.status === statusFilterValue;

        return matchesSearch && matchesZone && matchesStatus;
    });

    displayAgents(filteredAgents);
}

// Edit agent functionality
function editAgent(agentId) {
    const agent = allAgents.find(a => a.id === agentId);
    if (!agent) return;

    // Populate edit form
    document.getElementById('editAgentId').value = agent.id;
    document.getElementById('editName').value = agent.name;
    document.getElementById('editPhone').value = agent.phone;
    document.getElementById('editEmail').value = agent.email;
    document.getElementById('editZone').value = agent.zone || '';
    document.getElementById('editStatus').value = agent.status;
    document.getElementById('editExperience').value = agent.experience_years || '';
    document.getElementById('editRating').value = agent.rating || '';
    document.getElementById('editInspections').value = agent.total_inspections || '';

    // Show edit modal
    editModal.style.display = 'block';
}

// Save agent edit
async function saveAgentEdit() {
    const agentId = document.getElementById('editAgentId').value;
    const formData = new FormData(document.getElementById('editAgentForm'));
    
    const updateData = {
        name: formData.get('name'),
        phone: formData.get('phone'),
        email: formData.get('email'),
        zone: formData.get('zone') || null,
        status: formData.get('status'),
        experience_years: formData.get('experience_years') ? parseInt(formData.get('experience_years')) : null,
        rating: formData.get('rating') ? parseFloat(formData.get('rating')) : null,
        total_inspections: formData.get('total_inspections') ? parseInt(formData.get('total_inspections')) : null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/agents/${agentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updateData)
        });

        if (response.ok) {
            showSuccessModal('Agent updated successfully!');
            closeModal();
            loadAgents(); // Reload agents
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to update agent');
        }
    } catch (error) {
        console.error('Error updating agent:', error);
        showErrorModal(`Failed to update agent: ${error.message}`);
    }
}

// Delete agent functionality
async function deleteAgent(agentId) {
    if (!confirm('Are you sure you want to delete this agent? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/agents/${agentId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showSuccessModal('Agent deleted successfully!');
            loadAgents(); // Reload agents
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to delete agent');
        }
    } catch (error) {
        console.error('Error deleting agent:', error);
        showErrorModal(`Failed to delete agent: ${error.message}`);
    }
}

// Update close modal function
function closeModal() {
    successModal.style.display = 'none';
    errorModal.style.display = 'none';
    editModal.style.display = 'none';
}

// Update window click handler
window.onclick = function(event) {
    if (event.target === successModal) {
        successModal.style.display = 'none';
    }
    if (event.target === errorModal) {
        errorModal.style.display = 'none';
    }
    if (event.target === editModal) {
        editModal.style.display = 'none';
    }
}

// Add some CSS for error states
const style = document.createElement('style');
style.textContent = `
    .error {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1) !important;
    }
    
    .no-agents {
        text-align: center;
        color: #666;
        font-style: italic;
        padding: 40px 20px;
        background: #f8f9fa;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
    }
    
    .error {
        text-align: center;
        color: #dc3545;
        padding: 20px;
        background: #f8d7da;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
    }
`;
document.head.appendChild(style);
