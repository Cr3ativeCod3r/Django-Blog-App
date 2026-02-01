
const galleryImages = [
    {% for image in post.gallery_images.all %}
{
    url: "{{ image.image.url }}",
        caption: "{{ image.caption|default:post.title|escapejs }}"
} {% if not forloop.last %}, {% endif %}
{% endfor %}
];

let currentImageIndex = 0;

function openLightbox(index) {
    currentImageIndex = index;
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('hidden');
    lightbox.classList.add('flex');
    updateLightboxImage();
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.add('hidden');
    lightbox.classList.remove('flex');
    document.body.style.overflow = 'auto';
}

function changeImage(direction) {
    currentImageIndex += direction;
    if (currentImageIndex < 0) {
        currentImageIndex = galleryImages.length - 1;
    } else if (currentImageIndex >= galleryImages.length) {
        currentImageIndex = 0;
    }
    updateLightboxImage();
}

function updateLightboxImage() {
    const img = document.getElementById('lightbox-image');
    const caption = document.getElementById('lightbox-caption');
    img.src = galleryImages[currentImageIndex].url;
    caption.textContent = galleryImages[currentImageIndex].caption;
}

// Keyboard navigation
document.addEventListener('keydown', function (event) {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox.classList.contains('hidden')) {
        if (event.key === 'Escape') {
            closeLightbox();
        } else if (event.key === 'ArrowLeft') {
            changeImage(-1);
        } else if (event.key === 'ArrowRight') {
            changeImage(1);
        }
    }
});
