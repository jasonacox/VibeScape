"""Image generation service for VibeScape."""
import os
import time
import json
import uuid
from pathlib import Path
from typing import Optional, Dict
import requests
from config import Config


class ImageGenerator:
    """Handle AI image generation and caching."""
    
    def __init__(self):
        """Initialize the image generator."""
        self.api_key = Config.OPENAI_API_KEY
        self.cache_dir = Path(Config.CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict:
        """Load image metadata from cache."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {"images": []}
    
    def _save_metadata(self):
        """Save image metadata to cache."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def generate_image(self, prompt: str, theme: str) -> Optional[Dict]:
        """Generate an image using OpenAI DALL-E API.
        
        Args:
            prompt: The text prompt for image generation
            theme: The theme/season for this image
            
        Returns:
            Dictionary with image info or None if generation fails
        """
        if not self.api_key:
            print("Warning: No OpenAI API key configured. Using placeholder mode.")
            return self._create_placeholder_image(prompt, theme)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": Config.IMAGE_MODEL,
                "prompt": prompt,
                "n": 1,
                "size": Config.IMAGE_SIZE,
                "quality": Config.IMAGE_QUALITY
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                
                # Download the image
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    timestamp = int(time.time())
                    unique_id = uuid.uuid4().hex[:8]
                    filename = f"image_{timestamp}_{unique_id}.png"
                    filepath = self.cache_dir / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    # Store metadata
                    image_info = {
                        "filename": filename,
                        "prompt": prompt,
                        "theme": theme,
                        "timestamp": timestamp,
                        "path": f"generated/{filename}"
                    }
                    
                    self.metadata["images"].append(image_info)
                    self._cleanup_old_images()
                    self._save_metadata()
                    
                    return image_info
                else:
                    print(f"Failed to download image: {img_response.status_code}")
            else:
                print(f"Image generation failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"Error generating image: {e}")
        
        return None
    
    def _create_placeholder_image(self, prompt: str, theme: str) -> Dict:
        """Create a placeholder entry when API is not configured.
        
        Args:
            prompt: The text prompt
            theme: The theme/season
            
        Returns:
            Dictionary with placeholder image info
        """
        timestamp = int(time.time())
        unique_id = uuid.uuid4().hex[:8]
        filename = f"placeholder_{timestamp}_{unique_id}.txt"
        filepath = self.cache_dir / filename
        
        # Create a text file as placeholder
        with open(filepath, 'w') as f:
            f.write(f"Theme: {theme}\n\nPrompt: {prompt}\n\n")
            f.write("This is a placeholder. Configure OPENAI_API_KEY to generate real images.")
        
        image_info = {
            "filename": filename,
            "prompt": prompt,
            "theme": theme,
            "timestamp": timestamp,
            "path": f"generated/{filename}",
            "placeholder": True
        }
        
        self.metadata["images"].append(image_info)
        self._cleanup_old_images()
        self._save_metadata()
        
        return image_info
    
    def _cleanup_old_images(self):
        """Remove old images if cache exceeds maximum."""
        if len(self.metadata["images"]) > Config.MAX_CACHED_IMAGES:
            # Sort by timestamp and remove oldest
            sorted_images = sorted(
                self.metadata["images"],
                key=lambda x: x["timestamp"]
            )
            
            to_remove = sorted_images[:-Config.MAX_CACHED_IMAGES]
            
            for img in to_remove:
                filepath = self.cache_dir / img["filename"]
                if filepath.exists():
                    filepath.unlink()
            
            # Keep only recent images in metadata
            self.metadata["images"] = sorted_images[-Config.MAX_CACHED_IMAGES:]
    
    def get_recent_images(self, limit: int = 10):
        """Get most recent images from cache.
        
        Args:
            limit: Maximum number of images to return
            
        Returns:
            List of image info dictionaries
        """
        sorted_images = sorted(
            self.metadata["images"],
            key=lambda x: x["timestamp"],
            reverse=True
        )
        return sorted_images[:limit]
    
    def get_all_images(self):
        """Get all cached images."""
        return sorted(
            self.metadata["images"],
            key=lambda x: x["timestamp"],
            reverse=True
        )
