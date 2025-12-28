// VibeScape Frontend Application
class VibeScape {
    constructor() {
        this.images = [];
        this.currentIndex = 0;
        this.isPlaying = true;
        this.slideshowInterval = 60000; // 60 seconds default
        this.slideshowTimer = null;
        this.imageCheckInterval = null;
        this.themeCheckInterval = null;
        
        this.elements = {
            imageContainer: document.getElementById('imageContainer'),
            currentImage: document.getElementById('currentImage'),
            loading: document.getElementById('loading'),
            placeholder: document.getElementById('placeholder'),
            themeBadge: document.getElementById('themeBadge'),
            prevBtn: document.getElementById('prevBtn'),
            nextBtn: document.getElementById('nextBtn'),
            playPauseBtn: document.getElementById('playPauseBtn'),
            generateBtn: document.getElementById('generateBtn'),
            currentTheme: document.getElementById('currentTheme')
        };
        
        this.init();
    }
    
    async init() {
        // Load images
        await this.loadImages();
        
        // Update theme
        await this.updateTheme();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Start slideshow if we have images
        if (this.images.length > 0) {
            this.showImage(0);
            this.startSlideshow();
        }
        
        // Check for new images periodically
        this.imageCheckInterval = setInterval(() => this.loadImages(), 30000); // Check every 30 seconds
        
        // Update theme periodically
        this.themeCheckInterval = setInterval(() => this.updateTheme(), 300000); // Check every 5 minutes
    }
    
    cleanup() {
        // Clean up intervals to prevent memory leaks
        if (this.slideshowTimer) {
            clearInterval(this.slideshowTimer);
        }
        if (this.imageCheckInterval) {
            clearInterval(this.imageCheckInterval);
        }
        if (this.themeCheckInterval) {
            clearInterval(this.themeCheckInterval);
        }
    }
    
    setupEventListeners() {
        this.elements.prevBtn.addEventListener('click', () => this.previousImage());
        this.elements.nextBtn.addEventListener('click', () => this.nextImage());
        this.elements.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        this.elements.generateBtn.addEventListener('click', () => this.generateNewImage());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.previousImage();
            if (e.key === 'ArrowRight') this.nextImage();
            if (e.key === ' ') {
                e.preventDefault();
                this.togglePlayPause();
            }
            if (e.key === 'g' || e.key === 'G') this.generateNewImage();
        });
    }
    
    async loadImages() {
        try {
            const response = await fetch('/api/images');
            const data = await response.json();
            
            if (data.images && data.images.length > 0) {
                const newImageCount = data.images.length - this.images.length;
                this.images = data.images.filter(img => !img.placeholder);
                
                // If we got new images and we're on placeholder, show first image
                if (newImageCount > 0 && this.elements.placeholder.style.display !== 'none') {
                    this.showImage(0);
                    this.startSlideshow();
                }
                
                this.updateControls();
            }
        } catch (error) {
            console.error('Error loading images:', error);
        }
    }
    
    async updateTheme() {
        try {
            const response = await fetch('/api/current-theme');
            const data = await response.json();
            
            if (data.theme_name) {
                this.elements.themeBadge.textContent = data.theme_name;
                if (this.elements.currentTheme) {
                    this.elements.currentTheme.textContent = data.theme_name;
                }
            }
        } catch (error) {
            console.error('Error updating theme:', error);
        }
    }
    
    showImage(index) {
        if (this.images.length === 0) return;
        
        this.currentIndex = (index + this.images.length) % this.images.length;
        const image = this.images[this.currentIndex];
        
        // Hide placeholder and loading
        this.elements.placeholder.style.display = 'none';
        this.elements.loading.style.display = 'none';
        
        // Show image with fade effect
        const img = this.elements.currentImage;
        img.style.opacity = '0';
        img.src = `/static/${image.path}`;
        
        img.onload = () => {
            img.style.display = 'block';
            setTimeout(() => {
                img.style.opacity = '1';
                img.style.transition = 'opacity 1s ease-in';
            }, 10);
        };
        
        this.updateControls();
    }
    
    previousImage() {
        if (this.images.length === 0) return;
        this.showImage(this.currentIndex - 1);
        this.resetSlideshow();
    }
    
    nextImage() {
        if (this.images.length === 0) return;
        this.showImage(this.currentIndex + 1);
        this.resetSlideshow();
    }
    
    togglePlayPause() {
        this.isPlaying = !this.isPlaying;
        this.elements.playPauseBtn.textContent = this.isPlaying ? '⏸' : '▶';
        this.elements.playPauseBtn.title = this.isPlaying ? 'Pause Slideshow' : 'Play Slideshow';
        
        if (this.isPlaying) {
            this.startSlideshow();
        } else {
            this.stopSlideshow();
        }
    }
    
    startSlideshow() {
        if (!this.isPlaying || this.images.length === 0) return;
        
        this.stopSlideshow();
        this.slideshowTimer = setInterval(() => {
            this.nextImage();
        }, this.slideshowInterval);
    }
    
    stopSlideshow() {
        if (this.slideshowTimer) {
            clearInterval(this.slideshowTimer);
            this.slideshowTimer = null;
        }
    }
    
    resetSlideshow() {
        if (this.isPlaying) {
            this.startSlideshow();
        }
    }
    
    async generateNewImage() {
        const btn = this.elements.generateBtn;
        if (btn.disabled) return;
        
        btn.disabled = true;
        btn.textContent = '⏳';
        
        try {
            const response = await fetch('/api/generate', { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'success') {
                // Reload images
                await this.loadImages();
                btn.textContent = '✓';
                setTimeout(() => {
                    btn.textContent = '✨';
                    btn.disabled = false;
                }, 2000);
            } else {
                btn.textContent = '✗';
                setTimeout(() => {
                    btn.textContent = '✨';
                    btn.disabled = false;
                }, 2000);
            }
        } catch (error) {
            console.error('Error generating image:', error);
            btn.textContent = '✗';
            setTimeout(() => {
                btn.textContent = '✨';
                btn.disabled = false;
            }, 2000);
        }
    }
    
    updateControls() {
        const hasImages = this.images.length > 0;
        this.elements.prevBtn.disabled = !hasImages;
        this.elements.nextBtn.disabled = !hasImages;
        this.elements.playPauseBtn.disabled = !hasImages;
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new VibeScape();
});
