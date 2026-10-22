/* RemoteTravels - destinations page. The destination catalogue is rendered by
   Flask, the quick-look modal pulls live data from the JSON API so newly
   added destinations show up without touching this file. */

(function () {
    const modal = document.getElementById('destinationModal');
    if (!modal) return;

    const closeModalBtn = document.getElementById('closeModal');
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalTag = document.getElementById('modalTag');
    const modalDescription = document.getElementById('modalDescription');
    const modalDuration = document.getElementById('modalDuration');
    const modalLocation = document.getElementById('modalLocation');
    const modalPrice = document.getElementById('modalPrice');
    const similarGrid = document.getElementById('similarGrid');
    const destinationCards = document.querySelectorAll('.destination-card');

    const apiBase = document.body.dataset.apiBase || '/api/v1';

    async function fetchDestination(id) {
        const response = await fetch(`${apiBase}/destinations/${id}`);
        if (!response.ok) throw new Error('Destination not found');
        return response.json();
    }

    async function openDestinationModal(id) {
        let destination;
        try {
            destination = await fetchDestination(id);
        } catch (error) {
            console.error(error);
            return;
        }

        modalImage.src = destination.image_url;
        modalImage.alt = destination.name;
        modalTitle.textContent = destination.name;
        modalTag.textContent = destination.tag;
        modalDescription.textContent = destination.description;
        modalDuration.textContent = destination.duration;
        modalLocation.textContent = destination.location;
        modalPrice.innerHTML = `${destination.price} <span>/ person</span>`;

        const similar = destination.similar || [];
        similarGrid.innerHTML = '';
        similar.forEach(dest => {
            const similarCard = document.createElement('div');
            similarCard.className = 'similar-card';
            similarCard.setAttribute('data-id', dest.id);
            similarCard.innerHTML = `
                <div class="similar-img">
                    <img src="${dest.image_url}" alt="${dest.name}">
                </div>
                <div class="similar-content">
                    <h4>${dest.name}</h4>
                    <div class="similar-price">${dest.price}</div>
                </div>
            `;
            similarGrid.appendChild(similarCard);
            similarCard.addEventListener('click', () => openDestinationModal(dest.id));
        });

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    destinationCards.forEach(card => {
        card.addEventListener('click', event => {
            if (event.target.closest('a')) return;
            const id = parseInt(card.getAttribute('data-id'));
            if (!id) return;
            openDestinationModal(id);
        });
    });

    if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();
