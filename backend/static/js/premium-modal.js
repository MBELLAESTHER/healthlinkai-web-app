// Premium Upsell Modal functionality
class PremiumModal {
    constructor() {
        this.modal = null;
        this.init();
    }

    init() {
        this.createModal();
        this.bindEvents();
    }

    createModal() {
        const modalHTML = `
            <div id="premium-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center p-4">
                <div class="bg-white rounded-2xl max-w-md w-full shadow-soft-lg transform transition-all">
                    <div class="p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-xl font-bold text-gray-900">Upgrade to Premium</h3>
                            <button id="close-premium-modal" class="text-gray-400 hover:text-gray-600">
                                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                                </svg>
                            </button>
                        </div>
                        
                        <div class="text-center mb-6">
                            <div class="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                                </svg>
                            </div>
                            <p id="modal-message" class="text-gray-600 mb-4">You've reached your daily limit. Upgrade to Premium for unlimited access!</p>
                        </div>

                        <div class="space-y-3 mb-6">
                            <div class="flex items-center">
                                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                </svg>
                                <span class="text-gray-700">Unlimited symptom checks</span>
                            </div>
                            <div class="flex items-center">
                                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                </svg>
                                <span class="text-gray-700">Priority MindWell responses</span>
                            </div>
                            <div class="flex items-center">
                                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                </svg>
                                <span class="text-gray-700">Request doctor callback</span>
                            </div>
                            <div class="flex items-center">
                                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                </svg>
                                <span class="text-gray-700">24/7 priority support</span>
                            </div>
                        </div>

                        <div class="flex space-x-3">
                            <button id="upgrade-now" class="flex-1 btn-primary">
                                Upgrade Now - $9.99/month
                            </button>
                            <button id="maybe-later" class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors">
                                Maybe Later
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById('premium-modal');
    }

    bindEvents() {
        // Close modal events
        document.getElementById('close-premium-modal').addEventListener('click', () => this.hide());
        document.getElementById('maybe-later').addEventListener('click', () => this.hide());
        
        // Upgrade button
        document.getElementById('upgrade-now').addEventListener('click', () => {
            window.location.href = '/subscribe';
        });

        // Close on backdrop click
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.hide();
            }
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.modal.classList.contains('hidden')) {
                this.hide();
            }
        });
    }

    show(message = null) {
        if (message) {
            document.getElementById('modal-message').textContent = message;
        }
        this.modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    hide() {
        this.modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Doctor Callback Modal for Premium Users
class CallbackModal {
    constructor() {
        this.modal = null;
        this.init();
    }

    init() {
        this.createModal();
        this.bindEvents();
    }

    createModal() {
        const modalHTML = `
            <div id="callback-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center p-4">
                <div class="bg-white rounded-2xl max-w-md w-full shadow-soft-lg">
                    <div class="p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-xl font-bold text-gray-900">Request Doctor Callback</h3>
                            <button id="close-callback-modal" class="text-gray-400 hover:text-gray-600">
                                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                                </svg>
                            </button>
                        </div>
                        
                        <form id="callback-form" class="space-y-4">
                            <div>
                                <label for="callback-phone" class="block text-sm font-medium text-gray-700 mb-1">Phone Number *</label>
                                <input type="tel" id="callback-phone" name="phone" required 
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus-ring input-enhanced"
                                       placeholder="+237 6XX XXX XXX">
                            </div>
                            
                            <div>
                                <label for="preferred-time" class="block text-sm font-medium text-gray-700 mb-1">Preferred Time</label>
                                <select id="preferred-time" name="preferred_time" 
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus-ring input-enhanced">
                                    <option value="">Select preferred time</option>
                                    <option value="morning">Morning (8AM - 12PM)</option>
                                    <option value="afternoon">Afternoon (12PM - 6PM)</option>
                                    <option value="evening">Evening (6PM - 9PM)</option>
                                    <option value="anytime">Anytime</option>
                                </select>
                            </div>
                            
                            <div>
                                <label for="callback-reason" class="block text-sm font-medium text-gray-700 mb-1">Reason for Callback</label>
                                <textarea id="callback-reason" name="reason" rows="3"
                                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus-ring input-enhanced"
                                          placeholder="Brief description of your health concern..."></textarea>
                            </div>
                            
                            <div class="flex space-x-3 pt-4">
                                <button type="submit" class="flex-1 btn-primary">
                                    Request Callback
                                </button>
                                <button type="button" id="cancel-callback" class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors">
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById('callback-modal');
    }

    bindEvents() {
        // Close modal events
        document.getElementById('close-callback-modal').addEventListener('click', () => this.hide());
        document.getElementById('cancel-callback').addEventListener('click', () => this.hide());
        
        // Form submission
        document.getElementById('callback-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitCallback();
        });

        // Close on backdrop click
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.hide();
            }
        });
    }

    async submitCallback() {
        const form = document.getElementById('callback-form');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch('/request-callback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                this.showSuccess(result.message);
                form.reset();
            } else {
                this.showError(result.message || 'Failed to request callback');
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
        }
    }

    showSuccess(message) {
        // Create success notification
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);

        this.hide();
    }

    showError(message) {
        // Create error notification
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    show() {
        this.modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    hide() {
        this.modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Initialize modals when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.premiumModal = new PremiumModal();
    window.callbackModal = new CallbackModal();

    // Show premium modal if usage error exists
    if (window.showUpgradeModal) {
        window.premiumModal.show(window.upgradeMessage);
    }

    // Add callback button functionality
    const callbackButtons = document.querySelectorAll('[data-callback-button]');
    callbackButtons.forEach(button => {
        button.addEventListener('click', () => {
            window.callbackModal.show();
        });
    });
});

// Export for use in other scripts
window.PremiumModal = PremiumModal;
window.CallbackModal = CallbackModal;
