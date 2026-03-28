document.addEventListener('DOMContentLoaded', () => {
    const revealables = document.querySelectorAll('.reveal');
    revealables.forEach((node, index) => {
        setTimeout(() => {
            node.classList.add('is-visible');
        }, 120 * index);
    });
});
