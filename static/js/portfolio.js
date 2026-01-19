/**
 * Portfolio JavaScript - Main Application Logic
 * Handles navigation, animations, and interactive features
 * 
 * @author Veerendra Bannuru
 * @version 1.0.0
 */

// DOM Elements
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');

// Navigation Functionality

/**
 * Navigation scroll effect - Adds background blur when scrolling
 * Updates active navigation link based on current section
 */

window.addEventListener('scroll', () => {
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    // Update active nav link
    updateActiveNavLink();
});

/**
 * Updates the active navigation link based on current scroll position
 * Highlights the navigation item corresponding to the visible section
 */
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section');
    const scrollPos = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');

        if (sectionId && scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

/**
 * Smooth scrolling for navigation links
 * Prevents default anchor behavior and smoothly scrolls to target section
 * Closes mobile menu after navigation
 */
const NAVBAR_OFFSET = 70;

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);

        if (targetSection) {
            const offsetTop = targetSection.offsetTop - NAVBAR_OFFSET;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }

        // Close mobile menu if open
        if (navMenu && hamburger) {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    });
});

/* 
 * Mobile Menu Functionality
 *
 * Handles hamburger menu toggle and keyboard navigation
 */
if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        const isExpanded = hamburger.classList.contains('active');
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        hamburger.setAttribute('aria-expanded', String(!isExpanded));
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    });
}

// Scroll Animations
const ANIMATION_OBSERVER_OPTIONS = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const animationObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
}, ANIMATION_OBSERVER_OPTIONS);

// Observe all animatable elements
const animatableSelectors = [
    '.project-card',
    '.certification-card',
    '.experience-item',
    '.education-item',
    '.skill-category'
];

animatableSelectors.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => animationObserver.observe(element));
});

/* 
 * Statistics Counter Animation
 *
 * Animates number counter from 0 to target value
 */

function animateCounter(element, target) {
    if (!element || !target) return;
    
    let current = 0;
    const increment = target / 50;
    const duration = 30;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, duration);
}

// Page Initialization
document.addEventListener('DOMContentLoaded', () => {
    // Set initial active nav link
    updateActiveNavLink();

    // Initialize intro text animation
    const introText = document.querySelector('.intro-text');
    if (introText) {
        introText.style.animation = 'fadeInUp 1s ease';
    }

    // Scroll indicator functionality
    const scrollIndicator = document.getElementById('scroll-to-about');
    const aboutSection = document.getElementById('about');

    if (scrollIndicator && aboutSection) {
        scrollIndicator.addEventListener('click', () => {
            const offsetTop = aboutSection.offsetTop - NAVBAR_OFFSET;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        });
    }

    // Statistics counter animation
    if (aboutSection) {
        const statsObserverOptions = { threshold: 0.3 };
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const statNumbers = document.querySelectorAll('.stat-number');
                    statNumbers.forEach(stat => {
                        const target = parseInt(stat.getAttribute('data-target'), 10);
                        if (target && stat.textContent.trim() === '0') {
                            animateCounter(stat, target);
                        }
                    });
                    statsObserver.unobserve(entry.target);
                }
            });
        }, statsObserverOptions);

        statsObserver.observe(aboutSection);
    }
});
