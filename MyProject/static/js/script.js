// Simple script for subtle intro animations.

document.addEventListener('DOMContentLoaded', () => {
    // Hero Animation
    const heroText = document.querySelector('.hero-text');
    const heroImage = document.querySelector('.hero-image');
    
    // Check if elements exist before applying styles
    if (heroText && heroImage) {
        // Initial state for animation
        heroText.style.opacity = '0';
        heroText.style.transform = 'translateY(20px)';
        heroText.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
        
        heroImage.style.opacity = '0';
        heroImage.style.transform = 'scale(0.95)';
        heroImage.style.transition = 'opacity 0.8s ease-out 0.2s, transform 0.8s ease-out 0.2s';

        // Trigger animation after a short delay
        setTimeout(() => {
            heroText.style.opacity = '1';
            heroText.style.transform = 'translateY(0)';
            heroImage.style.opacity = '1';
            heroImage.style.transform = 'scale(1)';
        }, 100);
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Skills filter functionality
    const searchBar = document.getElementById('search-bar');
    const categoryFilter = document.getElementById('category-filter');
    const skillsGrid = document.getElementById('skills-grid');
    const skillCards = skillsGrid.querySelectorAll('.skill-card');
    const noResultsMessage = document.getElementById('no-results');

    function filterSkills() {
        if (!searchBar || !categoryFilter || !skillsGrid) return;
        const searchTerm = searchBar.value.toLowerCase();
        const selectedCategory = categoryFilter.value;
        let visibleCards = 0;

        skillCards.forEach(card => {
            const title = card.dataset.title.toLowerCase();
            const category = card.dataset.category;

            const matchesSearch = title.includes(searchTerm);
            const matchesCategory = selectedCategory === 'all' || category === selectedCategory;

            if (matchesSearch && matchesCategory) {
                card.classList.remove('hide');
                visibleCards++;
            } else {
                card.classList.add('hide');
            }
        });

        if (visibleCards === 0) {
            noResultsMessage.style.display = 'block';
        } else {
            noResultsMessage.style.display = 'none';
        }
    }

    if (searchBar && categoryFilter && skillsGrid) {
        searchBar.addEventListener('input', filterSkills);
        categoryFilter.addEventListener('change', filterSkills);
    }
});