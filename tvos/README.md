# VibeScapeTV - Apple TV App

A tvOS app that displays images from the VibeScape server with automatic refresh every 10 seconds.

## Features

- Fetches and displays images from a configurable VibeScape server
- Automatically refreshes every 10 seconds
- Displays the AI-generated prompt (can be toggled on/off)
- Smooth transitions between images (only when image changes)
- Configurable image server URL with validation and connectivity testing
- Built-in splash/settings screen with:
  - Prompt visibility toggle (ON/OFF)
  - VibeScape Image Server URL editor with Save/Reset
  - Real-time server connectivity verification
- Error handling with user-friendly messages

## Requirements

- Xcode 15.0 or later
- tvOS 16.0 or later
- Apple TV (4th generation or later)

## Setup

1. Open `VibeScapeTV.xcodeproj` in Xcode
2. Select your Apple TV device or simulator as the target
3. Build and run the project (⌘R)

## How to Use

- The app will automatically start fetching and displaying images from the default server
- Press **Play/Pause** or tap the image to open the splash/settings screen

### Splash Screen Options

- **Show Prompt Text**: Toggle ON/OFF to show/hide the AI prompt at the bottom of images
- **Image Server URL**: 
  - Edit the server endpoint URL
  - Press **Save** to test connectivity and apply changes
  - Press **Reset** to restore the default URL (`https://vibescape.jasonacox.com/image`)
  - The app validates the URL format and tests connectivity before saving
- **Close**: Return to the image viewer
- Press **Menu/Back** on the remote to close the splash screen

## Project Structure

- `VibeScapeTVApp.swift` - Main app entry point
- `ContentView.swift` - Main UI view with image display and prompt overlay
- `SplashView.swift` - Full-screen splash/settings view (prompt toggle)
- `ImageService.swift` - Service that handles fetching images from the API
- `Assets.xcassets` - App icons and assets

## API Format

The app expects JSON responses in the following format:

```jsonImage Server URL (In-App)

1. Press **Play/Pause** to open the splash/settings screen
2. Navigate to the **Image Server URL** text field
3. Edit the URL (must include `http://` or `https://`)
4. Press **Save** to validate and test connectivity
5. If successful, the new URL is saved and immediately applied
6. Press **Reset** to restore the default URL

### Change the Refresh Interval (Code)

To change the refresh interval, modify the `refreshInterval` constant in `ImageService.swift`:

```swift
private let refreshInterval: TimeInterval = 10.0 // seconds
```

### Change the Default Server URL (Code)

To change the default server URL, update `defaultImageURL` in `ImageService.swift`:

```swift
static let defaultI refresh interval, modify the `refreshInterval` constant in `ImageService.swift`:

```swift
private let refreshInterval: TimeInterval = 10.0 // seconds
```

To use a different server URL, update the `imageURL` in `ImageService.swift`:

```swift
private let imageURL = "https://vibescape.jasonacox.com/image"
```

## License

Same as the parent VibeScape project.
