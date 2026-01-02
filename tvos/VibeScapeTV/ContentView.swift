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
    @State private var showPrompt = true
    @State private var imageURL = ImageService.loadImageURL()
    
    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            
            if let image = imageService.currentImage {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
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
            
            // Always show prompt at bottom if available
            if showPrompt, let prompt = imageService.currentPrompt {
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
            }
            
            // Error message if loading fails
            if let error = imageService.errorMessage {
                VStack(spacing: 20) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .font(.system(size: 60))
                        .foregroundColor(.yellow)
                    Text("Error Loading Image")
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
        }
        .onDisappear {
            UIApplication.shared.isIdleTimerDisabled = false
            imageService.stopFetching()
        }
        .animation(.easeInOut(duration: 0.3), value: showSplash)
        .onPlayPauseCommand {
            showSplash.toggle()
        }
        .onChange(of: imageURL) { [imageService] newValue in
            _ = imageService.setImageURL(newValue)
        }
        .fullScreenCover(isPresented: $showSplash) {
            SplashView(isPresented: $showSplash, showPrompt: $showPrompt, imageURL: $imageURL)
        }
    }
}

#Preview {
    ContentView()
}
