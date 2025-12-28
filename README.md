# VibeScape

An always-on ambient generative art experience that sets the vibe.

VibeScape is a Python web service that continually displays AI-generated art in a slideshow format. It automatically watches the time of year and generates prompts that produce season-appropriate images.

## Features

✨ **Seasonal Awareness**: Automatically adjusts themes based on the current date
- **Holidays**: Christmas, New Year's Eve, New Year's, Valentine's Day, Halloween, Thanksgiving
- **Seasons**: Winter, Spring, Summer, Fall with appropriate imagery

🎨 **AI-Generated Art**: Uses OpenAI's DALL-E to create beautiful, ambient art
- Cozy winter scenes with fireplaces and snow
- Christmas decorations and festive atmospheres
- New Year's celebrations with fireworks
- Spring blooms and summer serenity
- Autumn colors and harvest themes

🖼️ **Ambient Display**: Clean, full-screen interface perfect for always-on displays
- Auto-rotating slideshow
- Smooth transitions and fade effects
- Keyboard controls and manual navigation
- Responsive design for any screen size

## Screenshots

[Screenshot of the application will appear here when running]

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jasonacox/VibeScape.git
cd VibeScape
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create configuration file:
```bash
cp .env.example .env
```

4. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### Running the Application

Start the VibeScape server:

```bash
python app.py
```

The application will:
1. Start the web server on `http://localhost:5000`
2. Generate an initial image based on the current season/holiday
3. Begin the background generation process
4. Display images in a continuous slideshow

Open your browser and navigate to `http://localhost:5000` to view the ambient art display.

### Keyboard Controls

- **←/→ Arrow Keys**: Navigate between images
- **Space Bar**: Pause/resume slideshow
- **G**: Generate a new image immediately

### Configuration Options

Edit `.env` to customize behavior:

```bash
# Slideshow timing
SLIDESHOW_INTERVAL=60        # Seconds between image transitions (default: 60)
GENERATION_INTERVAL=300      # Seconds between new image generation (default: 300)

# Image settings
IMAGE_MODEL=dall-e-3         # OpenAI model to use
IMAGE_SIZE=1024x1024         # Image dimensions
IMAGE_QUALITY=standard       # 'standard' or 'hd'

# Cache settings
MAX_CACHED_IMAGES=20         # Maximum images to store (default: 20)
```

## How It Works

### Seasonal Themes

VibeScape uses the current date to determine the appropriate theme:

- **December 20-23**: Christmas preparation themes
- **December 24-30**: Full Christmas themes
- **December 31**: New Year's Eve celebrations
- **January 1-2**: New Year themes
- **February 14**: Valentine's Day
- **October 25-31**: Halloween
- **November 20+**: Thanksgiving
- **December-February**: Winter scenes
- **March-May**: Spring scenes
- **June-August**: Summer scenes
- **September-November**: Fall scenes

### Prompt Generation

Each theme has carefully crafted prompt templates that create appropriate, ambient imagery:
- Winter: Cozy cabins, fireplaces, snowy mountains, warm interiors
- Christmas: Decorated trees, festive lights, presents, winter villages
- Spring: Blooming gardens, cherry blossoms, fresh meadows
- And more...

### Background Generation

The application runs a background thread that:
1. Generates new images at regular intervals (default: every 5 minutes)
2. Maintains a cache of recent images
3. Automatically removes old images when cache limit is reached
4. Continues generating indefinitely for an always-on experience

## API Endpoints

- `GET /`: Main application interface
- `GET /api/images`: Get list of all cached images
- `GET /api/current-theme`: Get current season/holiday theme
- `POST /api/generate`: Manually trigger image generation

## Development

### Project Structure

```
VibeScape/
├── app.py                  # Main Flask application
├── config.py               # Configuration management
├── seasonal_prompts.py     # Season/holiday detection and prompt generation
├── image_generator.py      # AI image generation and caching
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   ├── js/
│   │   └── app.js         # Frontend JavaScript
│   └── generated/         # Cache directory for generated images
└── .env                   # Configuration (not in git)
```

### Running Without API Key

If you run the application without an OpenAI API key, it will operate in placeholder mode and create text files instead of generating actual images. This is useful for testing the seasonal logic and UI without incurring API costs.

## Contributing

Contributions are welcome! Feel free to:
- Add new seasonal themes
- Improve prompt templates
- Enhance the UI/UX
- Add new features

## License

See LICENSE file for details.

## Credits

Created by Jason Cox
Uses OpenAI's DALL-E for image generation
