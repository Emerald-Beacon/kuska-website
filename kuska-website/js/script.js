// ========================================
// MOBILE MENU TOGGLE
// ========================================

const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');

        // Animate hamburger menu
        const spans = mobileMenuToggle.querySelectorAll('span');
        if (navMenu.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translateY(8px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            const spans = mobileMenuToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });
}

// ========================================
// SMOOTH SCROLLING
// ========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');

        // Skip if it's just "#" or links to privacy policy, etc.
        if (href === '#' || href === '#privacy') {
            return;
        }

        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ========================================
// TESTIMONIALS CAROUSEL
// ========================================

const testimonialCards = document.querySelectorAll('.testimonial-card');
const prevBtn = document.querySelector('.carousel-btn.prev');
const nextBtn = document.querySelector('.carousel-btn.next');
const indicators = document.querySelectorAll('.indicator');

let currentSlide = 0;

function showSlide(index) {
    // Hide all slides
    testimonialCards.forEach(card => {
        card.classList.remove('active');
    });

    // Remove active class from all indicators
    indicators.forEach(indicator => {
        indicator.classList.remove('active');
    });

    // Show current slide
    if (testimonialCards[index]) {
        testimonialCards[index].classList.add('active');
    }

    // Activate current indicator
    if (indicators[index]) {
        indicators[index].classList.add('active');
    }
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % testimonialCards.length;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + testimonialCards.length) % testimonialCards.length;
    showSlide(currentSlide);
}

if (nextBtn) {
    nextBtn.addEventListener('click', nextSlide);
}

if (prevBtn) {
    prevBtn.addEventListener('click', prevSlide);
}

// Indicator click events
indicators.forEach((indicator, index) => {
    indicator.addEventListener('click', () => {
        currentSlide = index;
        showSlide(currentSlide);
    });
});

// Auto-advance carousel every 6 seconds
let autoAdvance = setInterval(nextSlide, 6000);

// Pause auto-advance on hover
const carousel = document.querySelector('.testimonials-carousel');
if (carousel) {
    carousel.addEventListener('mouseenter', () => {
        clearInterval(autoAdvance);
    });

    carousel.addEventListener('mouseleave', () => {
        autoAdvance = setInterval(nextSlide, 6000);
    });
}

// ========================================
// FORM SUBMISSIONS
// ========================================

// Hero Form
const heroForm = document.getElementById('hero-contact-form');
if (heroForm) {
    heroForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form data
        const formData = new FormData(heroForm);
        const data = Object.fromEntries(formData);

        // Here you would typically send the data to a server
        console.log('Hero form submitted:', data);

        // Show success message
        alert('Thank you for your interest! We will contact you shortly.');

        // Reset form
        heroForm.reset();
    });
}

// Contact Form
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form data
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData);

        // Here you would typically send the data to a server
        console.log('Contact form submitted:', data);

        // Show success message
        alert('Thank you for reaching out! We will get back to you as soon as possible.');

        // Reset form
        contactForm.reset();
    });
}

// ========================================
// SCROLL ANIMATIONS (Fade in on scroll)
// ========================================

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
const animateElements = document.querySelectorAll('.service-card, .location-card, .faq-item, .testimonial-card');
animateElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ========================================
// SECTION REVEAL ANIMATIONS
// ========================================

const sectionObserverOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -100px 0px'
};

const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('section-visible');
            // Optional: Unobserve after animation to improve performance
            sectionObserver.unobserve(entry.target);
        }
    });
}, sectionObserverOptions);

// Observe all major sections
const sections = document.querySelectorAll('.about-section, .services-section, .locations-section, .insurance-section, .testimonials-section, .faqs-section, .contact-section');
sections.forEach(section => {
    section.classList.add('section-animate');
    sectionObserver.observe(section);
});

// ========================================
// HEADER SCROLL EFFECT
// ========================================

const header = document.querySelector('.header');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    // Add shadow on scroll
    if (currentScroll > 10) {
        header.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
    } else {
        header.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
    }

    lastScroll = currentScroll;
});

// ========================================
// KEYBOARD NAVIGATION FOR CAROUSEL
// ========================================

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        prevSlide();
    } else if (e.key === 'ArrowRight') {
        nextSlide();
    }
});

// ========================================
// FORM VALIDATION ENHANCEMENT
// ========================================

// Add visual feedback for form validation
const inputs = document.querySelectorAll('input, textarea, select');
inputs.forEach(input => {
    input.addEventListener('blur', () => {
        if (input.validity.valid && input.value !== '') {
            input.style.borderColor = '#10b981'; // Green for valid
        } else if (!input.validity.valid && input.value !== '') {
            input.style.borderColor = '#ef4444'; // Red for invalid
        } else {
            input.style.borderColor = '#e5e7eb'; // Default
        }
    });

    input.addEventListener('focus', () => {
        input.style.borderColor = '#3b82f6'; // Blue on focus
    });
});

// ========================================
// PHONE NUMBER FORMATTING
// ========================================

const phoneInputs = document.querySelectorAll('input[type="tel"]');
phoneInputs.forEach(input => {
    input.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');

        if (value.length > 10) {
            value = value.slice(0, 10);
        }

        if (value.length >= 6) {
            e.target.value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
        } else if (value.length >= 3) {
            e.target.value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
        } else {
            e.target.value = value;
        }
    });
});

// ========================================
// CLAUDE CODE EDITOR INTERFACE
// ========================================

let logoClickCount = 0;
let clickTimer = null;

const footerLogo = document.getElementById('footer-logo-trigger');
const editorInterface = document.getElementById('editor-interface');
const closeEditorBtn = document.getElementById('close-editor');
const sendMessageBtn = document.getElementById('send-message');
const editorInput = document.getElementById('editor-input');
const chatMessages = document.getElementById('chat-messages');

// Footer logo click handler
if (footerLogo) {
    footerLogo.addEventListener('click', () => {
        logoClickCount++;

        // Reset counter after 2 seconds
        clearTimeout(clickTimer);
        clickTimer = setTimeout(() => {
            logoClickCount = 0;
        }, 2000);

        // Show editor after 6 clicks
        if (logoClickCount === 6) {
            editorInterface.classList.remove('hidden');
            logoClickCount = 0;
            console.log('Claude Code Editor activated!');
        }
    });
}

// Close editor
if (closeEditorBtn) {
    closeEditorBtn.addEventListener('click', () => {
        editorInterface.classList.add('hidden');
    });
}

// Send message function
function sendMessage() {
    const message = editorInput.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessageToChat(message, 'user');

    // Clear input
    editorInput.value = '';

    // Show typing indicator
    showTypingIndicator();

    // Simulate AI response (in production, this would call Claude API)
    setTimeout(() => {
        removeTypingIndicator();
        const response = generateMockResponse(message);
        addMessageToChat(response, 'assistant');
    }, 1500);
}

// Add message to chat
function addMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}-message`;
    messageDiv.textContent = message;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Mock response generator (placeholder for Claude API)
function generateMockResponse(message) {
    const lowerMessage = message.toLowerCase();

    if (lowerMessage.includes('color') || lowerMessage.includes('blue') || lowerMessage.includes('yellow')) {
        return "I can help you change the colors! To modify the color scheme, I would update the CSS variables in the :root section. Would you like me to change specific colors like the primary blue or accent yellow?";
    } else if (lowerMessage.includes('font') || lowerMessage.includes('text')) {
        return "I can modify the fonts! The website currently uses Montserrat Alternates for headings and Montserrat for body text. What font changes would you like me to make?";
    } else if (lowerMessage.includes('hero') || lowerMessage.includes('header')) {
        return "I can help with the hero section! Would you like me to change the gradient background, adjust the text, or modify the contact form?";
    } else if (lowerMessage.includes('button')) {
        return "I can modify button styles! The buttons currently use the primary blue color. What would you like to change about them?";
    } else {
        return "I understand you want to make changes to the website. To actually edit the code, you'll need to:\n\n1. Set up Claude API credentials\n2. Connect this interface to the API\n3. Then I can make real-time edits!\n\nFor now, this is a demonstration interface. What would you like to change?";
    }
}

// Send message on button click
if (sendMessageBtn) {
    sendMessageBtn.addEventListener('click', sendMessage);
}

// Send message on Enter key (Shift+Enter for new line)
if (editorInput) {
    editorInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// ========================================
// INITIALIZE ON PAGE LOAD
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Kuska Autism Services website loaded successfully!');
    console.log('Tip: Click the footer logo 6 times to access the editor!');

    // Initialize first testimonial slide
    showSlide(0);
});
