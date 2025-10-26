// Simple JavaScript for additional interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn, .btn-outline-success');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            let productName, productPrice;

            if (this.classList.contains('add-to-cart-btn')) {
                // Product details page
                productName = document.querySelector('.display-5').textContent;
                productPrice = document.querySelector('.h2.text-success').textContent;
            } else {
                // Product card
                const cardBody = this.closest('.card-body');
                productName = cardBody.querySelector('.card-title').textContent;
                productPrice = cardBody.querySelector('.text-success').textContent;
            }

            // Show notification
            showAlert(`Added to cart: ${productName} - ${productPrice}`, 'success');
        });
    });

    // Contact form enhancement
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;

            // Add loading state
            submitBtn.innerHTML = '<span class="loading me-2"></span>Sending...';
            submitBtn.disabled = true;

            // The form will be submitted normally, but we show loading state
            // The page will refresh after submission
        });

        // Real-time validation
        const inputs = contactForm.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    }

    // Test Telegram functionality (for development)
    const testTelegram = document.getElementById('testTelegram');
    if (testTelegram) {
        testTelegram.addEventListener('click', function(e) {
            e.preventDefault();
            fetch('/test-telegram')
                .then(response => response.text())
                .then(data => {
                    showAlert(data, 'info');
                })
                .catch(error => {
                    showAlert('Error testing Telegram: ' + error, 'danger');
                });
        });
    }

    // Helper function to validate form fields
    function validateField(field) {
        const value = field.value.trim();
        const isValid = value !== '';

        if (!isValid) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        }

        return isValid;
    }

    // Helper function to show alerts
    function showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.custom-alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create alert element
        const alert = document.createElement('div');
        alert.className = `custom-alert alert alert-${type} alert-dismissible fade show position-fixed`;
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        alert.style.minWidth = '300px';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Add to page
        document.body.appendChild(alert);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    // Add animation to elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.product-card, .hero-section img').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});