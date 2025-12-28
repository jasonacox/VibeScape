"""Main Flask application for VibeScape."""
import os
import time
import threading
from flask import Flask, render_template, jsonify, send_from_directory
from config import Config
from seasonal_prompts import SeasonalPrompts
from image_generator import ImageGenerator

app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
prompt_generator = SeasonalPrompts()
image_generator = ImageGenerator()

# Background generation state
generation_state = {
    "last_generation": 0,
    "current_theme": None,
    "generating": False
}


def background_image_generation():
    """Background thread for continuous image generation."""
    while True:
        try:
            current_time = time.time()
            time_since_last = current_time - generation_state["last_generation"]
            
            if time_since_last >= Config.GENERATION_INTERVAL and not generation_state["generating"]:
                generation_state["generating"] = True
                
                # Generate new image
                theme, prompt = prompt_generator.generate_prompt()
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Generating image...")
                print(f"Theme: {theme}")
                print(f"Prompt: {prompt}")
                
                result = image_generator.generate_image(prompt, theme)
                
                if result:
                    print(f"✓ Generated: {result['filename']}")
                else:
                    print("✗ Generation failed")
                
                generation_state["last_generation"] = current_time
                generation_state["current_theme"] = theme
                generation_state["generating"] = False
                
        except Exception as e:
            print(f"Error in background generation: {e}")
            generation_state["generating"] = False
        
        # Sleep for a bit before checking again
        time.sleep(10)


@app.route('/')
def index():
    """Render the main page."""
    theme = prompt_generator.get_current_theme()
    theme_name = prompt_generator.get_theme_display_name(theme)
    return render_template('index.html', theme=theme_name)


@app.route('/api/images')
def get_images():
    """API endpoint to get available images."""
    images = image_generator.get_all_images()
    return jsonify({
        "images": images,
        "count": len(images)
    })


@app.route('/api/current-theme')
def get_current_theme():
    """API endpoint to get current theme."""
    theme = prompt_generator.get_current_theme()
    theme_name = prompt_generator.get_theme_display_name(theme)
    return jsonify({
        "theme": theme,
        "theme_name": theme_name
    })


@app.route('/api/generate', methods=['POST'])
def trigger_generation():
    """API endpoint to manually trigger image generation."""
    if generation_state["generating"]:
        return jsonify({"status": "already_generating"}), 429
    
    try:
        generation_state["generating"] = True
        theme, prompt = prompt_generator.generate_prompt()
        result = image_generator.generate_image(prompt, theme)
        generation_state["generating"] = False
        
        if result:
            return jsonify({
                "status": "success",
                "image": result
            })
        else:
            return jsonify({
                "status": "failed",
                "message": "Image generation failed"
            }), 500
            
    except Exception as e:
        generation_state["generating"] = False
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/static/generated/<path:filename>')
def serve_generated_image(filename):
    """Serve generated images."""
    return send_from_directory('static/generated', filename)


if __name__ == '__main__':
    # Ensure static directory exists
    os.makedirs('static/generated', exist_ok=True)
    
    # Start background generation thread
    generation_thread = threading.Thread(target=background_image_generation, daemon=True)
    generation_thread.start()
    
    # Generate first image immediately
    print("Generating initial image...")
    theme, prompt = prompt_generator.generate_prompt()
    result = image_generator.generate_image(prompt, theme)
    if result:
        print(f"✓ Initial image generated: {result['filename']}")
        generation_state["last_generation"] = time.time()
    
    print(f"\nVibeScape is running!")
    print(f"Slideshow interval: {Config.SLIDESHOW_INTERVAL} seconds")
    print(f"Generation interval: {Config.GENERATION_INTERVAL} seconds")
    print(f"Current theme: {prompt_generator.get_theme_display_name(prompt_generator.get_current_theme())}")
    print(f"\nOpen http://localhost:5000 in your browser\n")
    
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
