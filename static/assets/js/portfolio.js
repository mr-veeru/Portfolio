// Article navigation and close logic
function closeArticle() {
    const main = document.getElementById('main');
    const currentArticle = main.querySelector('article:not([style*="display: none"])');
    if (currentArticle) {
        main.classList.add('closing');
        setTimeout(() => {
            window.location.hash = '';
            main.classList.remove('closing');
        }, 300);
    }
}

// Keyboard shortcut for closing articles
window.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeArticle();
    }
});

// Click outside to close
window.addEventListener('click', function(e) {
    const main = document.getElementById('main');
    const currentArticle = main.querySelector('article:not([style*="display: none"])');
    // Prevent closing if click is inside the contact form or its children
    const contactForm = document.getElementById('contactForm');
    if (currentArticle && !currentArticle.contains(e.target) && !e.target.closest('nav') && (!contactForm || !contactForm.contains(e.target))) {
        closeArticle();
    }
});

// Touch swipe to close (for mobile)
let touchStartX = 0;
let touchEndX = 0;
window.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
});
window.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});
function handleSwipe() {
    const swipeThreshold = 100;
    const swipeDistance = touchEndX - touchStartX;
    if (Math.abs(swipeDistance) > swipeThreshold) {
        if (swipeDistance > 0) {
            closeArticle();
        }
    }
}

// AJAX form submission
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const button = this.querySelector('.submit-btn');
        button.classList.add('loading');
        fetch('/submit_form', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                button.classList.remove('loading');
                button.classList.add('success');
                window.location.href = '/thank_you';
            } else {
                throw new Error('Form submission failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            button.classList.remove('loading');
            alert('There was an error submitting the form. Please try again.');
        });
    });
}

// SPA section navigation logic (hero always visible)
const sectionIds = ['about', 'experience', 'skills', 'projects', 'certifications', 'contact'];
function showSection(id) {
  sectionIds.forEach(sec => {
    const el = document.getElementById('section-' + sec);
    const navBtn = document.getElementById('nav-' + sec);
    if (el) {
      if (sec === id) {
        el.classList.remove('hidden');
        el.classList.add('animate-fade-in');
        // Smooth scroll to section
        setTimeout(() => {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 10);
      } else {
        el.classList.add('hidden');
        el.classList.remove('animate-fade-in');
      }
    }
    if (navBtn) {
      if (sec === id) {
        navBtn.classList.add('bg-teal-700', 'text-white', 'shadow');
      } else {
        navBtn.classList.remove('bg-teal-700', 'text-white', 'shadow');
      }
    }
  });
}
// On load, show section from hash or none
window.addEventListener('DOMContentLoaded', () => {
  let hash = window.location.hash.replace('#', '');
  if (sectionIds.includes(hash)) {
    showSection(hash);
  } else {
    // Hide all sections
    sectionIds.forEach(sec => {
      const el = document.getElementById('section-' + sec);
      if (el) el.classList.add('hidden');
      const navBtn = document.getElementById('nav-' + sec);
      if (navBtn) navBtn.classList.remove('bg-teal-700', 'text-white', 'shadow');
    });
  }
});
// Listen for hash changes (back/forward)
window.addEventListener('hashchange', () => {
  let hash = window.location.hash.replace('#', '');
  if (sectionIds.includes(hash)) {
    showSection(hash);
  } else {
    // Hide all sections
    sectionIds.forEach(sec => {
      const el = document.getElementById('section-' + sec);
      if (el) el.classList.add('hidden');
      const navBtn = document.getElementById('nav-' + sec);
      if (navBtn) navBtn.classList.remove('bg-teal-700', 'text-white', 'shadow');
    });
  }
});
// When a nav button is clicked, update hash and show section
sectionIds.forEach(sec => {
  const navBtn = document.getElementById('nav-' + sec);
  if (navBtn) {
    navBtn.addEventListener('click', () => {
      window.location.hash = sec;
      showSection(sec);
    });
  }
});
// Add fade-in animation (Tailwind custom)
// Add this to your Tailwind config if needed:
// theme: { extend: { animation: { 'fade-in': 'fadeIn 0.5s ease-in' }, keyframes: { fadeIn: { '0%': { opacity: 0 }, '100%': { opacity: 1 } } } } } 