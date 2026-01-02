# VibeScapeTV - Apple TV App

A tvOS app that displays images from the VibeScape server with automatic refresh every 10 seconds.

## Features

- Fetches and displays images from `https://vibescape.jasonacox.com/image`
- Automatically refreshes every 10 seconds
- Displays the AI-generated prompt (can be hidden via the splash screen)
- Smooth transitions between images
- Avoids transitions when the image is unchanged
- Error handling with user-friendly messages
- Built-in splash/settings screen (VibeScape branding)

## Requirements

- Xcode 15.0 or later
- tvOS 16.0 or later
- Apple TV (4th generation or later)

## Setup

1. Open `VibeScapeTV.xcodeproj` in Xcode
2. Select your Apple TV device or simulator as the target
3. Build and run the project (⌘R)

## How to Use

- The app will automatically start fetching and displaying images
- Press **Play/Pause** to open/close the splash screen
- On the splash screen, use the **ON/OFF** button to toggle prompt visibility
- Images refresh every 10 seconds, but only fade when a new image arrives

## Project Structure

- `VibeScapeTVApp.swift` - Main app entry point
- `ContentView.swift` - Main UI view with image display and prompt overlay
- `SplashView.swift` - Full-screen splash/settings view (prompt toggle)
- `ImageService.swift` - Service that handles fetching images from the API
- `Assets.xcassets` - App icons and assets

## API Format

The app expects JSON responses in the following format:

```json
{
  "prompt": "Description of the generated image",
  "image_data": "data:image/jpeg;base64,..."
}
```

## Customization

To change the refresh interval, modify the `refreshInterval` constant in `ImageService.swift`:

```swift
private let refreshInterval: TimeInterval = 10.0 // seconds
```

To use a different server URL, update the `imageURL` in `ImageService.swift`:

```swift
private let imageURL = "https://vibescape.jasonacox.com/image"
```

## License

Same as the parent VibeScape project.
