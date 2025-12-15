document.querySelectorAll('.csv-table th').forEach(th => {
    th.addEventListener('mouseenter', () => th.style.backgroundColor = '#e0e0e0');
    th.addEventListener('mouseleave', () => th.style.backgroundColor = '#f4f4f4');
});
