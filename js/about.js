// Interaktif Pengubah Bingkai Wajah (Face Frame Customizer)
const shapeSelect = document.getElementById('frame-shape-select');
const avatars = document.querySelectorAll('.team-avatar');

shapeSelect.addEventListener('change', function() {
    const selectedShape = this.value;

    avatars.forEach(avatar => {
        // Hapus kelas bentuk lama
        avatar.classList.remove('circle', 'rounded', 'octagon');
        
        // Tambahkan bentuk baru sesuai pilihan dropdown
        avatar.classList.add(selectedShape);
    });
});