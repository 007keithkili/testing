/* RemoteTravels - admin panel behaviour: live table filtering and a few
   small niceties that keep the dashboard in sync with the public site. */

document.addEventListener('DOMContentLoaded', function () {
    // --- Live search over the table with the matching #adminSearch input ---
    const search = document.getElementById('adminSearch');
    if (search) {
        const table = search.closest('.admin-card')?.querySelector('table');
        const rows = table ? Array.from(table.querySelectorAll('tbody tr')) : [];

        search.addEventListener('input', function () {
            const term = search.value.trim().toLowerCase();
            rows.forEach(function (row) {
                const isEmptyRow = row.querySelector('.table-empty');
                row.style.display = !term || isEmptyRow
                    ? ''
                    : (row.textContent.toLowerCase().includes(term) ? '' : 'none');
            });
        });
    }

    // --- Keyboard shortcut: "/" focuses the search box ---
    document.addEventListener('keydown', function (event) {
        if (event.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
            event.preventDefault();
            const box = document.getElementById('adminSearch');
            if (box) box.focus();
        }
    });

    // --- Keep the table row actions tidy: mark destructive buttons ---
    document.querySelectorAll('.admin-actions button').forEach(function (button) {
        if (/delete/i.test(button.textContent)) {
            button.classList.add('btn-danger');
        }
    });
});
