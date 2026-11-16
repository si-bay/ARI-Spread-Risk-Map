from flask import Flask, jsonify
from flask_cors import CORS
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import time

app = Flask(__name__)
CORS(app)


REGIONS = [
    {"id": 1001, "country": "Malaysia", "province": "Kuala Lumpur", "city": "Kuala Lumpur", "district": "Setapak", "lat": 3.1890, "lng": 101.7000},
    {"id": 102, "country": "Thailand", "province": "Bangkok", "city": "Bangkok Metropolitan", "district": "Pathum Wan", "lat": 13.7460, "lng": 100.5330},
    {"id": 103, "country": "Singapore", "province": "Central Singapore", "city": "Singapore City", "district": "Downtown Core", "lat": 1.2868, "lng": 103.8545},

    {"id": 1, "country": "Indonesia", "province": "Riau", "city": "Pekanbaru City", "district": "Tampan Sub-district", "lat": 0.4500, "lng": 101.3800},
    {"id": 2, "country": "Indonesia", "province": "Riau", "city": "Pekanbaru City", "district": "Bukit Raya Sub-district", "lat": 0.4900, "lng": 101.4600},
    {"id": 3, "country": "Indonesia", "province": "Riau", "city": "Dumai City", "district": "East Dumai Sub-district", "lat": 1.6833, "lng": 101.4500},
    {"id": 4, "country": "Indonesia", "province": "Riau", "city": "Bengkalis Regency", "district": "Mandau Sub-district", "lat": 1.2500, "lng": 101.5000},
    {"id": 5, "country": "Indonesia", "province": "Central Kalimantan", "city": "Palangkaraya City", "district": "Pahandut Sub-district", "lat": -2.2100, "lng": 113.9166},
    {"id": 6, "country": "Indonesia", "province": "Central Kalimantan", "city": "Palangkaraya City", "district": "Jekan Raya Sub-district", "lat": -2.2200, "lng": 113.9300},
    {"id": 7, "country": "Indonesia", "province": "Central Kalimantan", "city": "East Kotawaringin Regency", "district": "Mentawa Baru Ketapang Sub-district", "lat": -2.5333, "lng": 112.9500},
    {"id": 8, "country": "Indonesia", "province": "West Kalimantan", "city": "Pontianak City", "district": "Pontianak City Sub-district", "lat": -0.0263, "lng": 109.3425},
    {"id": 9, "country": "Indonesia", "province": "West Kalimantan", "city": "Pontianak City", "district": "South Pontianak Sub-district", "lat": -0.0500, "lng": 109.3300},
    {"id": 10, "country": "Indonesia", "province": "West Kalimantan", "city": "Kubu Raya Regency", "district": "Sungai Raya Sub-district", "lat": -0.1500, "lng": 109.4000},
    {"id": 11, "country": "Indonesia", "province": "South Kalimantan", "city": "Banjarmasin City", "district": "Central Banjarmasin Sub-district", "lat": -3.3166, "lng": 114.5901},
    {"id": 12, "country": "Indonesia", "province": "South Kalimantan", "city": "Banjarbaru City", "district": "North Banjarbaru Sub-district", "lat": -3.4442, "lng": 114.8289},
    {"id": 13, "country": "Indonesia", "province": "Jambi", "city": "Jambi City", "district": "Telanaipura Sub-district", "lat": -1.6101, "lng": 103.6131},
    {"id": 14, "country": "Indonesia", "province": "Jambi", "city": "Jambi City", "district": "South Jambi Sub-district", "lat": -1.6300, "lng": 103.6000},
    {"id": 15, "country": "Indonesia", "province": "East Kalimantan", "city": "Samarinda City", "district": "Ulu Samarinda Sub-district", "lat": -0.5022, "lng": 117.1537},
    {"id": 16, "country": "Indonesia", "province": "East Kalimantan", "city": "Balikpapan City", "district": "South Balikpapan Sub-district", "lat": -1.2654, "lng": 116.8312},
    {"id": 17, "country": "Indonesia", "province": "DKI Jakarta", "city": "Central Jakarta City", "district": "Menteng Sub-district", "lat": -6.1751, "lng": 106.8650},
    {"id": 18, "country": "Indonesia", "province": "DKI Jakarta", "city": "South Jakarta City", "district": "Kebayoran Baru Sub-district", "lat": -6.2415, "lng": 106.7994},
    {"id": 19, "country": "Indonesia", "province": "East Java", "city": "Surabaya City", "district": "Gubeng Sub-district", "lat": -7.2756, "lng": 112.7508},
    {"id": 20, "country": "Indonesia", "province": "East Java", "city": "Banyuwangi Regency", "district": "Banyuwangi Sub-district", "lat": -8.2192, "lng": 114.3691},
    {"id": 21, "country": "Indonesia", "province": "East Java", "city": "Banyuwangi Regency", "district": "Rogojampi Sub-district", "lat": -8.3200, "lng": 114.3100},

    {"id": 22, "country": "Indonesia", "province": "Aceh", "city": "Banda Aceh City", "district": "Baiturrahman District", "lat": 5.5483, "lng": 95.3238},
    {"id": 23, "country": "Indonesia", "province": "North Sumatra", "city": "Medan City", "district": "Medan Baru District", "lat": 3.5670, "lng": 98.6563},
    {"id": 24, "country": "Indonesia", "province": "West Sumatra", "city": "Padang City", "district": "Padang Barat District", "lat": -0.9492, "lng": 100.3543},
    {"id": 25, "country": "Indonesia", "province": "South Sumatra", "city": "Palembang City", "district": "Ilir Timur I District", "lat": -2.9761, "lng": 104.7754},
    {"id": 26, "country": "Indonesia", "province": "Lampung", "city": "Bandar Lampung City", "district": "Enggal District", "lat": -5.4292, "lng": 105.2625},
    {"id": 27, "country": "Indonesia", "province": "Banten", "city": "Serang City", "district": "Serang District", "lat": -6.1200, "lng": 106.1503},
    {"id": 28, "country": "Indonesia", "province": "West Java", "city": "Bandung City", "district": "Sumur Bandung District", "lat": -6.9175, "lng": 107.6191},
    {"id": 29, "country": "Indonesia", "province": "Central Java", "city": "Semarang City", "district": "Semarang Tengah District", "lat": -6.9904, "lng": 110.4229},
    {"id": 30, "country": "Indonesia", "province": "Special Region of Yogyakarta", "city": "Yogyakarta City", "district": "Gondokusuman District", "lat": -7.7829, "lng": 110.3671},
    {"id": 31, "country": "Indonesia", "province": "Bali", "city": "Denpasar City", "district": "Denpasar Barat District", "lat": -8.6705, "lng": 115.2126},
    {"id": 32, "country": "Indonesia", "province": "West Nusa Tenggara", "city": "Mataram City", "district": "Selaparang District", "lat": -8.5833, "lng": 116.1167},
    {"id": 33, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Kupang City", "district": "Kota Raja District", "lat": -10.1772, "lng": 123.6070},
    {"id": 34, "country": "Indonesia", "province": "Central Sulawesi", "city": "Palu City", "district": "Palu Timur District", "lat": -0.8917, "lng": 119.8707},
    {"id": 35, "country": "Indonesia", "province": "South Sulawesi", "city": "Makassar City", "district": "Panakkukang District", "lat": -5.1550, "lng": 119.4370},
    {"id": 36, "country": "Indonesia", "province": "North Sulawesi", "city": "Manado City", "district": "Wenang District", "lat": 1.4900, "lng": 124.8420},
    {"id": 37, "country": "Indonesia", "province": "Gorontalo", "city": "Gorontalo City", "district": "Kota Selatan District", "lat": 0.5375, "lng": 123.0595},
    {"id": 38, "country": "Indonesia", "province": "Southeast Sulawesi", "city": "Kendari City", "district": "Mandonga District", "lat": -3.9722, "lng": 122.5149},
    {"id": 39, "country": "Indonesia", "province": "Maluku", "city": "Ambon City", "district": "Sirimau District", "lat": -3.6954, "lng": 128.1814},
    {"id": 40, "country": "Indonesia", "province": "North Maluku", "city": "Ternate City", "district": "Ternate Tengah District", "lat": 0.7893, "lng": 127.3842},
    {"id": 41, "country": "Indonesia", "province": "Papua", "city": "Jayapura City", "district": "Jayapura Utara District", "lat": -2.5337, "lng": 140.7181},

    {"id": 42, "country": "Indonesia", "province": "Aceh", "city": "Lhokseumawe City", "district": "Banda Sakti District", "lat": 5.1801, "lng": 97.1507},
    {"id": 43, "country": "Indonesia", "province": "North Sumatra", "city": "Binjai City", "district": "Binjai Kota District", "lat": 3.6001, "lng": 98.4854},
    {"id": 44, "country": "Indonesia", "province": "North Sumatra", "city": "Pematangsiantar City", "district": "Siantar Barat District", "lat": 2.9595, "lng": 99.0687},
    {"id": 45, "country": "Indonesia", "province": "West Sumatra", "city": "Bukittinggi City", "district": "Guguk Panjang District", "lat": -0.3050, "lng": 100.3692},
    {"id": 46, "country": "Indonesia", "province": "West Sumatra", "city": "Payakumbuh City", "district": "Payakumbuh Barat District", "lat": -0.2280, "lng": 100.6300},
    {"id": 47, "country": "Indonesia", "province": "South Sumatra", "city": "Lubuklinggau City", "district": "Lubuklinggau Barat I District", "lat": -3.2967, "lng": 102.8617},
    {"id": 48, "country": "Indonesia", "province": "South Sumatra", "city": "Prabumulih City", "district": "Prabumulih Barat District", "lat": -3.4320, "lng": 104.2350},
    {"id": 49, "country": "Indonesia", "province": "Lampung", "city": "Metro City", "district": "Metro Pusat District", "lat": -5.1130, "lng": 105.3067},
    {"id": 50, "country": "Indonesia", "province": "Banten", "city": "Cilegon City", "district": "Jombang District", "lat": -6.0160, "lng": 106.0550},
    {"id": 51, "country": "Indonesia", "province": "Banten", "city": "Tangerang City", "district": "Tangerang District", "lat": -6.1783, "lng": 106.6319},
    {"id": 52, "country": "Indonesia", "province": "Banten", "city": "South Tangerang City", "district": "Serpong District", "lat": -6.2889, "lng": 106.7178},
    {"id": 53, "country": "Indonesia", "province": "West Java", "city": "Bogor City", "district": "Bogor Tengah District", "lat": -6.5950, "lng": 106.8166},
    {"id": 54, "country": "Indonesia", "province": "West Java", "city": "Bekasi City", "district": "Bekasi Selatan District", "lat": -6.2383, "lng": 106.9756},
    {"id": 55, "country": "Indonesia", "province": "West Java", "city": "Depok City", "district": "Pancoran Mas District", "lat": -6.4025, "lng": 106.7942},
    {"id": 56, "country": "Indonesia", "province": "West Java", "city": "Cirebon City", "district": "Kejaksan District", "lat": -6.7063, "lng": 108.5570},
    {"id": 57, "country": "Indonesia", "province": "West Java", "city": "Tasikmalaya City", "district": "Cihideung District", "lat": -7.3274, "lng": 108.2207},
    {"id": 58, "country": "Indonesia", "province": "Central Java", "city": "Surakarta City", "district": "Laweyan District", "lat": -7.5666, "lng": 110.8167},
    {"id": 59, "country": "Indonesia", "province": "Central Java", "city": "Magelang City", "district": "Magelang Tengah District", "lat": -7.4797, "lng": 110.2177},
    {"id": 60, "country": "Indonesia", "province": "Central Java", "city": "Salatiga City", "district": "Sidorejo District", "lat": -7.3305, "lng": 110.5084},
    {"id": 61, "country": "Indonesia", "province": "Central Java", "city": "Pekalongan City", "district": "Pekalongan Barat District", "lat": -6.8898, "lng": 109.6753},
    {"id": 62, "country": "Indonesia", "province": "Central Java", "city": "Tegal City", "district": "Tegal Barat District", "lat": -6.8694, "lng": 109.1402},
    {"id": 63, "country": "Indonesia", "province": "Central Java", "city": "Purwokerto", "district": "Purwokerto Timur District", "lat": -7.4243, "lng": 109.2396},
    {"id": 64, "country": "Indonesia", "province": "Central Java", "city": "Cilacap Regency", "district": "Cilacap Selatan District", "lat": -7.7270, "lng": 109.0090},
    {"id": 65, "country": "Indonesia", "province": "East Java", "city": "Malang City", "district": "Klojen District", "lat": -7.9666, "lng": 112.6326},
    {"id": 66, "country": "Indonesia", "province": "East Java", "city": "Kediri City", "district": "Kota District", "lat": -7.8167, "lng": 112.0167},
    {"id": 67, "country": "Indonesia", "province": "East Java", "city": "Jember Regency", "district": "Sumbersari District", "lat": -8.1724, "lng": 113.7000},
    {"id": 68, "country": "Indonesia", "province": "East Java", "city": "Probolinggo City", "district": "Kanigaran District", "lat": -7.7543, "lng": 113.2159},
    {"id": 69, "country": "Indonesia", "province": "East Java", "city": "Madiun City", "district": "Manguharjo District", "lat": -7.6298, "lng": 111.5239},
    {"id": 70, "country": "Indonesia", "province": "East Java", "city": "Sidoarjo Regency", "district": "Sidoarjo District", "lat": -7.4478, "lng": 112.7183},
    {"id": 71, "country": "Indonesia", "province": "East Java", "city": "Gresik Regency", "district": "Gresik District", "lat": -7.1567, "lng": 112.6555},
    {"id": 72, "country": "Indonesia", "province": "East Java", "city": "Batu City", "district": "Batu District", "lat": -7.8712, "lng": 112.5263},
    {"id": 73, "country": "Indonesia", "province": "Bali", "city": "Singaraja", "district": "Buleleng District", "lat": -8.1120, "lng": 115.0882},
    {"id": 74, "country": "Indonesia", "province": "West Nusa Tenggara", "city": "Bima City", "district": "Rasanae Barat District", "lat": -8.4600, "lng": 118.7267},
    {"id": 75, "country": "Indonesia", "province": "West Nusa Tenggara", "city": "Sumbawa Besar", "district": "Sumbawa District", "lat": -8.4932, "lng": 117.4200},
    {"id": 76, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Ende Regency", "district": "Ende Tengah District", "lat": -8.8432, "lng": 121.6623},
    {"id": 77, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Maumere", "district": "Alok District", "lat": -8.6199, "lng": 122.2111},
    {"id": 78, "country": "Indonesia", "province": "North Sulawesi", "city": "Bitung City", "district": "Maesa District", "lat": 1.4451, "lng": 125.1824},
    {"id": 79, "country": "Indonesia", "province": "North Sulawesi", "city": "Tomohon City", "district": "Tomohon Tengah District", "lat": 1.3220, "lng": 124.8380},
    {"id": 80, "country": "Indonesia", "province": "South Sulawesi", "city": "Parepare City", "district": "Ujung District", "lat": -4.0135, "lng": 119.6255},
    {"id": 81, "country": "Indonesia", "province": "South Sulawesi", "city": "Palopo City", "district": "Wara District", "lat": -2.9920, "lng": 120.1960},
    {"id": 82, "country": "Indonesia", "province": "Southeast Sulawesi", "city": "Bau-Bau City", "district": "Wolio District", "lat": -5.4667, "lng": 122.6333},
    {"id": 83, "country": "Indonesia", "province": "North Kalimantan", "city": "Tarakan City", "district": "Tarakan Barat District", "lat": 3.3000, "lng": 117.6333},
    {"id": 84, "country": "Indonesia", "province": "West Kalimantan", "city": "Singkawang City", "district": "Singkawang Barat District", "lat": 0.9060, "lng": 108.9872},
    {"id": 85, "country": "Indonesia", "province": "West Kalimantan", "city": "Ketapang Regency", "district": "Delta Pawan District", "lat": -1.8500, "lng": 109.9833},
    {"id": 86, "country": "Indonesia", "province": "Central Kalimantan", "city": "Pangkalan Bun", "district": "Arut Selatan District", "lat": -2.6833, "lng": 111.6167},
    {"id": 87, "country": "Indonesia", "province": "North Kalimantan", "city": "Tanjung Selor", "district": "Tanjung Selor District", "lat": 2.8375, "lng": 117.3653},
    {"id": 88, "country": "Indonesia", "province": "Southwest Papua", "city": "Sorong City", "district": "Sorong District", "lat": -0.8762, "lng": 131.2558},
    {"id": 89, "country": "Indonesia", "province": "West Papua", "city": "Manokwari Regency", "district": "West Manokwari District", "lat": -0.8615, "lng": 134.0620},
    {"id": 90, "country": "Indonesia", "province": "Central Papua", "city": "Nabire Regency", "district": "Nabire District", "lat": -3.3667, "lng": 135.4833},
    {"id": 91, "country": "Indonesia", "province": "South Papua", "city": "Merauke Regency", "district": "Merauke District", "lat": -8.4932, "lng": 140.4018},

    {"id": 92, "country": "Indonesia", "province": "Aceh", "city": "Meulaboh", "district": "Johan Pahlawan District", "lat": 4.1440, "lng": 96.1285},
    {"id": 93, "country": "Indonesia", "province": "Aceh", "city": "Langsa City", "district": "Langsa Kota District", "lat": 4.4683, "lng": 97.9683},
    {"id": 94, "country": "Indonesia", "province": "Aceh", "city": "Takengon", "district": "Lut Tawar District", "lat": 4.6296, "lng": 96.8414},
    {"id": 95, "country": "Indonesia", "province": "North Sumatra", "city": "Sibolga City", "district": "Sibolga Kota District", "lat": 1.7400, "lng": 98.7833},
    {"id": 96, "country": "Indonesia", "province": "North Sumatra", "city": "Tebing Tinggi City", "district": "Tebing Tinggi Kota District", "lat": 3.3274, "lng": 99.1623},
    {"id": 97, "country": "Indonesia", "province": "North Sumatra", "city": "Gunungsitoli City", "district": "Gunungsitoli District", "lat": 1.2888, "lng": 97.6143},
    {"id": 98, "country": "Indonesia", "province": "Riau", "city": "Rengat", "district": "Rengat District", "lat": -0.3730, "lng": 102.5480},
    {"id": 99, "country": "Indonesia", "province": "Riau", "city": "Tembilahan", "district": "Tembilahan District", "lat": -0.3228, "lng": 103.1590},
    {"id": 100, "country": "Indonesia", "province": "Riau", "city": "Siak Sri Indrapura", "district": "Siak District", "lat": 0.7930, "lng": 102.0450},
    {"id": 101, "country": "Indonesia", "province": "Riau Islands", "city": "Batam City", "district": "Batam Kota District", "lat": 1.1191, "lng": 104.0530},
    {"id": 102, "country": "Indonesia", "province": "Riau Islands", "city": "Tanjungpinang City", "district": "Tanjungpinang Kota District", "lat": 0.9186, "lng": 104.4665},
    {"id": 103, "country": "Indonesia", "province": "Jambi", "city": "Sungai Penuh City", "district": "Sungai Penuh District", "lat": -2.0631, "lng": 101.3910},
    {"id": 104, "country": "Indonesia", "province": "Bengkulu", "city": "Bengkulu City", "district": "Ratu Samban District", "lat": -3.8004, "lng": 102.2655},
    {"id": 105, "country": "Indonesia", "province": "Bengkulu", "city": "Curup", "district": "Curup District", "lat": -3.4667, "lng": 102.5333},
    {"id": 106, "country": "Indonesia", "province": "Bangka Belitung Islands", "city": "Pangkalpinang City", "district": "Taman Sari District", "lat": -2.1291, "lng": 106.1138},
    {"id": 107, "country": "Indonesia", "province": "Bangka Belitung Islands", "city": "Tanjung Pandan", "district": "Tanjung Pandan District", "lat": -2.7411, "lng": 107.6348},
    {"id": 108, "country": "Indonesia", "province": "South Sumatra", "city": "Sekayu", "district": "Sekayu District", "lat": -2.8720, "lng": 103.8460},
    {"id": 109, "country": "Indonesia", "province": "Lampung", "city": "Kalianda", "district": "Kalianda District", "lat": -5.7380, "lng": 105.5910},
    {"id": 110, "country": "Indonesia", "province": "Banten", "city": "Rangkasbitung", "district": "Rangkasbitung District", "lat": -6.3590, "lng": 106.2490},
    {"id": 111, "country": "Indonesia", "province": "West Java", "city": "Cianjur", "district": "Cianjur District", "lat": -6.8170, "lng": 107.1390},
    {"id": 112, "country": "Indonesia", "province": "West Java", "city": "Sukabumi City", "district": "Cikole District", "lat": -6.9277, "lng": 106.9290},
    {"id": 113, "country": "Indonesia", "province": "West Java", "city": "Purwakarta", "district": "Purwakarta District", "lat": -6.5560, "lng": 107.4430},
    {"id": 114, "country": "Indonesia", "province": "West Java", "city": "Garut", "district": "Garut Kota District", "lat": -7.2167, "lng": 107.9000},
    {"id": 115, "country": "Indonesia", "province": "Central Java", "city": "Pati", "district": "Pati District", "lat": -6.7550, "lng": 111.0380},
    {"id": 116, "country": "Indonesia", "province": "Central Java", "city": "Kudus", "district": "Kota Kudus District", "lat": -6.8048, "lng": 110.8405},
    {"id": 117, "country": "Indonesia", "province": "Central Java", "city": "Rembang", "district": "Rembang District", "lat": -6.7090, "lng": 111.3410},
    {"id": 118, "country": "Indonesia", "province": "Central Java", "city": "Wonosobo", "district": "Wonosobo District", "lat": -7.3620, "lng": 109.9000},
    {"id": 119, "country": "Indonesia", "province": "East Java", "city": "Blitar City", "district": "Sananwetan District", "lat": -8.0983, "lng": 112.1681},
    {"id": 120, "country": "Indonesia", "province": "East Java", "city": "Pasuruan City", "district": "Panggungrejo District", "lat": -7.6453, "lng": 112.9075},
    {"id": 121, "country": "Indonesia", "province": "East Java", "city": "Lumajang", "district": "Lumajang District", "lat": -8.1335, "lng": 113.2240},
    {"id": 122, "country": "Indonesia", "province": "East Java", "city": "Bondowoso", "district": "Bondowoso District", "lat": -7.9135, "lng": 113.8215},
    {"id": 123, "country": "Indonesia", "province": "Bali", "city": "Tabanan", "district": "Tabanan District", "lat": -8.5413, "lng": 115.1252},
    {"id": 124, "country": "Indonesia", "province": "West Nusa Tenggara", "city": "Praya", "district": "Praya District", "lat": -8.7050, "lng": 116.2700},
    {"id": 125, "country": "Indonesia", "province": "West Nusa Tenggara", "city": "Dompu", "district": "Dompu District", "lat": -8.5360, "lng": 118.4630},
    {"id": 126, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Ruteng", "district": "Langke Rembong District", "lat": -8.6130, "lng": 120.4630},
    {"id": 127, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Waingapu", "district": "Kota Waingapu District", "lat": -9.6567, "lng": 120.2640},
    {"id": 128, "country": "Indonesia", "province": "West Kalimantan", "city": "Putussibau", "district": "Putussibau Utara District", "lat": 0.8480, "lng": 112.9320},
    {"id": 129, "country": "Indonesia", "province": "West Kalimantan", "city": "Sintang", "district": "Sintang District", "lat": 0.0680, "lng": 111.4980},
    {"id": 130, "country": "Indonesia", "province": "Central Kalimantan", "city": "Kuala Kapuas", "district": "Selat District", "lat": -3.0090, "lng": 114.3870},
    {"id": 131, "country": "Indonesia", "province": "East Kalimantan", "city": "Bontang City", "district": "Bontang Utara District", "lat": 0.1333, "lng": 117.5000},
    {"id": 132, "country": "Indonesia", "province": "East Kalimantan", "city": "Tenggarong", "district": "Tenggarong District", "lat": -0.4260, "lng": 116.9870},
    {"id": 133, "country": "Indonesia", "province": "East Kalimantan", "city": "Tanah Grogot", "district": "Tanah Grogot District", "lat": -1.9000, "lng": 116.2000},
    {"id": 134, "country": "Indonesia", "province": "Central Sulawesi", "city": "Tolitoli", "district": "Baolan District", "lat": 1.0410, "lng": 120.8160},
    {"id": 135, "country": "Indonesia", "province": "Central Sulawesi", "city": "Luwuk", "district": "Luwuk District", "lat": -0.9510, "lng": 122.7870},
    {"id": 136, "country": "Indonesia", "province": "West Sulawesi", "city": "Mamuju", "district": "Mamuju District", "lat": -2.6740, "lng": 118.8880},
    {"id": 137, "country": "Indonesia", "province": "West Sulawesi", "city": "Majene", "district": "Banggae District", "lat": -3.5400, "lng": 118.9700},
    {"id": 138, "country": "Indonesia", "province": "Maluku", "city": "Masohi", "district": "Kota Masohi District", "lat": -3.3000, "lng": 128.9670},
    {"id": 139, "country": "Indonesia", "province": "Maluku", "city": "Tual City", "district": "Dullah Selatan District", "lat": -5.6270, "lng": 132.7520},
    {"id": 140, "country": "Indonesia", "province": "North Maluku", "city": "Tobelo", "district": "Tobelo District", "lat": 1.7280, "lng": 128.0090},
    {"id": 141, "country": "Indonesia", "province": "Highland Papua", "city": "Wamena", "district": "Wamena District", "lat": -4.0950, "lng": 138.9470},

    {"id": 142, "country": "Indonesia", "province": "Aceh", "city": "Sabang City", "district": "Sukakarya District", "lat": 5.8930, "lng": 95.3230},
    {"id": 143, "country": "Indonesia", "province": "Aceh", "city": "Subulussalam City", "district": "Simpang Kiri District", "lat": 2.6420, "lng": 98.0000},
    {"id": 144, "country": "Indonesia", "province": "North Sumatra", "city": "Padangsidimpuan City", "district": "Padangsidimpuan Utara District", "lat": 1.3730, "lng": 99.2680},
    {"id": 145, "country": "Indonesia", "province": "North Sumatra", "city": "Kabanjahe", "district": "Kabanjahe District", "lat": 3.1000, "lng": 98.4900},
    {"id": 146, "country": "Indonesia", "province": "North Sumatra", "city": "Stabat", "district": "Stabat District", "lat": 3.7610, "lng": 98.4510},
    {"id": 147, "country": "Indonesia", "province": "Riau", "city": "Pangkalan Kerinci", "district": "Pangkalan Kerinci District", "lat": 0.4410, "lng": 101.8580},
    {"id": 148, "country": "Indonesia", "province": "Riau", "city": "Bagansiapiapi", "district": "Bangko District", "lat": 2.1570, "lng": 100.8160},
    {"id": 149, "country": "Indonesia", "province": "Riau", "city": "Teluk Kuantan", "district": "Kuantan Tengah District", "lat": -0.5250, "lng": 101.5660},
    {"id": 150, "country": "Indonesia", "province": "Jambi", "city": "Muara Bungo", "district": "Pasar Muara Bungo District", "lat": -1.4950, "lng": 102.1350},
    {"id": 151, "country": "Indonesia", "province": "Jambi", "city": "Kuala Tungkal", "district": "Tungkal Ilir District", "lat": -0.8170, "lng": 103.4660},
    {"id": 152, "country": "Indonesia", "province": "Bengkulu", "city": "Manna", "district": "Kota Manna District", "lat": -4.4660, "lng": 103.0000},
    {"id": 153, "country": "Indonesia", "province": "Bengkulu", "city": "Arga Makmur", "district": "Arga Makmur District", "lat": -3.4330, "lng": 102.1830},
    {"id": 154, "country": "Indonesia", "province": "Lampung", "city": "Liwa", "district": "Balik Bukit District", "lat": -5.0330, "lng": 104.0670},
    {"id": 155, "country": "Indonesia", "province": "Lampung", "city": "Menggala", "district": "Menggala District", "lat": -4.4670, "lng": 105.2170},
    {"id": 156, "country": "Indonesia", "province": "Bangka Belitung Islands", "city": "Toboali", "district": "Toboali District", "lat": -3.0170, "lng": 106.4500},
    {"id": 157, "country": "Indonesia", "province": "Bangka Belitung Islands", "city": "Sungailiat", "district": "Sungailiat District", "lat": -1.8500, "lng": 106.1170},
    {"id": 158, "country": "Indonesia", "province": "Banten", "city": "Pandeglang", "district": "Pandeglang District", "lat": -6.3080, "lng": 106.1070},
    {"id": 159, "country": "Indonesia", "province": "West Java", "city": "Cibinong", "district": "Cibinong District", "lat": -6.4810, "lng": 106.8540},
    {"id": 160, "country": "Indonesia", "province": "West Java", "city": "Soreang", "district": "Soreang District", "lat": -7.0240, "lng": 107.5190},
    {"id": 161, "country": "Indonesia", "province": "West Java", "city": "Sumedang", "district": "Sumedang Utara District", "lat": -6.8580, "lng": 107.9160},
    {"id": 162, "country": "Indonesia", "province": "West Java", "city": "Majalengka", "district": "Majalengka District", "lat": -6.8370, "lng": 108.2270},
    {"id": 163, "country": "Indonesia", "province": "West Java", "city": "Indramayu", "district": "Indramayu District", "lat": -6.3270, "lng": 108.3200},
    {"id": 164, "country": "Indonesia", "province": "West Java", "city": "Kuningan", "district": "Kuningan District", "lat": -6.9760, "lng": 108.4830},
    {"id": 165, "country": "Indonesia", "province": "Central Java", "city": "Temanggung", "district": "Temanggung District", "lat": -7.3160, "lng": 110.1720},
    {"id": 166, "country": "Indonesia", "province": "Central Java", "city": "Purworejo", "district": "Purworejo District", "lat": -7.7140, "lng": 110.0080},
    {"id": 167, "country": "Indonesia", "province": "Central Java", "city": "Kebumen", "district": "Kebumen District", "lat": -7.6730, "lng": 109.6530},
    {"id": 168, "country": "Indonesia", "province": "Central Java", "city": "Blora", "district": "Blora District", "lat": -6.9690, "lng": 111.4180},
    {"id": 169, "country": "Indonesia", "province": "East Java", "city": "Bojonegoro", "district": "Bojonegoro District", "lat": -7.1500, "lng": 111.8820},
    {"id": 170, "country": "Indonesia", "province": "East Java", "city": "Tuban", "district": "Tuban District", "lat": -6.8970, "lng": 112.0640},
    {"id": 171, "country": "Indonesia", "province": "East Java", "city": "Situbondo", "district": "Situbondo District", "lat": -7.7060, "lng": 114.0090},
    {"id": 172, "country": "Indonesia", "province": "East Java", "city": "Nganjuk", "district": "Nganjuk District", "lat": -7.6050, "lng": 111.9040},
    {"id": 173, "country": "Indonesia", "province": "East Java", "city": "Ponorogo", "district": "Ponorogo District", "lat": -7.8680, "lng": 111.4620},
    {"id": 174, "country": "Indonesia", "province": "East Java", "city": "Pacitan", "district": "Pacitan District", "lat": -8.1970, "lng": 111.1010},
    {"id": 175, "country": "Indonesia", "province": "East Java", "city": "Trenggalek", "district": "Trenggalek District", "lat": -8.0500, "lng": 111.7170},
    {"id": 176, "country": "Indonesia", "province": "East Java", "city": "Bangil", "district": "Bangil District", "lat": -7.5990, "lng": 112.7830},
    {"id": 177, "country": "Indonesia", "province": "Bali", "city": "Negara", "district": "Jembrana District", "lat": -8.3570, "lng": 114.6170},
    {"id": 178, "country": "Indonesia", "province": "Bali", "city": "Amlapura", "district": "Karangasem District", "lat": -8.4500, "lng": 115.6090},
    {"id": 179, "country": "Indonesia", "province": "West Nusa Tenggara", "city": "Gerung", "district": "Gerung District", "lat": -8.7000, "lng": 116.1170},
    {"id": 180, "country": "Indonesia", "province": "West Nusa Tenggara", "city": "Taliwang", "district": "Taliwang District", "lat": -8.7440, "lng": 116.8530},
    {"id": 181, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Kefamenanu", "district": "Kota Kefamenanu District", "lat": -9.4470, "lng": 124.4780},
    {"id": 182, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Soe", "district": "Kota Soe District", "lat": -9.8600, "lng": 124.2840},
    {"id": 183, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Larantuka", "district": "Larantuka District", "lat": -8.3460, "lng": 122.9870},
    {"id": 184, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Bajawa", "district": "Bajawa District", "lat": -8.7870, "lng": 120.9760},
    {"id": 185, "country": "Indonesia", "province": "Central Kalimantan", "city": "Buntok", "district": "Dusun Selatan District", "lat": -1.7330, "lng": 114.8330},
    {"id": 186, "country": "Indonesia", "province": "Central Kalimantan", "city": "Muara Teweh", "district": "Teweh Tengah District", "lat": -0.9500, "lng": 114.9000},
    {"id": 187, "country": "Indonesia", "province": "East Kalimantan", "city": "Tanjung Redeb", "district": "Tanjung Redeb District", "lat": 2.1540, "lng": 117.4900},
    {"id": 188, "country": "Indonesia", "province": "East Kalimantan", "city": "Sendawar", "district": "Barong Tongkok District", "lat": -0.1800, "lng": 115.7000},
    {"id": 189, "country": "Indonesia", "province": "Central Sulawesi", "city": "Parigi", "district": "Parigi District", "lat": -0.8270, "lng": 120.1680},
    {"id": 190, "country": "Indonesia", "province": "South Sulawesi", "city": "Sengkang", "district": "Tempe District", "lat": -4.1330, "lng": 120.0300},
    {"id": 191, "country": "Indonesia", "province": "South Sulawesi", "city": "Rantepao", "district": "Rantepao District", "lat": -2.9700, "lng": 119.8970},

    {"id": 192, "country": "Indonesia", "province": "Aceh", "city": "Sigli", "district": "Pidie District", "lat": 5.3840, "lng": 95.9600},
    {"id": 193, "country": "Indonesia", "province": "Aceh", "city": "Bireuen", "district": "Kota Juang District", "lat": 5.2030, "lng": 96.7010},
    {"id": 194, "country": "Indonesia", "province": "North Sumatra", "city": "Balige", "district": "Balige District", "lat": 2.3330, "lng": 99.0660},
    {"id": 195, "country": "Indonesia", "province": "North Sumatra", "city": "Tarutung", "district": "Tarutung District", "lat": 2.0170, "lng": 98.9660},
    {"id": 196, "country": "Indonesia", "province": "West Sumatra", "city": "Lubuk Basung", "district": "Lubuk Basung District", "lat": -0.3200, "lng": 100.0000},
    {"id": 197, "country": "Indonesia", "province": "West Sumatra", "city": "Painan", "district": "IV Jurai District", "lat": -1.3500, "lng": 100.5730},
    {"id": 198, "country": "Indonesia", "province": "South Sumatra", "city": "Lahat", "district": "Lahat District", "lat": -3.7860, "lng": 103.5420},
    {"id": 199, "country": "Indonesia", "province": "South Sumatra", "city": "Muara Enim", "district": "Muara Enim District", "lat": -3.6500, "lng": 103.7700},
    {"id": 200, "country": "Indonesia", "province": "Lampung", "city": "Pringsewu", "district": "Pringsewu District", "lat": -5.3580, "lng": 104.9740},
    {"id": 201, "country": "Indonesia", "province": "Lampung", "city": "Kota Agung", "district": "Kota Agung District", "lat": -5.4900, "lng": 104.6200},
    {"id": 202, "country": "Indonesia", "province": "Bengkulu", "city": "Kepahiang", "district": "Kepahiang District", "lat": -3.6500, "lng": 102.5800},
    {"id": 203, "country": "Indonesia", "province": "Bangka Belitung Islands", "city": "Muntok", "district": "Muntok District", "lat": -2.0670, "lng": 105.1670},
    {"id": 204, "country": "Indonesia", "province": "Riau Islands", "city": "Tanjung Uban", "district": "Bintan Utara District", "lat": 1.0830, "lng": 104.2330},
    {"id": 205, "country": "Indonesia", "province": "Riau Islands", "city": "Daik Lingga", "district": "Lingga District", "lat": -0.2000, "lng": 104.6170},
    {"id": 206, "country": "Indonesia", "province": "West Java", "city": "Banjar City", "district": "Banjar District", "lat": -7.3700, "lng": 108.5340},
    {"id": 207, "country": "Indonesia", "province": "West Java", "city": "Subang", "district": "Subang District", "lat": -6.5710, "lng": 107.7580},
    {"id": 208, "country": "Indonesia", "province": "West Java", "city": "Ciamis", "district": "Ciamis District", "lat": -7.3250, "lng": 108.3530},
    {"id": 209, "country": "Indonesia", "province": "Special Region of Yogyakarta", "city": "Wonosari", "district": "Wonosari District", "lat": -7.9670, "lng": 110.6030},
    {"id": 210, "country": "Indonesia", "province": "Central Java", "city": "Jepara", "district": "Jepara District", "lat": -6.5940, "lng": 110.6680},
    {"id": 211, "country": "Indonesia", "province": "Central Java", "city": "Demak", "district": "Demak District", "lat": -6.8940, "lng": 110.6380},
    {"id": 212, "country": "Indonesia", "province": "Central Java", "city": "Wonogiri", "district": "Wonogiri District", "lat": -7.8170, "lng": 110.9260},
    {"id": 213, "country": "Indonesia", "province": "East Java", "city": "Mojokerto City", "district": "Magersari District", "lat": -7.4720, "lng": 112.4330},
    {"id": 214, "country": "Indonesia", "province": "East Java", "city": "Lamongan", "district": "Lamongan District", "lat": -7.1170, "lng": 112.4170},
    {"id": 215, "country": "Indonesia", "province": "East Java", "city": "Sampang", "district": "Sampang District", "lat": -7.1870, "lng": 113.2390},
    {"id": 216, "country": "Indonesia", "province": "Bali", "city": "Semarapura", "district": "Klungkung District", "lat": -8.5330, "lng": 115.4000},
    {"id": 217, "country": "Indonesia", "province": "West Nusa Tenggara", "city": "Selong", "district": "Selong District", "lat": -8.6500, "lng": 116.5330},
    {"id": 218, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Atambua", "district": "Kota Atambua District", "lat": -9.1060, "lng": 124.8920},
    {"id": 219, "country": "Indonesia", "province": "East Nusa Tenggara", "city": "Kalabahi", "district": "Teluk Mutiara District", "lat": -8.2160, "lng": 124.5170},
    {"id": 220, "country": "Indonesia", "province": "West Kalimantan", "city": "Nanga Pinoh", "district": "Nanga Pinoh District", "lat": -0.3500, "lng": 111.7500},
    {"id": 221, "country": "Indonesia", "province": "South Kalimantan", "city": "Martapura", "district": "Martapura District", "lat": -3.4160, "lng": 114.8500},
    {"id": 222, "country": "Indonesia", "province": "South Kalimantan", "city": "Kandangan", "district": "Kandangan District", "lat": -2.7830, "lng": 115.2670},
    {"id": 223, "country": "Indonesia", "province": "East Kalimantan", "city": "Sangatta", "district": "Sangatta Utara District", "lat": 0.5180, "lng": 117.5360},
    {"id": 224, "country": "Indonesia", "province": "North Kalimantan", "city": "Nunukan", "district": "Nunukan District", "lat": 4.1330, "lng": 117.6670},
    {"id": 225, "country": "Indonesia", "province": "North Sulawesi", "city": "Kotamobagu City", "district": "Kotamobagu Barat District", "lat": 0.7330, "lng": 124.3170},
    {"id": 226, "country": "Indonesia", "province": "Gorontalo", "city": "Limboto", "district": "Limboto District", "lat": 0.6350, "lng": 122.9780},
    {"id": 227, "country": "Indonesia", "province": "Central Sulawesi", "city": "Poso", "district": "Poso Kota District", "lat": -1.3950, "lng": 120.7520},
    {"id": 228, "country": "Indonesia", "province": "Southeast Sulawesi", "city": "Kolaka", "district": "Kolaka District", "lat": -4.0500, "lng": 121.6000},
    {"id": 229, "country": "Indonesia", "province": "West Sulawesi", "city": "Polewali", "district": "Polewali District", "lat": -3.4000, "lng": 119.3500},
    {"id": 230, "country": "Indonesia", "province": "Maluku", "city": "Namlea", "district": "Namlea District", "lat": -3.2670, "lng": 127.1000},
    {"id": 231, "country": "Indonesia", "province": "North Maluku", "city": "Sofifi", "district": "Oba Utara District", "lat": 0.7370, "lng": 127.5580},
    {"id": 232, "country": "Indonesia", "province": "Papua", "city": "Biak", "district": "Biak Kota District", "lat": -1.1830, "lng": 136.0830},
    {"id": 233, "country": "Indonesia", "province": "Papua", "city": "Serui", "district": "Yapen Selatan District", "lat": -1.8830, "lng": 136.2330},
    {"id": 234, "country": "Indonesia", "province": "Central Papua", "city": "Timika", "district": "Mimika Baru District", "lat": -4.5500, "lng": 136.8830},
    {"id": 235, "country": "Indonesia", "province": "West Papua", "city": "Fakfak", "district": "Fakfak District", "lat": -2.9170, "lng": 132.3000},
    {"id": 236, "country": "Indonesia", "province": "West Papua", "city": "Kaimana", "district": "Kaimana District", "lat": -3.6500, "lng": 133.7500},
    {"id": 237, "country": "Indonesia", "province": "West Papua", "city": "Bintuni", "district": "Bintuni District", "lat": -2.1170, "lng": 133.5330},
    {"id": 238, "country": "Indonesia", "province": "South Papua", "city": "Tanah Merah", "district": "Mandobo District", "lat": -6.1000, "lng": 140.3000},
    {"id": 239, "country": "Indonesia", "province": "Highland Papua", "city": "Oksibil", "district": "Oksibil District", "lat": -4.9000, "lng": 140.6330},
    {"id": 240, "country": "Indonesia", "province": "Highland Papua", "city": "Dekai", "district": "Dekai District", "lat": -4.8500, "lng": 139.5000},
    {"id": 241, "country": "Indonesia", "province": "Central Papua", "city": "Enarotali", "district": "Paniai Timur District", "lat": -3.9170, "lng": 136.3670}
]


AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
CACHE_SECONDS = 900
_cache = {"created_at": 0, "payload": None}


def fetch_json(url, params):
    request_url = f"{url}?{urlencode(params)}"
    request = Request(request_url, headers={"User-Agent": "ARI-Spread-Risk-Map/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_locations(payload, expected_count):
    if isinstance(payload, list):
        return payload
    if expected_count == 1 and isinstance(payload, dict):
        return [payload]
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        return payload["results"]
    raise ValueError("Unexpected Open-Meteo response structure")


def get_value(data, key):
    if not isinstance(data, dict):
        return None
    value = data.get(key)
    return value if isinstance(value, (int, float)) else None


def build_payload():
    latitudes = ",".join(str(region["lat"]) for region in REGIONS)
    longitudes = ",".join(str(region["lng"]) for region in REGIONS)

    air_params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "current": "us_aqi,pm2_5,pm10,nitrogen_dioxide,sulphur_dioxide,ozone",
        "timezone": "auto",
        "domains": "cams_global"
    }

    weather_params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation",
        "timezone": "auto"
    }

    air_results = normalize_locations(fetch_json(AIR_URL, air_params), len(REGIONS))

    try:
        weather_results = normalize_locations(fetch_json(WEATHER_URL, weather_params), len(REGIONS))
    except Exception:
        weather_results = [{} for _ in REGIONS]

    output = []

    for index, region in enumerate(REGIONS):
        air_result = air_results[index] if index < len(air_results) else {}
        weather_result = weather_results[index] if index < len(weather_results) else {}
        air_current = air_result.get("current", {}) if isinstance(air_result, dict) else {}
        weather_current = weather_result.get("current", {}) if isinstance(weather_result, dict) else {}
        air_units = air_result.get("current_units", {}) if isinstance(air_result, dict) else {}
        weather_units = weather_result.get("current_units", {}) if isinstance(weather_result, dict) else {}

        item = dict(region)
        item["air_quality"] = {
            "us_aqi": get_value(air_current, "us_aqi"),
            "pm2_5": get_value(air_current, "pm2_5"),
            "pm10": get_value(air_current, "pm10"),
            "nitrogen_dioxide": get_value(air_current, "nitrogen_dioxide"),
            "sulphur_dioxide": get_value(air_current, "sulphur_dioxide"),
            "ozone": get_value(air_current, "ozone"),
            "time": air_current.get("time") if isinstance(air_current, dict) else None,
            "units": {
                "pm2_5": air_units.get("pm2_5", "μg/m³"),
                "pm10": air_units.get("pm10", "μg/m³"),
                "nitrogen_dioxide": air_units.get("nitrogen_dioxide", "μg/m³"),
                "sulphur_dioxide": air_units.get("sulphur_dioxide", "μg/m³"),
                "ozone": air_units.get("ozone", "μg/m³")
            }
        }
        item["weather"] = {
            "temperature_2m": get_value(weather_current, "temperature_2m"),
            "relative_humidity_2m": get_value(weather_current, "relative_humidity_2m"),
            "wind_speed_10m": get_value(weather_current, "wind_speed_10m"),
            "wind_direction_10m": get_value(weather_current, "wind_direction_10m"),
            "precipitation": get_value(weather_current, "precipitation"),
            "time": weather_current.get("time") if isinstance(weather_current, dict) else None,
            "units": {
                "temperature_2m": weather_units.get("temperature_2m", "°C"),
                "relative_humidity_2m": weather_units.get("relative_humidity_2m", "%"),
                "wind_speed_10m": weather_units.get("wind_speed_10m", "km/h"),
                "wind_direction_10m": weather_units.get("wind_direction_10m", "°"),
                "precipitation": weather_units.get("precipitation", "mm")
            }
        }
        item["grid_location"] = {
            "latitude": air_result.get("latitude") if isinstance(air_result, dict) else None,
            "longitude": air_result.get("longitude") if isinstance(air_result, dict) else None,
            "elevation": air_result.get("elevation") if isinstance(air_result, dict) else None
        }
        output.append(item)

    return {
        "status": "success",
        "source": "Open-Meteo Air Quality API (CAMS Global) and Open-Meteo Weather API",
        "model_note": "Air-quality values are model estimates for the nearest model grid cell, not measurements from a local monitoring station.",
        "resolution_note": "CAMS Global air-quality model grid is approximately 0.4° (about 44–45 km); this is a model-grid resolution, not the precision of each map marker.",
        "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cache_seconds": CACHE_SECONDS,
        "data": output
    }


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "ERI environmental data API"})


@app.get("/api/regions")
def get_regions():
    now = time.time()
    if _cache["payload"] is not None and now - _cache["created_at"] < CACHE_SECONDS:
        return jsonify(_cache["payload"])

    try:
        payload = build_payload()
        _cache["created_at"] = now
        _cache["payload"] = payload
        return jsonify(payload)
    except (HTTPError, URLError, TimeoutError, ValueError, IndexError) as error:
        return jsonify({
            "status": "error",
            "message": "Environmental data provider could not be reached or returned an invalid response.",
            "detail": str(error)
        }), 502
    except Exception as error:
        app.logger.exception("Unexpected error while retrieving environmental data")
        return jsonify({
            "status": "error",
            "message": "Unexpected server error.",
            "detail": str(error)
        }), 500


if __name__ == "__main__":
    print("ERI API running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
