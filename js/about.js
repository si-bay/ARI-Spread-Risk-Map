const shapeSelect = document.getElementById('frame-shape-select');
const avatars = document.querySelectorAll('.team-avatar');

shapeSelect.addEventListener('change', function() {
    const selectedShape = this.value;

    avatars.forEach(avatar => {
        avatar.classList.remove('circle', 'rounded', 'octagon');
        avatar.classList.add(selectedShape);
    });
});