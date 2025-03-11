/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})



const filters = {
     calls: document.getElementById('filter-calls'),
     sockets: document.getElementById('filter-sockets'),
     toilet: document.getElementById('filter-toilet'),
     wifi: document.getElementById('filter-wifi'),
     seats: document.getElementById('filter-seats'),
     price: document.getElementById('filter-price')
     };

const cafes = document.querySelectorAll('.cafe');

function applyFilters() {
     cafes.forEach(cafe => {
         const matchesCalls = !filters.calls.checked || cafe.dataset.calls === 'True';
         const matchesSockets = !filters.sockets.checked || cafe.dataset.sockets === 'True';
         const matchesToilet = !filters.toilet.checked || cafe.dataset.toilet === 'True';
         const matchesWifi = !filters.wifi.checked || cafe.dataset.wifi === 'True';
         const matchesSeats = !filters.seats.value || parseInt(cafe.dataset.seats) >= parseInt(filters.seats.value);
         const matchesPrice = !filters.price.value || cafe.dataset.price.includes(filters.price.value);

         if (matchesCalls && matchesSockets && matchesToilet && matchesWifi && matchesSeats && matchesPrice) {
            cafe.style.display = 'flex';
         } else {
            cafe.style.display = 'none';
         }
     });
}

Object.values(filters).forEach(filter => {
    filter.addEventListener('input', applyFilters);
});

