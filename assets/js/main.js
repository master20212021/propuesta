/* =============================================
   EROS MARKETING — Propuesta Dulce y Salado
   JavaScript — Interactions & Animations
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {

    // --- Navbar scroll effect ---
    const navbar = document.getElementById('navbar');
    const backToTop = document.getElementById('backToTop');

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;

        // Navbar shrink
        if (scrollY > 80) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Back to top button
        if (scrollY > 600) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }

        // Active nav link
        updateActiveNav();
    });

    // --- Back to top ---
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // --- Mobile nav toggle ---
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Close mobile nav on link click
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });

    // --- Active nav link based on scroll ---
    function updateActiveNav() {
        const sections = document.querySelectorAll('section[id]');
        const scrollY = window.scrollY + 100;

        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            const navLink = document.querySelector(`.nav-links a[href="#${id}"]`);

            if (navLink) {
                if (scrollY >= top && scrollY < top + height) {
                    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
                    navLink.classList.add('active');
                }
            }
        });
    }

    // --- Scroll reveal animations ---
    const revealElements = document.querySelectorAll(
        '.card, .logo-card, .slogan-card, .banner-item, .social-card, .promo-card, .pricing-card, .subsection, .caballete-mockup-container, .menu-showcase, .contact-card'
    );

    revealElements.forEach(el => {
        el.classList.add('reveal');
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => observer.observe(el));

    // --- Smooth scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = navbar.offsetHeight + 10;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // --- Typing effect for hero (optional subtle touch) ---
    const heroBrand = document.querySelector('.hero-brand');
    if (heroBrand) {
        heroBrand.style.opacity = '0';
        heroBrand.style.transform = 'translateY(20px)';
        setTimeout(() => {
            heroBrand.style.transition = 'all 0.8s ease';
            heroBrand.style.opacity = '1';
            heroBrand.style.transform = 'translateY(0)';
        }, 300);
    }

    // --- Counter animation for section numbers ---
    const sectionNumbers = document.querySelectorAll('.section-number');
    const numberObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInScale 0.5s ease forwards';
                numberObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    sectionNumbers.forEach(num => numberObserver.observe(num));

    // Add fadeInScale keyframes dynamically
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInScale {
            from { opacity: 0; transform: scale(0.5); }
            to { opacity: 1; transform: scale(1); }
        }
    `;
    document.head.appendChild(style);

    console.log('🚀 Eros Marketing — Propuesta Dulce y Salado loaded successfully');
});
