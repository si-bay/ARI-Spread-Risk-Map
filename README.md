# ARI-Spread-Risk-Map
A web that can generate risk map of ARI (acute respiration infection).

🦠 Peta Risiko Persebaran ISPA (ARI Spread Risk Map)

Platform pemantauan spasial dan simulasi prediktif risiko Infeksi Saluran Pernapasan Akut (ISPA) berbasis lingkungan untuk mendukung mitigasi kesehatan masyarakat.

🚀 Fitur Utama

Beranda & Dokumentasi Sistem (index.html): Informasi latar belakang, definisi klinis ISPA, dan tujuan platform.

Peta Spasial & Generator Simulasi (generator.html): Peta interaktif berbasis Leaflet.js dengan filter wilayah dan kalkulator prediktif berbasis parameter AQI serta kepadatan penduduk.

Profil Tim Pengembang (about.html): Pengenalan kolaborator lengkap dengan tautan media sosial dan pengatur bingkai foto interaktif.

Ekspor Data Spasial: Kemampuan mengunduh ringkasan dataset hasil simulasi ke dalam format .csv.

🛠️ Teknologi yang Digunakan

Frontend: HTML5, CSS3, Bootstrap 5, Bootstrap Icons

Mapping Engine: Leaflet.js & CartoDB Basemaps

Logika & Pemodelan: JavaScript (ES6+), scikit-learn (konsep pembobotan data tabular)

📂 Struktur Direktori Proyek

C:\Users\Denzf\Documents\ARI-spread-risk-map\
│
├── css\
│   └── bootstrap.min.css (dan berkas pendukung Bootstrap)
│
└── pages\
    ├── index.html
    ├── index.css
    ├── generator.html
    ├── generator.css
    ├── generator.js
    ├── about.html
    └── about.css


⚙️ Cara Menjalankan Proyek

Clone atau unduh repositori ini ke komputer Anda.

Pastikan struktur folder css dan pages sudah sesuai dengan direktori lokal Anda.

Buka peramban (browser) dan jalankan berkas pages/index.html secara langsung, atau gunakan ekstensi Live Server di VS Code.