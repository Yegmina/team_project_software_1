'use strict';
let options = {
    inertia: true,
    inertiaMaxSpeed: 1000,
    keyboard: true,
    // center: L.latLng(50, 100),
}
const map = L.map('map', options).setView([45, 10], 3);
/* L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map); */
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    minZoom: 2.5,
    maxZoom: 20,
}).addTo(map);


