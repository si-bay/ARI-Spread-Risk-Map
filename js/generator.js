// --- GENERATOR.JS : PETA SPASIAL & LOGIKA MODEL TABULAR ---

// 1. Inisialisasi Peta (Default berpusat di Surabaya / Wilayah Pantauan - Tanpa API Key)
const map = L.map('map').setView([-7.2575, 112.7521], 12);

// Tambahkan Layer Peta Dasar Gratis (CartoDB Positron - Tidak Butuh Token/API Key)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    maxZoom: 18
}).addTo(map);

// 2. Dataset Awal Wilayah (Simulasi Data Tabular)
let ispaData = [
    { id: 1, name: "Kec. Gubeng", lat: -7.2756, lng: 112.7508, riskScore: 84, level: "high", cases: 342, aqi: 158, density: "14.200/km²" },
    { id: 2, name: "Kec. Wonokromo", lat: -7.2981, lng: 112.7366, riskScore: 78, level: "high", cases: 295, aqi: 149, density: "16.500/km²" },
    { id: 3, name: "Kec. Sukolilo", lat: -7.2912, lng: 112.7963, riskScore: 55, level: "medium", cases: 140, aqi: 112, density: "6.800/km²" },
    { id: 4, name: "Kec. Rungkut", lat: -7.3215, lng: 112.7782, riskScore: 62, level: "medium", cases: 185, aqi: 125, density: "8.900/km²" },
    { id: 5, name: "Kec. Genteng", lat: -7.2621, lng: 112.7420, riskScore: 74, level: "high", cases: 260, aqi: 145, density: "13.100/km²" },
    { id: 6, name: "Kec. Benowo", lat: -7.2289, lng: 112.6345, riskScore: 31, level: "low", cases: 48, aqi: 72, density: "2.400/km²" },
    { id: 7, name: "Kec. Lakarsantri", lat: -7.3054, lng: 112.6489, riskScore: 35, level: "low", cases: 52, aqi: 68, density: "3.100/km²" },
    { id: 8, name: "Kec. Tegalsari", lat: -7.2718, lng: 112.7354, riskScore: 67, level: "medium", cases: 210, aqi: 130, density: "15.400/km²" }
];

let markersLayer = L.layerGroup().addTo(map);

// Live Slider AQI
const inputAqi = document.getElementById('input-aqi');
const valAqi = document.getElementById('val-aqi');
inputAqi.addEventListener('input', () => {
    valAqi.textContent = inputAqi.value;
});

// Fungsi Warna & Label Risiko
function getRiskColor(level) {
    if (level === 'high') return '#ef4444';
    if (level === 'medium') return '#f59e0b';
    return '#10b981';
}

function getRiskLabel(level) {
    if (level === 'high') return 'Tinggi';
    if (level === 'medium') return 'Sedang';
    return 'Rendah';
}

// Menampilkan Detail di Sidebar
function showRegionDetail(item) {
    const detailBox = document.getElementById('region-detail');
    const badgeColor = getRiskColor(item.level);
    
    detailBox.innerHTML = `
        <h3>Detail: ${item.name}</h3>
        <ul class="detail-list">
            <li>
                <span>Status Risiko (Model Tabular)</span>
                <strong style="color: ${badgeColor}">${getRiskLabel(item.level)} (${item.riskScore}/100)</strong>
            </li>
            <li>
                <span>Kasus Aktif ISPA</span>
                <strong>${item.cases} Kasus</strong>
            </li>
            <li>
                <span>Indeks Polusi (AQI / Karhutla)</span>
                <strong>${item.aqi}</strong>
            </li>
            <li>
                <span>Kepadatan Penduduk</span>
                <strong>${item.density}</strong>
            </li>
        </ul>
    `;
}

// Merender Peta & Statistik
function renderMapData(data) {
    markersLayer.clearLayers();

    let countHigh = 0, countMedium = 0, countLow = 0;

    data.forEach(item => {
        if (item.level === 'high') countHigh++;
        else if (item.level === 'medium') countMedium++;
        else countLow++;

        const color = getRiskColor(item.level);

        const circle = L.circle([item.lat, item.lng], {
            color: color,
            fillColor: color,
            fillOpacity: 0.35,
            radius: item.riskScore * 15
        });

        circle.bindPopup(`
            <strong>${item.name}</strong><br>
            Risiko: <b>${getRiskLabel(item.level)}</b> (Skor: ${item.riskScore})<br>
            Kasus: ${item.cases}
        `);

        circle.on('click', () => {
            showRegionDetail(item);
        });

        markersLayer.addLayer(circle);
    });

    document.getElementById('count-high').textContent = countHigh;
    document.getElementById('count-medium').textContent = countMedium;
    document.getElementById('count-low').textContent = countLow;
}

// Filter & Pencarian Wilayah
function filterData() {
    const searchText = document.getElementById('search-input').value.toLowerCase();
    const selectedRisk = document.getElementById('risk-filter').value;

    const filtered = ispaData.filter(item => {
        const matchesName = item.name.toLowerCase().includes(searchText);
        const matchesRisk = selectedRisk === 'all' || item.level === selectedRisk;
        return matchesName && matchesRisk;
    });

    renderMapData(filtered);
}

document.getElementById('search-input').addEventListener('input', filterData);
document.getElementById('risk-filter').addEventListener('change', filterData);

// Simulasi Model Tabular saat Form Disubmit
document.getElementById('risk-generator-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('region-name').value;
    const aqi = parseFloat(inputAqi.value);
    const cases = parseFloat(document.getElementById('input-cases').value);
    const density = parseFloat(document.getElementById('input-density').value);

    // Kalkulasi Berbasis Logika Model Tabular (Feature Weights)
    const densityScore = Math.min((density / 25000) * 100, 100);
    const aqiScore = Math.min((aqi / 300) * 100, 100);
    const casesScore = Math.min((cases / 500) * 100, 100);

    let rawScore = (aqiScore * 0.4) + (casesScore * 0.35) + (densityScore * 0.25);
    let finalScore = Math.round(Math.min(Math.max(rawScore, 10), 99));

    let level = 'low';
    if (finalScore > 70) level = 'high';
    else if (finalScore >= 40) level = 'medium';

    // Random koordinat di sekitar area pemantauan untuk simulasi wilayah baru
    const randomLat = -7.2575 + (Math.random() - 0.5) * 0.08;
    const randomLng = 112.7521 + (Math.random() - 0.5) * 0.08;

    const newItem = {
        id: ispaData.length + 1,
        name: name,
        lat: randomLat,
        lng: randomLng,
        riskScore: finalScore,
        level: level,
        cases: cases,
        aqi: aqi,
        density: density.toLocaleString() + '/km²'
    };

    ispaData.push(newItem);
    renderMapData(ispaData);
    showRegionDetail(newItem);

    // Reset Form
    this.reset();
    valAqi.textContent = "120";
    inputAqi.value = 120;
});

// Fitur Ekspor CSV
document.getElementById('btn-export').addEventListener('click', () => {
    let csvContent = "data:text/csv;charset=utf-8,ID,Wilayah,Skor Risiko,Tingkat,Kasus,AQI,Kepadatan\n";
    ispaData.forEach(item => {
        csvContent += `"${item.id}","${item.name}","${item.riskScore}","${getRiskLabel(item.level)}","${item.cases}","${item.aqi}","${item.density}"\n`;
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "dataset_peta_risiko_ispa.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

// Render Awal Peta
renderMapData(ispaData);