//
//  ContentView.swift
//  VibeScapeTV
//
//  by Jason A. Cox
//  https://github.com/jasonacox/VibeScape
//  1 January 2026

import SwiftUI

/// Main tvOS screen: displays the latest VibeScape image and (optionally) the prompt.
///
/// Remote controls:
/// - Tap/Select on the image opens the splash/settings screen.
/// - Play/Pause toggles the splash/settings screen.
struct ContentView: View {
    @StateObject private var imageService = ImageService()
    @State private var showSplash = false
    @State private var promptMode: PromptDisplayMode = ImageService.loadPromptMode()
    @State private var isPromptCurrentlyVisible = true
    @State private var promptFadeTimer: Timer?
    @State private var imageURL = ImageService.loadImageURL()
    @State private var showConnectionError = false
    
    /// Check if this is a connection error (server offline or wrong URL)
    private var isConnectionError: Bool {
        guard let error = imageService.errorMessage else { return false }
        return error.contains("Could not connect") || 
               error.contains("Network error") ||
               error.contains("Invalid URL")
    }
    
    /// Determines if prompt should be shown based on current mode
    private var shouldShowPrompt: Bool {
        switch promptMode {
        case .alwaysHidden:
            return false
        case .alwaysVisible:
            return true
        case .autoFade:
            return isPromptCurrentlyVisible
        }
    }
    
    /// Start 5-second fade timer for auto-fade mode
    private func startPromptFadeTimer() {
        promptFadeTimer?.invalidate()
        
        guard promptMode == .autoFade else { return }
        
        isPromptCurrentlyVisible = true
        promptFadeTimer = Timer.scheduledTimer(withTimeInterval: 5.0, repeats: false) { _ in
            withAnimation(.easeOut(duration: 1.0)) {
                isPromptCurrentlyVisible = false
            }
        }
    }
    
    /// Show prompt again when user interacts with remote
    private func onUserInteraction() {
        if promptMode == .autoFade && !isPromptCurrentlyVisible {
            withAnimation(.easeIn(duration: 0.3)) {
                isPromptCurrentlyVisible = true
            }
            startPromptFadeTimer()
        }
    }
    
    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            
            if let image = imageService.currentImage {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .clipped()
                    .ignoresSafeArea()
                    .transition(.opacity)
                    .animation(.easeInOut(duration: 0.5), value: imageService.currentImage)
                    .focusable()
                    .onTapGesture {
                        showSplash = true
                    }
            } else {
                VStack(spacing: 20) {
                    ProgressView()
                        .scaleEffect(2)
                    Text("Loading VibeScape...")
                        .font(.title2)
                        .foregroundColor(.white)
                }
            }
            
            // Show prompt at bottom based on display mode
            if let prompt = imageService.currentPrompt {
                GeometryReader { geometry in
                    VStack {
                        Spacer()
                        HStack {
                            Spacer()
                            Text(prompt)
                                .font(.system(size: 20))
                                .foregroundColor(.white.opacity(0.6))
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 20)
                                .padding(.vertical, 8)
                                .background(Color.black.opacity(0.3))
                                .cornerRadius(6)
                                .frame(maxWidth: geometry.size.width * 0.5)
                            Spacer()
                        }
                        .padding(.bottom, 10)
                    }
                }
                .ignoresSafeArea()
                .opacity(shouldShowPrompt ? 1.0 : 0.0)
                .animation(.easeInOut(duration: 1.0), value: isPromptCurrentlyVisible)
            }
            
            // Error message if loading fails (only show if no cached image and not a connection error)
            if let error = imageService.errorMessage, 
               imageService.currentImage == nil,
               !isConnectionError {
                VStack(spacing: 20) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .font(.system(size: 60))
                        .foregroundColor(.yellow)
                    Text("Loading Image...")
                        .font(.title)
                        .foregroundColor(.white)
                    Text(error)
                        .font(.body)
                        .foregroundColor(.white)
                        .multilineTextAlignment(.center)
                        .padding()
                }
                .padding()
            }
        }
        .onAppear {
            UIApplication.shared.isIdleTimerDisabled = true
            // Sync stored URL before starting (in case it differs from default)
            if imageURL != imageService.imageURL {
                _ = imageService.setImageURL(imageURL)
            }
            imageService.startFetching()
            startPromptFadeTimer()
        }
        .onDisappear {
            UIApplication.shared.isIdleTimerDisabled = false
            promptFadeTimer?.invalidate()
            imageService.stopFetching()
        }
        .animation(.easeInOut(duration: 0.3), value: showSplash)
        .onPlayPauseCommand {
            onUserInteraction()
            showSplash.toggle()
        }
        .onMoveCommand { _ in
            onUserInteraction()
        }
        .onChange(of: imageURL) { [imageService] newValue in
            _ = imageService.setImageURL(newValue)
        }
        .onChange(of: imageService.currentImage) { _ in
            startPromptFadeTimer()
        }
        .onChange(of: imageService.errorMessage) { error in
            // Show connection error alert when no image is cached
            if isConnectionError && imageService.currentImage == nil {
                showConnectionError = true
            }
        }
        .alert("Unable to Connect", isPresented: $showConnectionError) {
            Button("Settings") {
                showSplash = true
            }
        } message: {
            Text("Could not connect to the VibeScape server.\n\nPlease check that the server is running and the URL is correct.")
        }
        .fullScreenCover(isPresented: $showSplash) {
            SplashView(isPresented: $showSplash, promptMode: $promptMode, imageURL: $imageURL)
        }
    }
}

#Preview {
    ContentView()
}
