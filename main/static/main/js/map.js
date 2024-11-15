// main/static/main/js/map.js

function openYandexMaps(latitude, longitude) {
    const url = `https://yandex.ru/maps/?rtext=~${latitude},${longitude}&rtt=auto`;
    window.open(url, '_blank');
}

document.addEventListener('DOMContentLoaded', function () {
    // Проверяем наличие элемента с ID 'locations-data'
    const locationsDataElement = document.getElementById('locations-data');
    if (!locationsDataElement) {
        console.error("Элемент с ID 'locations-data' не найден на странице.");
        return;
    }

    // Получаем JSON-данные из элемента 'locations-data'
    var locations = JSON.parse(locationsDataElement.textContent);

    var map = L.map('map').setView([55.751244, 37.618423], 10);  // центр на Москве

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    if (Array.isArray(locations) && locations.length > 0) {
        var markers = [];
        locations.forEach(function(location) {
            var marker = L.marker([location.latitude, location.longitude]).addTo(map);
            var popupContent = "<b>" + location.city + "</b><br/>" + location.address;
            marker.bindPopup(popupContent);
            markers.push(marker);
        });
        var group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.5));
    } else {
        console.warn("Нет доступных локаций для отображения на карте.");
    }
});
