//
//  SplashView.swift
//  VibeScapeTV
//
//  by Jason A. Cox
//  https://github.com/jasonacox/VibeScape
//  1 January 2026
//

import SwiftUI

/// Full-screen splash/settings screen.
///
/// This is presented as a modal (`fullScreenCover`) to ensure it owns the tvOS focus environment.
/// - Use the ON/OFF button to toggle prompt visibility.
/// - Menu/Back dismisses the splash.
struct SplashView: View {
    @Binding var isPresented: Bool
    @Binding var showPrompt: Bool
    @FocusState private var focusedButton: FocusableButton?
    
    /// Focus targets for the tvOS focus engine.
    enum FocusableButton {
        case toggle
        case close
    }
    
    var body: some View {
        ZStack {
            // Semi-transparent backdrop
            Color.black.opacity(0.95)
                .ignoresSafeArea()
            
            VStack(spacing: 30) {
                // VibeScape title with gradient
                Text("VibeScape")
                    .font(.system(size: 80, weight: .bold))
                    .foregroundStyle(
                        LinearGradient(
                            colors: [Color(red: 0.7, green: 0, blue: 0), Color(red: 1, green: 0.84, blue: 0)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .shadow(color: .black.opacity(0.4), radius: 6, x: 2, y: 2)
                
                // Subtitle
                Text("AI Powered Seasonal Dreams")
                    .font(.system(size: 28))
                    .foregroundColor(.white.opacity(0.9))
                
                // GitHub link
                Text("github.com/jasonacox/VibeScape")
                    .font(.system(size: 22))
                    .foregroundColor(Color(red: 1, green: 0.84, blue: 0))
                    .padding(.top, 10)
                
                // Version
                Text("Version: 1.0")
                    .font(.system(size: 18))
                    .foregroundColor(.white.opacity(0.6))
                    .padding(.top, 15)
                
                // Divider
                Rectangle()
                    .fill(Color.white.opacity(0.3))
                    .frame(height: 1)
                    .frame(maxWidth: 500)
                    .padding(.vertical, 20)
                
                // Settings section
                VStack(spacing: 25) {
                    // Toggle for showing/hiding prompt
                    VStack(spacing: 15) {
                        Text("Show Prompt Text")
                            .font(.system(size: 24))
                            .foregroundColor(.white)
                        
                        Button(action: {
                            showPrompt.toggle()
                        }) {
                            Text(showPrompt ? "ON" : "OFF")
                                .font(.system(size: 22, weight: .semibold))
                                .foregroundColor(.white)
                                .frame(width: 150, height: 60)
                                .background(showPrompt ? Color.green.opacity(0.8) : Color.gray.opacity(0.6))
                                .cornerRadius(10)
                        }
                        .buttonStyle(.card)
                        .focused($focusedButton, equals: .toggle)
                    }
                    
                    // Close button
                    Button(action: {
                        isPresented = false
                    }) {
                        Text("Close")
                            .font(.system(size: 24, weight: .medium))
                            .foregroundColor(.white)
                            .frame(width: 250, height: 60)
                            .background(Color.white.opacity(0.2))
                            .cornerRadius(10)
                    }
                    .buttonStyle(.card)
                    .focused($focusedButton, equals: .close)
                }
                .focusSection()
                
                // Close instruction
                Text("or press Menu/Back to close")
                    .font(.system(size: 18))
                    .foregroundColor(.white.opacity(0.5))
                    .padding(.top, 10)
            }
            .padding(60)
            .background(
                LinearGradient(
                    colors: [
                        Color(red: 0.7, green: 0.067, blue: 0.067).opacity(0.18),
                        Color(red: 1, green: 0.84, blue: 0).opacity(0.12)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .cornerRadius(20)
            .shadow(color: .black.opacity(0.5), radius: 60, x: 0, y: 20)
        }
        .onAppear {
            focusedButton = .toggle
        }
        .onExitCommand {
            isPresented = false
        }
    }
}

#Preview {
    SplashView(isPresented: .constant(true), showPrompt: .constant(true))
}
