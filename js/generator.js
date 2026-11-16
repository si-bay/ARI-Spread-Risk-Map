
const API_URL = 'http://127.0.0.1:5000/api/regions';

const map = L.map('map', {
    maxBounds: [[-85, -180], [85, 180]],
    maxBoundsViscosity: 1,
    worldCopyJump: false
}).setView([-2.5, 115], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 18,
    minZoom: 2,
    noWrap: true
}).addTo(map);

const markersLayer = L.layerGroup().addTo(map);

let regionData = [];
let currentFilteredData = [];
let selectedRegionId = null;
let metadataBox = null;

const countrySelect = document.getElementById('country-select');
const provinceSelect = document.getElementById('province-select');
const citySelect = document.getElementById('city-select');
const districtSelect = document.getElementById('district-select');
const riskFilter = document.getElementById('risk-filter');
const detailBox = document.getElementById('region-detail');
const statusBox = document.getElementById('data-status');

const categoryInfo = {
    good: { label: 'Good', color: '#16a34a' },
    moderate: { label: 'Moderate', color: '#eab308' },
    sensitive: { label: 'Unhealthy for Sensitive Groups', color: '#f97316' },
    unhealthy: { label: 'Unhealthy', color: '#dc2626' },
    very_unhealthy: { label: 'Very Unhealthy', color: '#9333ea' },
    hazardous: { label: 'Hazardous', color: '#7f1d1d' },
    unavailable: { label: 'Unavailable', color: '#64748b' }
};

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    })[character]);
}

function getCategory(aqi) {
    if (typeof aqi !== 'number' || !Number.isFinite(aqi) || aqi < 0) {
        return 'unavailable';
    }

    if (aqi <= 50) return 'good';
    if (aqi <= 100) return 'moderate';
    if (aqi <= 150) return 'sensitive';
    if (aqi <= 200) return 'unhealthy';
    if (aqi <= 300) return 'very_unhealthy';

    return 'hazardous';
}

function formatValue(value, unit = '') {
    if (typeof value !== 'number' || !Number.isFinite(value)) {
        return 'Not available';
    }

    const formatted = Number(value.toFixed(2));

    return `${formatted}${unit ? ` ${escapeHtml(unit)}` : ''}`;
}

function escapeCsv(value) {
    const text = value === null || value === undefined ? '' : String(value);
    return `"${text.replaceAll('"', '""')}"`;
}

function setStatus(message, type = 'info') {
    if (!statusBox) return;

    statusBox.textContent = message;
    statusBox.className = `alert alert-${type} small py-2 mb-0`;
}


function initializeMetadata() {
    document.getElementById('metadata-source').textContent
    document.getElementById('metadata-retrieved').textContent
    document.getElementById('metadata-cache').textContent
}

function updateMetadata(result) {
    const retrievedDate = result.retrieved_at
        ? new Date(result.retrieved_at)
        : null;

    const retrievedText = retrievedDate && !Number.isNaN(retrievedDate.getTime())
        ? retrievedDate.toLocaleString()
        : 'Unavailable';

    const values = {
        'metadata-source': result.source || 'Unavailable',
        'metadata-retrieved': retrievedText,
        'metadata-cache': Number.isFinite(Number(result.cache_seconds))
            ? `${result.cache_seconds} seconds`
            : 'Unavailable',
        'metadata-model': result.model_note || 'Unavailable',
        'metadata-resolution': result.resolution_note || 'Unavailable'
    };

    Object.entries(values).forEach(([id, value]) => {
        const element = document.getElementById(id);

        if (element) {
            element.textContent = value;
        }
    });
}

function updateMetadataError(message) {
    const values = {
        'metadata-source': 'Unavailable',
        'metadata-retrieved': 'Unavailable',
        'metadata-cache': 'Unavailable',
        'metadata-model': message,
        'metadata-resolution': 'Unavailable'
    };

    Object.entries(values).forEach(([id, value]) => {
        const element = document.getElementById(id);

        if (element) {
            element.textContent = value;
        }
    });
}

function updateDropdown(select, values, firstLabel) {
    if (!select) return;

    const previous = select.value;
    select.replaceChildren();

    const first = document.createElement('option');
    first.value = 'all';
    first.textContent = firstLabel;
    select.appendChild(first);

    [...new Set(values.filter(Boolean))]
        .sort()
        .forEach(value => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = value;
            select.appendChild(option);
        });

    if ([...select.options].some(option => option.value === previous)) {
        select.value = previous;
    }
}

function getGeographicMatches() {
    const country = countrySelect?.value || 'all';

    return regionData.filter(item =>
        country === 'all' || item.country === country
    );
}

function refreshGeographicDropdowns(level) {
    const countryMatches = getGeographicMatches();

    if (level <= 1) {
        updateDropdown(
            provinceSelect,
            countryMatches.map(item => item.province),
            '-- All Provinces --'
        );
    }

    const province = provinceSelect?.value || 'all';

    const provinceMatches = countryMatches.filter(item =>
        province === 'all' || item.province === province
    );

    if (level <= 2) {
        updateDropdown(
            citySelect,
            provinceMatches.map(item => item.city),
            '-- All Regencies/Cities --'
        );
    }

    const city = citySelect?.value || 'all';

    const cityMatches = provinceMatches.filter(item =>
        city === 'all' || item.city === city
    );

    if (level <= 3) {
        updateDropdown(
            districtSelect,
            cityMatches.map(item => item.district),
            '-- All Districts --'
        );
    }
}

function initializeDropdowns() {
    updateDropdown(
        countrySelect,
        regionData.map(item => item.country),
        '-- All Countries --'
    );

    refreshGeographicDropdowns(1);
}

function matchesFilters(item) {
    const country = countrySelect?.value || 'all';
    const province = provinceSelect?.value || 'all';
    const city = citySelect?.value || 'all';
    const district = districtSelect?.value || 'all';
    const category = riskFilter?.value || 'all';

    const itemCategory = getCategory(item.air_quality?.us_aqi);

    return (country === 'all' || item.country === country)
        && (province === 'all' || item.province === province)
        && (city === 'all' || item.city === city)
        && (district === 'all' || item.district === district)
        && (category === 'all' || itemCategory === category);
}

function updateSummary(data) {
    const counts = {
        good: 0,
        moderate: 0,
        unhealthy: 0,
        unavailable: 0
    };

    data.forEach(item => {
        const category = getCategory(item.air_quality?.us_aqi);

        if (category === 'good') counts.good++;
        else if (category === 'moderate') counts.moderate++;
        else if (category === 'unavailable') counts.unavailable++;
        else counts.unhealthy++;
    });

    const elements = {
        good: document.getElementById('count-good'),
        moderate: document.getElementById('count-moderate'),
        unhealthy: document.getElementById('count-unhealthy'),
        unavailable: document.getElementById('count-unavailable')
    };

    Object.entries(counts).forEach(([key, value]) => {
        if (elements[key]) {
            elements[key].textContent = value;
        }
    });
}

function renderDetail(item) {
    if (!detailBox) return;

    const air = item.air_quality || {};
    const weather = item.weather || {};
    const category = getCategory(air.us_aqi);
    const categoryData = categoryInfo[category];

    const timestamp = air.time || weather.time || 'Timestamp unavailable';

    detailBox.innerHTML = `
        <h3>${escapeHtml(item.district || 'Unknown area')}</h3>
        <p class="small text-muted mb-2">
            ${escapeHtml(item.city)}, ${escapeHtml(item.province)}, ${escapeHtml(item.country)}
        </p>

        <div class="mb-2">
            <span class="badge" style="background:${categoryData.color}">
                ${categoryData.label}
            </span>
        </div>

        <ul class="detail-list">
            <li><span>US AQI</span><strong>${formatValue(air.us_aqi)}</strong></li>
            <li><span>PM2.5</span><strong>${formatValue(air.pm2_5, air.units?.pm2_5 || 'μg/m³')}</strong></li>
            <li><span>PM10</span><strong>${formatValue(air.pm10, air.units?.pm10 || 'μg/m³')}</strong></li>
            <li><span>Nitrogen dioxide (NO₂)</span><strong>${formatValue(air.nitrogen_dioxide, air.units?.nitrogen_dioxide || 'μg/m³')}</strong></li>
            <li><span>Sulphur dioxide (SO₂)</span><strong>${formatValue(air.sulphur_dioxide, air.units?.sulphur_dioxide || 'μg/m³')}</strong></li>
            <li><span>Ozone (O₃)</span><strong>${formatValue(air.ozone, air.units?.ozone || 'μg/m³')}</strong></li>
            <li><span>Temperature</span><strong>${formatValue(weather.temperature_2m, weather.units?.temperature_2m || '°C')}</strong></li>
            <li><span>Humidity</span><strong>${formatValue(weather.relative_humidity_2m, weather.units?.relative_humidity_2m || '%')}</strong></li>
            <li><span>Wind speed</span><strong>${formatValue(weather.wind_speed_10m, weather.units?.wind_speed_10m || 'km/h')}</strong></li>
            <li><span>Wind direction</span><strong>${formatValue(weather.wind_direction_10m, weather.units?.wind_direction_10m || '°')}</strong></li>
            <li><span>Precipitation</span><strong>${formatValue(weather.precipitation, weather.units?.precipitation || 'mm')}</strong></li>
        </ul>

        <p class="small text-muted mt-2 mb-1">
            Provider timestamp: ${escapeHtml(timestamp)}
        </p>

        <p class="small text-muted mb-0">
            Air-quality values are model estimates for the nearest grid cell,
            not local sensor measurements.
        </p>
    `;
}

function renderMap(data) {
    markersLayer.clearLayers();
    updateSummary(data);

    data.forEach(item => {
        const lat = Number(item.lat);
        const lng = Number(item.lng);

        if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

        const category = getCategory(item.air_quality?.us_aqi);
        const style = categoryInfo[category];

        const marker = L.circleMarker([lat, lng], {
            radius: 8,
            color: style.color,
            fillColor: style.color,
            fillOpacity: 0.75,
            weight: 1.5
        });

        marker.bindPopup(`
            <strong>${escapeHtml(item.district)}</strong><br>
            ${escapeHtml(item.city)}, ${escapeHtml(item.country)}<br>
            US AQI: ${formatValue(item.air_quality?.us_aqi)}<br>
            Category: ${style.label}
        `);

        marker.on('click', () => {
            selectedRegionId = item.id;
            renderDetail(item);
        });

        marker.addTo(markersLayer);
    });
}

function applyFilters() {
    currentFilteredData = regionData.filter(matchesFilters);

    renderMap(currentFilteredData);

    const selectedDistrict = districtSelect?.value || 'all';

    if (selectedDistrict !== 'all' && currentFilteredData.length === 1) {
        const target = currentFilteredData[0];

        map.setView([target.lat, target.lng], 11);
        selectedRegionId = target.id;
        renderDetail(target);
        return;
    }

    const selectedItem = currentFilteredData.find(
        item => item.id === selectedRegionId
    );

    if (selectedItem) {
        renderDetail(selectedItem);
    } else if (currentFilteredData.length > 0) {
        renderDetail(currentFilteredData[0]);
    } else if (detailBox) {
        detailBox.innerHTML = `
            <h3>Location Details</h3>
            <p class="placeholder-text">No locations match the selected filters.</p>
        `;
    }

    if (currentFilteredData.length > 0) {
        const target = currentFilteredData[0];

        if ((citySelect?.value || 'all') !== 'all') {
            map.setView([target.lat, target.lng], 9);
        } else if ((provinceSelect?.value || 'all') !== 'all') {
            map.setView([target.lat, target.lng], 7);
        } else if ((countrySelect?.value || 'all') !== 'all') {
            map.setView([target.lat, target.lng], 5);
        } else {
            map.setView([-2.5, 115], 4);
        }
    }
}

function exportCsv() {
    if (currentFilteredData.length === 0) {
        alert('No region data to export.');
        return;
    }

    const headers = [
        'ID',
        'Country',
        'Province',
        'City/Regency',
        'Area',
        'Latitude',
        'Longitude',
        'US AQI',
        'AQI Category',
        'PM2.5 (μg/m³)',
        'PM10 (μg/m³)',
        'NO2 (μg/m³)',
        'SO2 (μg/m³)',
        'O3 (μg/m³)',
        'Temperature (°C)',
        'Humidity (%)',
        'Wind speed (km/h)',
        'Wind direction (°)',
        'Precipitation (mm)',
        'Provider timestamp'
    ];

    const rows = currentFilteredData.map(item => {
        const air = item.air_quality || {};
        const weather = item.weather || {};

        return [
            item.id,
            item.country,
            item.province,
            item.city,
            item.district,
            item.lat,
            item.lng,
            air.us_aqi,
            categoryInfo[getCategory(air.us_aqi)].label,
            air.pm2_5,
            air.pm10,
            air.nitrogen_dioxide,
            air.sulphur_dioxide,
            air.ozone,
            weather.temperature_2m,
            weather.relative_humidity_2m,
            weather.wind_speed_10m,
            weather.wind_direction_10m,
            weather.precipitation,
            air.time || weather.time
        ].map(escapeCsv).join(',');
    });

    const csv = [
        headers.map(escapeCsv).join(','),
        ...rows
    ].join('\r\n');

    const blob = new Blob(['\uFEFF' + csv], {
        type: 'text/csv;charset=utf-8;'
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    link.href = url;
    link.download = 'eri_environmental_indicators.csv';

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
}

async function initializeApp() {
    initializeMetadata();
    setStatus('Retrieving environmental estimates from Open-Meteo...', 'info');

    try {
        const response = await fetch(API_URL, {
            signal: AbortSignal.timeout(35000)
        });

        const result = await response.json();

        if (!response.ok || result.status !== 'success' || !Array.isArray(result.data)) {
            throw new Error(result.message || 'Invalid API response.');
        }

        regionData = result.data.filter(item =>
            item &&
            Number.isFinite(Number(item.lat)) &&
            Number.isFinite(Number(item.lng))
        );

        if (regionData.length === 0) {
            throw new Error('No valid location data was received.');
        }

        updateMetadata(result);

        currentFilteredData = [...regionData];

        initializeDropdowns();
        applyFilters();

        setStatus(
            `Successfully retrieved environmental data for ${regionData.length} locations.`,
            'success'
        );

        const initialRegion = regionData.find(item => item.id === 20) || regionData[0];

        selectedRegionId = initialRegion.id;
        renderDetail(initialRegion);

    } catch (error) {
        regionData = [];
        currentFilteredData = [];

        renderMap([]);
        updateMetadataError(error.message);

        if (detailBox) {
            detailBox.innerHTML = `
                <h3>Environmental data unavailable</h3>
                <p class="placeholder-text">
                    The application could not retrieve current provider data.
                    Check that the Flask API is running and that the internet connection is available.
                    No sample values are substituted.
                </p>
            `;
        }

        setStatus(
            `Could not load environmental data: ${error.message}`,
            'danger'
        );
    }
}

countrySelect?.addEventListener('change', () => {
    if (provinceSelect) provinceSelect.value = 'all';
    if (citySelect) citySelect.value = 'all';
    if (districtSelect) districtSelect.value = 'all';

    refreshGeographicDropdowns(1);
    applyFilters();
});

provinceSelect?.addEventListener('change', () => {
    if (citySelect) citySelect.value = 'all';
    if (districtSelect) districtSelect.value = 'all';

    refreshGeographicDropdowns(2);
    applyFilters();
});

citySelect?.addEventListener('change', () => {
    if (districtSelect) districtSelect.value = 'all';

    refreshGeographicDropdowns(3);
    applyFilters();
});

districtSelect?.addEventListener('change', applyFilters);
riskFilter?.addEventListener('change', applyFilters);

document.getElementById('btn-export')?.addEventListener('click', exportCsv);

initializeApp();
