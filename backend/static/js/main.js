// Main JavaScript for HealthLinkAI - MindWell

// Utility functions
const Utils = {
    // Generate unique session ID
    generateSessionId: () => {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    },

    // Format date for display
    formatDate: (date) => {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Escape HTML to prevent XSS
    escapeHtml: (text) => {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    // Show notification
    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300 translate-x-full`;
        
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-black',
            info: 'bg-blue-500 text-white'
        };
        
        notification.className += ` ${colors[type] || colors.info}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    },

    // Debounce function
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// API service
const API = {
    baseUrl: '',
    
    // Generic API call
    call: async (endpoint, options = {}) => {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(API.baseUrl + endpoint, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'API call failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Symptom checker
    checkSymptoms: async (symptoms, age, gender) => {
        return API.call('/api/check-symptoms', {
            method: 'POST',
            body: JSON.stringify({ symptoms, age, gender })
        });
    },

    // MindWell chat
    sendMessage: async (message) => {
        return API.call('/api/mindwell', {
            method: 'POST',
            body: JSON.stringify({ message })
        });
    },

    // Get nearest providers
    getNearestProviders: async (lat, lng, type = null, limit = 10) => {
        const params = new URLSearchParams({
            lat: lat,
            lng: lng,
            limit: limit,
            format: 'json'
        });
        if (type) params.append('type', type);
        
        return API.call(`/providers?${params.toString()}`);
    },

    // Get recommendations
    getRecommendations: async () => {
        return API.call('/api/recommendations');
    }
};

// Form validation
const Validator = {
    email: (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    phone: (phone) => {
        const re = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
        return re.test(phone);
    },

    required: (value) => {
        return value && value.trim().length > 0;
    },

    minLength: (value, min) => {
        return value && value.length >= min;
    },

    maxLength: (value, max) => {
        return value && value.length <= max;
    }
};

// Loading states
const Loading = {
    show: (element, text = 'Loading...') => {
        if (element) {
            element.disabled = true;
            element.innerHTML = `
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                ${text}
            `;
        }
    },

    hide: (element, originalText) => {
        if (element) {
            element.disabled = false;
            element.innerHTML = originalText;
        }
    }
};

// Local storage management
const Storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Storage error:', error);
        }
    },

    get: (key, defaultValue = null) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Storage error:', error);
            return defaultValue;
        }
    },

    remove: (key) => {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Storage error:', error);
        }
    },

    clear: () => {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('Storage error:', error);
        }
    }
};

// Analytics and tracking
const Analytics = {
    track: (event, properties = {}) => {
        // Placeholder for analytics tracking
        console.log('Analytics Event:', event, properties);
        
        // In production, integrate with analytics service
        // Example: gtag('event', event, properties);
    },

    pageView: (page) => {
        Analytics.track('page_view', { page });
    },

    userAction: (action, category = 'user') => {
        Analytics.track('user_action', { action, category });
    }
};

// Accessibility helpers
const A11y = {
    announceToScreenReader: (message) => {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    },

    trapFocus: (element) => {
        const focusableElements = element.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        element.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        lastElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        firstElement.focus();
                        e.preventDefault();
                    }
                }
            }
        });
    }
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Track page view
    Analytics.pageView(window.location.pathname);
    
    // Initialize mobile menu
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            Analytics.userAction('mobile_menu_toggle');
        });
    }
    
    // Initialize tooltips and popovers
    initializeTooltips();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
    
    // Check for saved user preferences
    loadUserPreferences();
});

// Initialize tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
        element.addEventListener('focus', showTooltip);
        element.addEventListener('blur', hideTooltip);
    });
}

function showTooltip(event) {
    const element = event.target;
    const text = element.getAttribute('data-tooltip');
    
    if (!text) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'absolute z-50 px-2 py-1 text-sm text-white bg-gray-900 rounded shadow-lg';
    tooltip.textContent = text;
    tooltip.id = 'tooltip';
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
}

function hideTooltip() {
    const tooltip = document.getElementById('tooltip');
    if (tooltip) {
        document.body.removeChild(tooltip);
    }
}

// Form enhancements
function initializeFormEnhancements() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Add loading states to submit buttons
        form.addEventListener('submit', (e) => {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                Loading.show(submitButton, 'Processing...');
                
                // Reset after form submission (if not prevented)
                setTimeout(() => {
                    Loading.hide(submitButton, originalText);
                }, 100);
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', validateInput);
            input.addEventListener('input', Utils.debounce(validateInput, 300));
        });
    });
}

function validateInput(event) {
    const input = event.target;
    const value = input.value;
    let isValid = true;
    let errorMessage = '';
    
    // Required validation
    if (input.hasAttribute('required') && !Validator.required(value)) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    
    // Email validation
    if (input.type === 'email' && value && !Validator.email(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address';
    }
    
    // Phone validation
    if (input.type === 'tel' && value && !Validator.phone(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid phone number';
    }
    
    // Min/max length validation
    const minLength = input.getAttribute('minlength');
    if (minLength && value && !Validator.minLength(value, parseInt(minLength))) {
        isValid = false;
        errorMessage = `Minimum ${minLength} characters required`;
    }
    
    const maxLength = input.getAttribute('maxlength');
    if (maxLength && value && !Validator.maxLength(value, parseInt(maxLength))) {
        isValid = false;
        errorMessage = `Maximum ${maxLength} characters allowed`;
    }
    
    // Update UI based on validation
    updateInputValidation(input, isValid, errorMessage);
}

function updateInputValidation(input, isValid, errorMessage) {
    const errorElement = input.parentNode.querySelector('.error-message');
    
    if (isValid) {
        input.classList.remove('border-red-500');
        input.classList.add('border-green-500');
        if (errorElement) {
            errorElement.remove();
        }
    } else {
        input.classList.remove('border-green-500');
        input.classList.add('border-red-500');
        
        if (!errorElement && errorMessage) {
            const error = document.createElement('p');
            error.className = 'error-message text-red-500 text-sm mt-1';
            error.textContent = errorMessage;
            input.parentNode.appendChild(error);
        }
    }
}

// Keyboard shortcuts
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i]');
            if (searchInput) {
                searchInput.focus();
                Analytics.userAction('keyboard_shortcut_search');
            }
        }
        
        // Escape to close modals/menus
        if (e.key === 'Escape') {
            const mobileMenu = document.querySelector('.mobile-menu');
            if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
            }
        }
    });
}

// User preferences
function loadUserPreferences() {
    const preferences = Storage.get('userPreferences', {});
    
    // Apply saved preferences
    if (preferences.theme) {
        document.body.classList.add(`theme-${preferences.theme}`);
    }
    
    if (preferences.fontSize) {
        document.body.style.fontSize = preferences.fontSize;
    }
}

function saveUserPreferences(preferences) {
    const current = Storage.get('userPreferences', {});
    const updated = { ...current, ...preferences };
    Storage.set('userPreferences', updated);
}

// MindWell Chat Enhancement
const MindWellChat = {
    init() {
        const chatContainer = document.getElementById('chat-messages');
        const chatForm = document.getElementById('chat-form');
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-button');
        
        if (!chatContainer || !chatForm || !chatInput) return;
        
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;
            
            this.addMessage(message, 'user');
            chatInput.value = '';
            this.showTypingIndicator();
            
            try {
                const response = await API.sendMessage(message);
                this.hideTypingIndicator();
                this.addMessage(response.response, 'bot');
                this.scrollToBottom();
            } catch (error) {
                this.hideTypingIndicator();
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot', true);
            }
        });
    },
    
    addMessage(text, sender, isError = false) {
        const chatContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-4`;
        
        const bubbleClass = sender === 'user' 
            ? 'bg-teal-600 text-white' 
            : isError ? 'bg-red-100 text-red-800' : 'bg-white text-cool-gray-900 shadow-soft';
            
        messageDiv.innerHTML = `
            <div class="max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${bubbleClass}">
                <p class="text-sm">${Utils.escapeHtml(text)}</p>
                <span class="text-xs opacity-75">${new Date().toLocaleTimeString()}</span>
            </div>
        `;
        
        chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    },
    
    showTypingIndicator() {
        const chatContainer = document.getElementById('chat-messages');
        const indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.className = 'flex justify-start mb-4';
        indicator.innerHTML = `
            <div class="bg-white shadow-soft rounded-2xl px-4 py-2">
                <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-cool-gray-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-cool-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-cool-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
            </div>
        `;
        chatContainer.appendChild(indicator);
        this.scrollToBottom();
    },
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    },
    
    scrollToBottom() {
        const chatContainer = document.getElementById('chat-messages');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
};

// Symptom Checker Enhancement
const SymptomChecker = {
    currentStep: 1,
    selectedSymptoms: [],
    
    init() {
        this.initSymptomChips();
        this.initMultiStepForm();
    },
    
    initSymptomChips() {
        const commonSymptoms = [
            'Headache', 'Fever', 'Cough', 'Fatigue', 'Nausea', 'Dizziness',
            'Chest Pain', 'Shortness of Breath', 'Abdominal Pain', 'Joint Pain'
        ];
        
        const chipsContainer = document.getElementById('symptom-chips');
        if (!chipsContainer) return;
        
        commonSymptoms.forEach(symptom => {
            const chip = document.createElement('button');
            chip.type = 'button';
            chip.className = 'symptom-chip px-3 py-1 rounded-full border border-cool-gray-300 text-sm hover:bg-teal-50 hover:border-teal-300 transition-colors';
            chip.textContent = symptom;
            chip.addEventListener('click', () => this.toggleSymptom(chip, symptom));
            chipsContainer.appendChild(chip);
        });
    },
    
    toggleSymptom(chip, symptom) {
        if (this.selectedSymptoms.includes(symptom)) {
            this.selectedSymptoms = this.selectedSymptoms.filter(s => s !== symptom);
            chip.classList.remove('bg-teal-100', 'border-teal-500', 'text-teal-700');
            chip.classList.add('border-cool-gray-300');
        } else {
            this.selectedSymptoms.push(symptom);
            chip.classList.add('bg-teal-100', 'border-teal-500', 'text-teal-700');
            chip.classList.remove('border-cool-gray-300');
        }
    },
    
    initMultiStepForm() {
        const form = document.getElementById('symptom-form');
        if (!form) return;
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            this.showSkeletonLoader();
            
            const formData = new FormData(form);
            formData.append('selected_symptoms', this.selectedSymptoms.join(','));
            
            try {
                const response = await fetch('/symptoms', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const html = await response.text();
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const results = doc.querySelector('#results-section');
                    
                    if (results) {
                        this.hideSkeletonLoader();
                        this.showResults(results.innerHTML);
                    }
                }
            } catch (error) {
                this.hideSkeletonLoader();
                Utils.showNotification('Error analyzing symptoms', 'error');
            }
        });
    },
    
    showSkeletonLoader() {
        const resultsContainer = document.getElementById('results-container');
        if (!resultsContainer) return;
        
        resultsContainer.innerHTML = `
            <div class="bg-white rounded-2xl shadow-soft p-6 animate-pulse">
                <div class="h-4 bg-cool-gray-200 rounded w-3/4 mb-4"></div>
                <div class="h-4 bg-cool-gray-200 rounded w-1/2 mb-6"></div>
                <div class="space-y-3">
                    <div class="h-3 bg-cool-gray-200 rounded"></div>
                    <div class="h-3 bg-cool-gray-200 rounded w-5/6"></div>
                    <div class="h-3 bg-cool-gray-200 rounded w-4/6"></div>
                </div>
            </div>
        `;
        resultsContainer.classList.remove('hidden');
    },
    
    hideSkeletonLoader() {
        const resultsContainer = document.getElementById('results-container');
        if (resultsContainer) {
            resultsContainer.innerHTML = '';
        }
    },
    
    showResults(html) {
        const resultsContainer = document.getElementById('results-container');
        if (!resultsContainer) return;
        
        resultsContainer.innerHTML = html;
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
        
        // Add icons to results
        const riskElements = resultsContainer.querySelectorAll('[data-risk]');
        riskElements.forEach(el => {
            const risk = el.dataset.risk;
            let icon = '';
            
            if (risk === 'high' || risk === 'critical') {
                icon = '<svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>';
            }
            
            el.innerHTML = icon + el.innerHTML;
        });
    }
};

// Providers Enhancement
const ProvidersEnhancement = {
    userLocation: null,
    
    init() {
        this.getUserLocation();
    },
    
    async getUserLocation() {
        const statusEl = document.getElementById('location-status');
        
        if (!navigator.geolocation) {
            this.showLocationError('Geolocation not supported');
            return;
        }
        
        if (statusEl) {
            statusEl.innerHTML = '<div class="text-blue-600">Getting your location...</div>';
        }
        
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                this.userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                if (statusEl) {
                    statusEl.innerHTML = '<div class="text-green-600">Location detected</div>';
                }
                
                await this.loadNearestProviders();
            },
            (error) => {
                this.showLocationError('Location access denied');
            }
        );
    },
    
    showLocationError(message) {
        const statusEl = document.getElementById('location-status');
        if (statusEl) {
            statusEl.innerHTML = `<div class="text-red-600">${message}</div>`;
        }
    },
    
    async loadNearestProviders() {
        if (!this.userLocation) return;
        
        try {
            const data = await API.getNearestProviders(
                this.userLocation.lat,
                this.userLocation.lng
            );
            
            this.renderProviderCards(data.providers || []);
        } catch (error) {
            Utils.showNotification('Error loading providers', 'error');
        }
    },
    
    renderProviderCards(providers) {
        const container = document.getElementById('providers-list');
        if (!container) return;
        
        container.innerHTML = providers.map(provider => `
            <div class="bg-white rounded-2xl shadow-soft p-6 hover:shadow-lg transition-shadow">
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <h3 class="text-lg font-semibold text-cool-gray-900">${provider.name}</h3>
                        <p class="text-teal-600">${provider.specialty}</p>
                        <p class="text-cool-gray-600 text-sm">${provider.address}</p>
                    </div>
                    <div class="text-right">
                        <div class="text-yellow-500">★ ${provider.rating}</div>
                        <div class="text-sm text-cool-gray-600">${provider.distance_display}</div>
                    </div>
                </div>
                <div class="flex space-x-2">
                    <a href="tel:${provider.phone}" class="btn-primary flex-1 text-center">Call</a>
                    <a href="mailto:${provider.email}" class="btn-secondary flex-1 text-center">Email</a>
                </div>
            </div>
        `).join('');
    }
};

// Initialize page-specific enhancements
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    
    if (path.includes('/mindwell')) {
        MindWellChat.init();
    }
    
    if (path.includes('/symptoms')) {
        SymptomChecker.init();
    }
    
    if (path.includes('/providers')) {
        ProvidersEnhancement.init();
    }
});

// Export utilities for use in other scripts
window.HealthLinkAI = {
    Utils,
    API,
    Validator,
    Loading,
    Storage,
    Analytics,
    A11y,
    saveUserPreferences,
    MindWellChat,
    SymptomChecker,
    ProvidersEnhancement
};
