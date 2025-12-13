// Contact form functionality

if (window.location.pathname.includes('contact.html')) {
    document.addEventListener('DOMContentLoaded', function() {
        const contactForm = document.getElementById('contactForm');
        const formSuccess = document.getElementById('formSuccess');
        const formError = document.getElementById('formError');
        
        if (contactForm) {
            contactForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Get form data
                const formData = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    subject: document.getElementById('subject').value,
                    message: document.getElementById('message').value
                };
                
                // Validate
                if (!formData.name || !formData.email || !formData.subject || !formData.message) {
                    showMessage(formError, 'Please fill in all required fields.');
                    return;
                }
                
                // For static site, we'll create a mailto link
                // In production, you'd send this to a serverless function or API
                const mailtoLink = `mailto:info@luvora.com?subject=${encodeURIComponent(formData.subject)}&body=${encodeURIComponent(
                    `Name: ${formData.name}\nEmail: ${formData.email}\nPhone: ${formData.phone}\n\nMessage:\n${formData.message}`
                )}`;
                
                // Show success message
                contactForm.style.display = 'none';
                showMessage(formSuccess, 'Thank you for your message! Opening email client...');
                
                // Open mailto link
                setTimeout(() => {
                    window.location.href = mailtoLink;
                }, 1000);
                
                // Reset form after 3 seconds
                setTimeout(() => {
                    contactForm.reset();
                    contactForm.style.display = 'block';
                    formSuccess.style.display = 'none';
                }, 3000);
            });
        }
    });
}

function showMessage(element, message) {
    if (element) {
        element.querySelector('p').textContent = message;
        element.style.display = 'block';
        
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }
}
