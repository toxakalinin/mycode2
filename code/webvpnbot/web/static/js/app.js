document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects
    const buttons = document.querySelectorAll('a, button');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translateY(0)';
        });
    });

    // Add loading state for downloads
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.innerHTML = '<div class="loading-spinner"></div>';
        });
    });
});
