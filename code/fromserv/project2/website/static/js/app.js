document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('a, button');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translateY(0)';
        });
    });
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.innerHTML = '<div class="loading-spinner"></div>';
        });
    });
});
