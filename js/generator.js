const map = L.map('map').setView([15.0, 0.0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 18
}).addTo(map);

function fallbackPredictByRFWeights(aqi, cases, densityVal, humidity) {
    const aqiScore = Math.min((aqi / 300) * 100, 100);
    const casesScore = Math.min((cases / 500) * 100, 100);
    const densityScore = Math.min((densityVal / 15000) * 100, 100);
    const humidityScore = Math.min((humidity / 100) * 100, 100);

    let rawScore = (aqiScore * 0.7223) + (casesScore * 0.2597) + (densityScore * 0.0093) + (humidityScore * 0.0087);
    let finalScore = Math.round(Math.min(Math.max(rawScore * 1.1, 10), 99));

    let level = 'low';
    if (finalScore > 65) {
        level = 'high';
    } else if (finalScore >= 35) {
        level = 'medium';
    }

    return { score: finalScore, level: level };
}

let ispaData = [
    { id: 101, country: "Malaysia", province: "Kuala Lumpur", city: "Kuala Lumpur", district: "Setapak", lat: 3.1890, lng: 101.7000, aqi: 85, cases: 90, density: "7.500/km²", humidity: 78 },
    { id: 102, country: "Thailand", province: "Bangkok", city: "Bangkok Metropolitan", district: "Pathum Wan", lat: 13.7460, lng: 100.5330, aqi: 155, cases: 260, density: "12.000/km²", humidity: 65 },
    { id: 103, country: "Singapore", province: "Central Singapore", city: "Singapore City", district: "Downtown Core", lat: 1.2868, lng: 103.8545, aqi: 45, cases: 20, density: "8.000/km²", humidity: 80 },

    { id: 1, country: "Indonesia", province: "Riau", city: "Pekanbaru City", district: "Tampan Sub-district", lat: 0.4500, lng: 101.3800, aqi: 185, cases: 380, density: "1.250/km²", humidity: 55 },
    { id: 2, country: "Indonesia", province: "Riau", city: "Pekanbaru City", district: "Bukit Raya Sub-district", lat: 0.4900, lng: 101.4600, aqi: 170, cases: 310, density: "1.420/km²", humidity: 57 },
    { id: 3, country: "Indonesia", province: "Riau", city: "Dumai City", district: "East Dumai Sub-district", lat: 1.6833, lng: 101.4500, aqi: 210, cases: 410, density: "850/km²", humidity: 50 },
    { id: 4, country: "Indonesia", province: "Riau", city: "Bengkalis Regency", district: "Mandau Sub-district", lat: 1.2500, lng: 101.5000, aqi: 195, cases: 350, density: "780/km²", humidity: 53 },

    { id: 5, country: "Indonesia", province: "Central Kalimantan", city: "Palangkaraya City", district: "Pahandut Sub-district", lat: -2.2100, lng: 113.9166, aqi: 160, cases: 290, density: "620/km²", humidity: 60 },
    { id: 6, country: "Indonesia", province: "Central Kalimantan", city: "Palangkaraya City", district: "Jekan Raya Sub-district", lat: -2.2200, lng: 113.9300, aqi: 165, cases: 305, density: "710/km²", humidity: 59 },
    { id: 7, country: "Indonesia", province: "Central Kalimantan", city: "East Kotawaringin Regency", district: "Mentawa Baru Ketapang Sub-district", lat: -2.5333, lng: 112.9500, aqi: 180, cases: 340, density: "540/km²", humidity: 56 },

    { id: 8, country: "Indonesia", province: "West Kalimantan", city: "Pontianak City", district: "Pontianak City Sub-district", lat: -0.0263, lng: 109.3425, aqi: 140, cases: 245, density: "4.100/km²", humidity: 65 },
    { id: 9, country: "Indonesia", province: "West Kalimantan", city: "Pontianak City", district: "South Pontianak Sub-district", lat: -0.0500, lng: 109.3300, aqi: 135, cases: 220, density: "3.900/km²", humidity: 66 },
    { id: 10, country: "Indonesia", province: "West Kalimantan", city: "Kubu Raya Regency", district: "Sungai Raya Sub-district", lat: -0.1500, lng: 109.4000, aqi: 150, cases: 270, density: "950/km²", humidity: 63 },

    { id: 11, country: "Indonesia", province: "South Kalimantan", city: "Banjarmasin City", district: "Central Banjarmasin Sub-district", lat: -3.3166, lng: 114.5901, aqi: 95, cases: 130, density: "9.800/km²", humidity: 75 },
    { id: 12, country: "Indonesia", province: "South Kalimantan", city: "Banjarbaru City", district: "North Banjarbaru Sub-district", lat: -3.4442, lng: 114.8289, aqi: 88, cases: 110, density: "2.100/km²", humidity: 77 },

    { id: 13, country: "Indonesia", province: "Jambi", city: "Jambi City", district: "Telanaipura Sub-district", lat: -1.6101, lng: 103.6131, aqi: 175, cases: 310, density: "2.400/km²", humidity: 58 },
    { id: 14, country: "Indonesia", province: "Jambi", city: "Jambi City", district: "South Jambi Sub-district", lat: -1.6300, lng: 103.6000, aqi: 168, cases: 295, density: "2.800/km²", humidity: 60 },

    { id: 15, country: "Indonesia", province: "East Kalimantan", city: "Samarinda City", district: "Ulu Samarinda Sub-district", lat: -0.5022, lng: 117.1537, aqi: 65, cases: 85, density: "1.800/km²", humidity: 80 },
    { id: 16, country: "Indonesia", province: "East Kalimantan", city: "Balikpapan City", district: "South Balikpapan Sub-district", lat: -1.2654, lng: 116.8312, aqi: 50, cases: 45, density: "3.500/km²", humidity: 83 },

    { id: 17, country: "Indonesia", province: "DKI Jakarta", city: "Central Jakarta City", district: "Menteng Sub-district", lat: -6.1751, lng: 106.8650, aqi: 110, cases: 190, density: "19.500/km²", humidity: 70 },
    { id: 18, country: "Indonesia", province: "DKI Jakarta", city: "South Jakarta City", district: "Kebayoran Baru Sub-district", lat: -6.2415, lng: 106.7994, aqi: 105, cases: 175, density: "14.200/km²", humidity: 72 },

    { id: 19, country: "Indonesia", province: "East Java", city: "Surabaya City", district: "Gubeng Sub-district", lat: -7.2756, lng: 112.7508, aqi: 75, cases: 95, density: "8.400/km²", humidity: 72 },
    { id: 20, country: "Indonesia", province: "East Java", city: "Banyuwangi Regency", district: "Banyuwangi Sub-district", lat: -8.2192, lng: 114.3691, aqi: 42, cases: 30, density: "720/km²", humidity: 82 },
    { id: 21, country: "Indonesia", province: "East Java", city: "Banyuwangi Regency", district: "Rogojampi Sub-district", lat: -8.3200, lng: 114.3100, aqi: 45, cases: 35, density: "850/km²", humidity: 80 }
];

let markersLayer = L.layerGroup().addTo(map);
let currentFilteredData = [];
let isPythonModelActive = false;

const countrySelect = document.getElementById('country-select');
const provinceSelect = document.getElementById('province-select');
const citySelect = document.getElementById('city-select');
const districtSelect = document.getElementById('district-select');
const riskFilter = document.getElementById('risk-filter');

async function initializeModelAndData() {
    const detailBox = document.getElementById('region-detail');
    if (detailBox) {
        detailBox.innerHTML = `<h3>Loading AI Analysis...</h3><p class="placeholder-text">Detecting Python Random Forest model server...</p>`;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ regions: ispaData }),
            signal: AbortSignal.timeout(2500)
        });

        const result = await response.json();

        if (result.status === 'success') {
            ispaData = result.data;
            isPythonModelActive = true;
            console.log("Successfully connected to Python Model (.pkl) Flask API.");
        } else {
            throw new Error("Invalid API response format");
        }
    } catch (error) {
        console.warn("Python server not detected. Enabling Standalone Random Forest Fallback Logic (JS).");
        isPythonModelActive = false;

        ispaData.forEach(item => {
            let densityVal = parseFloat(item.density.replace('.', '').replace('/km²', ''));
            let fallbackResult = fallbackPredictByRFWeights(item.aqi, item.cases, densityVal, item.humidity);
            item.riskScore = fallbackResult.score;
            item.level = fallbackResult.level;
        });
    }

    currentFilteredData = [...ispaData];
    if (detailBox) {
        const sourceBadge = isPythonModelActive 
            ? '<span class="badge bg-success">Python Model (.pkl) Active</span>' 
            : '<span class="badge bg-warning text-dark">Standalone Mode (RF Fallback Active)</span>';

        detailBox.innerHTML = `
            <h3>Region Details</h3>
            <p class="placeholder-text mb-2">Select a region from the list or click a point on the map to view analysis.</p>
            <div>${sourceBadge}</div>
        `;
    }

    initDropdowns();
    renderMapData(currentFilteredData);
}

function initDropdowns() {
    const countries = [...new Set(ispaData.map(item => item.country))];
    if (countrySelect) {
        countrySelect.innerHTML = '<option value="all">-- All Countries --</option>';
        countries.forEach(cnt => {
            const opt = document.createElement('option');
            opt.value = cnt;
            opt.textContent = cnt;
            countrySelect.appendChild(opt);
        });
    }

    provinceSelect.innerHTML = '<option value="all">-- All Provinces --</option>';
    const provinces = [...new Set(ispaData.map(item => item.province))];
    provinces.forEach(prov => {
        const opt = document.createElement('option');
        opt.value = prov;
        opt.textContent = prov;
        provinceSelect.appendChild(opt);
    });
}

if (countrySelect) {
    countrySelect.addEventListener('change', function() {
        const selectedCountry = this.value;
        provinceSelect.innerHTML = '<option value="all">-- All Provinces --</option>';
        citySelect.innerHTML = '<option value="all">-- All Regencies/Cities --</option>';
        districtSelect.innerHTML = '<option value="all">-- All Districts --</option>';

        let filteredProv = selectedCountry === 'all' ? ispaData : ispaData.filter(i => i.country === selectedCountry);
        let provinces = [...new Set(filteredProv.map(i => i.province))];
        provinces.forEach(prov => {
            const opt = document.createElement('option');
            opt.value = prov;
            opt.textContent = prov;
            provinceSelect.appendChild(opt);
        });
        filterData();
    });
}

provinceSelect.addEventListener('change', function() {
    const selectedProv = this.value;
    citySelect.innerHTML = '<option value="all">-- All Regencies/Cities --</option>';
    districtSelect.innerHTML = '<option value="all">-- All Districts --</option>';

    if (selectedProv !== 'all') {
        const cities = [...new Set(ispaData.filter(i => i.province === selectedProv).map(i => i.city))];
        cities.forEach(city => {
            const opt = document.createElement('option');
            opt.value = city;
            opt.textContent = city;
            citySelect.appendChild(opt);
        });
    }
    filterData();
});

citySelect.addEventListener('change', function() {
    const selectedCity = this.value;
    districtSelect.innerHTML = '<option value="all">-- All Districts --</option>';

    if (selectedCity !== 'all') {
        const districts = [...new Set(ispaData.filter(i => i.city === selectedCity).map(i => i.district))];
        districts.forEach(dist => {
            const opt = document.createElement('option');
            opt.value = dist;
            opt.textContent = dist;
            districtSelect.appendChild(opt);
        });
    }
    filterData();
});

districtSelect.addEventListener('change', filterData);
riskFilter.addEventListener('change', filterData);

function getRiskColor(level) {
    if (level === 'high') return '#ef4444';
    if (level === 'medium') return '#f59e0b';
    return '#10b981';
}

function getRiskLabel(level) {
    if (level === 'high') return 'High';
    if (level === 'medium') return 'Medium';
    return 'Low';
}

function showRegionDetail(item) {
    const detailBox = document.getElementById('region-detail');
    if (!detailBox) return;
    const badgeColor = getRiskColor(item.level);
    const modelSourceText = isPythonModelActive ? 'Python Model (.pkl)' : 'RF Fallback (JS)';
    
    detailBox.innerHTML = `
        <h3>${item.district}</h3>
        <p class="small text-muted mb-2">${item.city}, ${item.province}, ${item.country}</p>
        <ul class="detail-list">
            <li>
                <span>Risk Status (${modelSourceText})</span>
                <strong style="color: ${badgeColor}">${getRiskLabel(item.level)} (${item.riskScore}/100)</strong>
            </li>
            <li>
                <span>Weekly Active Cases</span>
                <strong>${item.cases} Cases</strong>
            </li>
            <li>
                <span>AQI / PM2.5 (NASA GEOS-CF)</span>
                <strong>${item.aqi} µg/m³</strong>
            </li>
            <li>
                <span>Density (WorldPop 2020)</span>
                <strong>${item.density}</strong>
            </li>
            <li>
                <span>Air Humidity</span>
                <strong>${item.humidity}%</strong>
            </li>
        </ul>
    `;
}

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
            fillOpacity: 0.4,
            radius: item.riskScore * 18
        });

        circle.bindPopup(`
            <strong>${item.district}, ${item.city}</strong><br>
            Risk: <b>${getRiskLabel(item.level)}</b> (Score: ${item.riskScore})<br>
            NASA AQI: ${item.aqi} | Cases: ${item.cases}
        `);

        circle.on('click', () => {
            showRegionDetail(item);
        });

        markersLayer.addLayer(circle);
    });

    const elHigh = document.getElementById('count-high');
    const elMed = document.getElementById('count-medium');
    const elLow = document.getElementById('count-low');
    if (elHigh) elHigh.textContent = countHigh;
    if (elMed) elMed.textContent = countMedium;
    if (elLow) elLow.textContent = countLow;
}

function filterData() {
    const selectedRisk = riskFilter ? riskFilter.value : 'all';
    const selectedCountry = countrySelect && countrySelect.value ? countrySelect.value : 'all';
    const selectedProv = provinceSelect.value;
    const selectedCity = citySelect.value;
    const selectedDist = districtSelect.value;

    currentFilteredData = ispaData.filter(item => {
        const matchesRisk = selectedRisk === 'all' || item.level === selectedRisk;
        const matchesCountry = selectedCountry === 'all' || item.country === selectedCountry;
        const matchesProv = selectedProv === 'all' || item.province === selectedProv;
        const matchesCity = selectedCity === 'all' || item.city === selectedCity;
        const matchesDist = selectedDist === 'all' || item.district === selectedDist;

        return matchesRisk && matchesCountry && matchesProv && matchesCity && matchesDist;
    });

    renderMapData(currentFilteredData);

    if (currentFilteredData.length > 0) {
        if (selectedDist !== 'all') {
            const target = currentFilteredData.find(i => i.district === selectedDist);
            if (target) {
                map.setView([target.lat, target.lng], 12);
                showRegionDetail(target);
            }
        } else if (selectedCity !== 'all') {
            const target = currentFilteredData[0];
            map.setView([target.lat, target.lng], 9);
        } else if (selectedProv !== 'all') {
            const target = currentFilteredData[0];
            map.setView([target.lat, target.lng], 7);
        } else if (selectedCountry !== 'all') {
            const target = currentFilteredData[0];
            map.setView([target.lat, target.lng], 5);
        } else {
            map.setView([15.0, 0.0], 2);
        }
    }
}

const btnExport = document.getElementById('btn-export');
if (btnExport) {
    btnExport.addEventListener('click', () => {
        if (currentFilteredData.length === 0) {
            alert("No matching region data to export!");
            return;
        }

        let csvContent = "data:text/csv;charset=utf-8,ID,Country,Province,Regency/City,District,Risk Score,Risk Level,Weekly Cases,AQI (NASA),Density (WorldPop),Humidity\n";
        
        currentFilteredData.forEach(item => {
            csvContent += `\"${item.id}\",\"${item.country}\",\"${item.province}\",\"${item.city}\",\"${item.district}\",\"${item.riskScore}\",\"${getRiskLabel(item.level)}\",\"${item.cases}\",\"${item.aqi}\",\"${item.density}\",\"${item.humidity}%\"\n`;
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "selected_ari_risk_analysis.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
}

initializeModelAndData();