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

/**
 * API Functions
 * Fetch portfolio data from backend API and render dynamically
 */

/**
 * Fetch data from API endpoint
 */
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`/api/${endpoint}`);
        const data = await response.json();
        if (data.success) {
            return data.data;
        }
        throw new Error(data.message || 'Failed to fetch data');
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        return null;
    }
}

/**
 * Render projects dynamically
 */
async function renderProjects() {
    const projects = await fetchAPI('projects');
    if (!projects) return;

    const projectsGrid = document.querySelector('.projects-grid');
    if (!projectsGrid) return;

    projectsGrid.innerHTML = projects.map(project => {
        const linksHTML = project.links.map(link => {
            const iconClass = link.type === 'live' ? 'fas fa-external-link-alt' : 'fab fa-github';
            const ariaLabel = link.type === 'live' ? 'View Project' : 'View Code';
            return `<a href="${link.url}" target="_blank" rel="noopener noreferrer" class="project-link" aria-label="${ariaLabel}">
                <i class="${iconClass}"></i>
            </a>`;
        }).join('');

        const tagsHTML = project.tags.map(tag => `<span class="tag">${tag}</span>`).join('');

        return `
            <div class="project-card">
                <div class="project-image">
                    <div class="project-placeholder">
                        <i class="${project.icon}"></i>
                    </div>
                </div>
                <div class="project-content">
                    <div class="project-header">
                        <h3 class="project-title">${project.title}</h3>
                        <div class="project-links">${linksHTML}</div>
                    </div>
                    <p class="project-description">${project.description}</p>
                    <div class="project-tags">${tagsHTML}</div>
                </div>
            </div>
        `;
    }).join('');

    // Re-observe new project cards for animations
    document.querySelectorAll('.project-card').forEach(card => {
        animationObserver.observe(card);
    });
}

/**
 * Render skills dynamically
 */
async function renderSkills() {
    const skillsGrid = document.querySelector('.skills-grid');
    if (!skillsGrid) return;

    const skills = await fetchAPI('skills');
    if (!skills || skills.length === 0) {
        skillsGrid.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">Unable to load skills. Please refresh the page.</p>';
        return;
    }

    skillsGrid.innerHTML = skills.map(category => {
        const skillsHTML = category.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('');
        return `
            <div class="skill-category">
                <h3 class="category-title">${category.title}</h3>
                <div class="skill-tags">${skillsHTML}</div>
            </div>
        `;
    }).join('');

    // Re-observe new skill categories for animations
    document.querySelectorAll('.skill-category').forEach(category => {
        animationObserver.observe(category);
    });
}

/**
 * Render experience dynamically
 */
async function renderExperience() {
    const experience = await fetchAPI('experience');
    if (!experience) return;

    const experienceTimeline = document.querySelector('.experience-timeline');
    if (!experienceTimeline) return;

    experienceTimeline.innerHTML = experience.map(exp => {
        const descriptionHTML = exp.description.map(desc => `<li>${desc}</li>`).join('');
        const tagsHTML = exp.tags.map(tag => `<span class="experience-tag">${tag}</span>`).join('');

        return `
            <div class="experience-item">
                <div class="experience-dot"></div>
                <div class="experience-content">
                    <div class="experience-period">${exp.period}</div>
                    <h3 class="experience-title">${exp.title}</h3>
                    <div class="experience-company">${exp.company} – ${exp.location}</div>
                    <ul class="experience-description">${descriptionHTML}</ul>
                    <div class="experience-tags">${tagsHTML}</div>
                </div>
            </div>
        `;
    }).join('');

    // Re-observe new experience items for animations
    document.querySelectorAll('.experience-item').forEach(item => {
        animationObserver.observe(item);
    });
}

/**
 * Render education dynamically
 */
async function renderEducation() {
    const educationTimeline = document.querySelector('.education-timeline');
    if (!educationTimeline) return;

    const education = await fetchAPI('education');
    if (!education || education.length === 0) {
        educationTimeline.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">Unable to load education. Please refresh the page.</p>';
        return;
    }

    educationTimeline.innerHTML = education.map(edu => `
        <div class="education-item">
            <div class="education-dot"></div>
            <div class="education-content">
                <div class="education-period">${edu.period}</div>
                <h3 class="education-title">${edu.title}</h3>
                <div class="education-institution">${edu.institution}</div>
                <div class="education-location">${edu.location}</div>
                <div class="education-grade">${edu.grade}</div>
            </div>
        </div>
    `).join('');

    // Re-observe new education items for animations
    document.querySelectorAll('.education-item').forEach(item => {
        animationObserver.observe(item);
    });
}

/**
 * Render certifications dynamically
 */
async function renderCertifications() {
    const certificationsGrid = document.querySelector('.certifications-grid');
    if (!certificationsGrid) return;

    const certifications = await fetchAPI('certifications');
    if (!certifications || certifications.length === 0) {
        certificationsGrid.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">Unable to load certifications. Please refresh the page.</p>';
        return;
    }

    certificationsGrid.innerHTML = certifications.map(cert => `
        <div class="certification-card">
            <div class="certification-icon">
                <i class="${cert.icon}"></i>
            </div>
            <h3 class="certification-title">${cert.title}</h3>
            <div class="certification-issuer">${cert.issuer}</div>
            <div class="certification-description">${cert.description}</div>
        </div>
    `).join('');

    // Re-observe new certification cards for animations
    document.querySelectorAll('.certification-card').forEach(card => {
        animationObserver.observe(card);
    });
}

/**
 * Update statistics from API
 */
async function updateStats() {
    const stats = await fetchAPI('stats');
    if (!stats) return;

    const statElements = {
        'github_projects': document.querySelector('.stat-item:nth-child(1) .stat-number'),
        'live_projects': document.querySelector('.stat-item:nth-child(2) .stat-number'),
        'years_experience': document.querySelector('.stat-item:nth-child(3) .stat-number')
    };

    if (statElements.github_projects) {
        statElements.github_projects.setAttribute('data-target', stats.github_projects);
        statElements.github_projects.textContent = '0';
    }
    if (statElements.live_projects) {
        statElements.live_projects.setAttribute('data-target', stats.live_projects);
        statElements.live_projects.textContent = '0';
    }
    if (statElements.years_experience) {
        statElements.years_experience.setAttribute('data-target', stats.years_experience);
        statElements.years_experience.textContent = '0';
    }
}

// Page Initialization
document.addEventListener('DOMContentLoaded', async () => {
    // Set initial active nav link
    updateActiveNavLink();

    // Load data from API
    await Promise.all([
        renderProjects(),
        renderSkills(),
        renderExperience(),
        renderEducation(),
        renderCertifications(),
        updateStats()
    ]);

    const aboutSection = document.getElementById('about');

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

    // Contact form (AJAX): prevent redirect, show inline status
    const contactForm = document.getElementById('contact-form');
    if (!contactForm) return;

    const submitBtn = document.getElementById('submit-btn');
    const submitText = document.getElementById('submit-text');
    const submitIcon = document.getElementById('submit-icon');

    const statusEl =
        document.getElementById('form-status') ||
        Object.assign(document.createElement('p'), {
            id: 'form-status',
            className: 'form-status'
        });
    if (!statusEl.isConnected) {
        statusEl.setAttribute('role', 'status');
        statusEl.setAttribute('aria-live', 'polite');
        contactForm.appendChild(statusEl);
    }

    const setStatus = (msg, ok) => {
        statusEl.textContent = msg || '';
        statusEl.classList.toggle('is-success', ok === true);
        statusEl.classList.toggle('is-error', ok === false);
    };

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        setStatus('', null);
        if (submitBtn) submitBtn.disabled = true;
        if (submitText) submitText.textContent = 'Sending...';
        if (submitIcon) submitIcon.className = 'fas fa-spinner fa-spin';

        try {
            const res = await fetch(contactForm.action, {
                method: 'POST',
                body: new FormData(contactForm),
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await res.json().catch(() => ({}));
            const ok = !!(res.ok && data.success);
            setStatus(
                data.message ||
                    (ok
                        ? "Message sent successfully! I'll get back to you soon."
                        : 'Unable to send message right now. Please try again later or email me directly.'),
                ok
            );
            if (ok) contactForm.reset();
        } catch {
            setStatus('Network error. Please try again later or email me directly.', false);
        } finally {
            if (submitBtn) submitBtn.disabled = false;
            if (submitText) submitText.textContent = 'Send Message';
            if (submitIcon) submitIcon.className = 'fas fa-paper-plane';
        }
    });
});
