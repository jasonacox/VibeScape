//
//  SplashView.swift
//  VibeScapeTV
//
//  by Jason A. Cox
//  https://github.com/jasonacox/VibeScape
//  1 January 2026
//

import SwiftUI
import Foundation

/// Full-screen splash/settings screen.
///
/// This is presented as a modal (`fullScreenCover`) to ensure it owns the tvOS focus environment.
/// - Use the ON/OFF button to toggle prompt visibility.
/// - Menu/Back dismisses the splash.
struct SplashView: View {
    @Binding var isPresented: Bool
    @Binding var promptMode: PromptDisplayMode
    @Binding var imageURL: String
    @FocusState private var focusedButton: FocusableButton?

    @State private var draftImageURL: String = ""
    @State private var showValidationAlert = false
    @State private var validationMessage = ""
    @State private var showResultAlert = false
    @State private var resultTitle = ""
    @State private var resultMessage = ""
    @State private var closeOnResultOK = false
    @State private var isSaving = false
    
    /// Focus targets for the tvOS focus engine.
    enum FocusableButton {
        case promptMode
        case urlField
        case saveURL
        case resetURL
        case close
    }
    
    /// Get app version from bundle
    private var appVersion: String {
        let version = Bundle.main.object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String ?? "1.0"
        let build = Bundle.main.object(forInfoDictionaryKey: "CFBundleVersion") as? String ?? "1"
        return "Version \(version) (Build \(build))"
    }
    
    var body: some View {
        ZStack {
            // Full-screen gradient background matching the logo's sunset-to-night sky
            LinearGradient(
                colors: [
                    Color(red: 0.08, green: 0.10, blue: 0.28),  // Deep night blue (top)
                    Color(red: 0.20, green: 0.15, blue: 0.45),  // Purple transition
                    Color(red: 0.55, green: 0.30, blue: 0.50),  // Mauve/pink
                    Color(red: 0.85, green: 0.45, blue: 0.40),  // Warm coral
                    Color(red: 1.00, green: 0.65, blue: 0.30)   // Sunset orange (bottom)
                ],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()
            
            VStack(spacing: 20) {
                // VibeScape logo image
                Image("VibeScapeLogo")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(maxWidth: 600, maxHeight: 280)
                    .shadow(color: .black.opacity(0.5), radius: 20, x: 0, y: 10)
                
                // Subtitle
                Text("AI Powered Seasonal Dreams")
                    .font(.system(size: 26, weight: .light))
                    .foregroundColor(.white.opacity(0.95))
                    .shadow(color: .black.opacity(0.3), radius: 4, x: 0, y: 2)
                
                // GitHub link
                Text("github.com/jasonacox/VibeScape")
                    .font(.system(size: 20))
                    .foregroundColor(.white.opacity(0.8))
                    .padding(.top, 4)
                
                // Version
                Text(appVersion)
                    .font(.system(size: 16))
                    .foregroundColor(.white.opacity(0.5))
                    .padding(.top, 8)
                
                // Divider - subtle white line
                Rectangle()
                    .fill(Color.white.opacity(0.25))
                    .frame(height: 1)
                    .frame(maxWidth: 450)
                    .padding(.vertical, 16)
                
                // Settings section
                VStack(spacing: 20) {
                    // Prompt display mode selector (cycling button)
                    VStack(spacing: 12) {
                        Text("Prompt Display Mode")
                            .font(.system(size: 22))
                            .foregroundColor(.white.opacity(0.9))
                        
                        Button(action: {
                            // Cycle to next mode
                            let allModes = PromptDisplayMode.allCases
                            if let currentIndex = allModes.firstIndex(of: promptMode) {
                                let nextIndex = (currentIndex + 1) % allModes.count
                                promptMode = allModes[nextIndex]
                                ImageService.savePromptMode(promptMode)
                            }
                        }) {
                            HStack(spacing: 12) {
                                Text(promptMode.displayName)
                                    .font(.system(size: 20, weight: .semibold))
                                    .foregroundColor(.white)
                                Image(systemName: "arrow.triangle.2.circlepath")
                                    .font(.system(size: 18))
                                    .foregroundColor(.white.opacity(0.8))
                            }
                            .frame(width: 340, height: 54)
                            .background(Color(red: 0.2, green: 0.6, blue: 0.4))
                            .cornerRadius(10)
                        }
                        .buttonStyle(.card)
                        .focused($focusedButton, equals: .promptMode)
                    }

                    // Image URL
                    VStack(spacing: 10) {
                        Text("Image Server URL")
                            .font(.system(size: 22))
                            .foregroundColor(.white.opacity(0.9))

                        TextField("https://…/image", text: $draftImageURL)
                            .textFieldStyle(.plain)
                            .font(.system(size: 18))
                            .textInputAutocapitalization(.never)
                            .autocorrectionDisabled()
                            .padding(.horizontal, 14)
                            .padding(.vertical, 10)
                            .background(Color.black.opacity(0.3))
                            .cornerRadius(8)
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(Color.white.opacity(0.2), lineWidth: 1)
                            )
                            .frame(width: 700)
                            .focused($focusedButton, equals: .urlField)

                        HStack(spacing: 16) {
                            Button(action: {
                                beginSaveURL(draftImageURL)
                            }) {
                                Text(isSaving ? "Saving…" : "Save")
                                    .font(.system(size: 20, weight: .semibold))
                                    .foregroundColor(.white)
                                    .frame(width: 160, height: 50)
                                    .background(Color.white.opacity(0.15))
                                    .cornerRadius(8)
                            }
                            .buttonStyle(.card)
                            .focused($focusedButton, equals: .saveURL)
                            .disabled(isSaving)

                            Button(action: {
                                draftImageURL = ImageService.defaultImageURL
                                beginSaveURL(draftImageURL)
                            }) {
                                Text("Reset")
                                    .font(.system(size: 20, weight: .semibold))
                                    .foregroundColor(.white)
                                    .frame(width: 160, height: 50)
                                    .background(Color.white.opacity(0.15))
                                    .cornerRadius(8)
                            }
                            .buttonStyle(.card)
                            .focused($focusedButton, equals: .resetURL)
                            .disabled(isSaving)
                        }
                    }
                    
                    // Close button
                    Button(action: {
                        isPresented = false
                    }) {
                        Text("Close")
                            .font(.system(size: 22, weight: .medium))
                            .foregroundColor(.white)
                            .frame(width: 220, height: 54)
                            .background(Color.white.opacity(0.15))
                            .cornerRadius(8)
                    }
                    .buttonStyle(.card)
                    .focused($focusedButton, equals: .close)
                    .padding(.top, 8)
                }
                .padding(30)
                .background(Color.black.opacity(0.35))
                .cornerRadius(16)
                .focusSection()
                
                // Close instruction
                Text("Press Menu to close")
                    .font(.system(size: 16))
                    .foregroundColor(.white.opacity(0.4))
                    .padding(.top, 6)
            }
            .padding(.horizontal, 80)
            .padding(.vertical, 50)
        }
        .onAppear {
            draftImageURL = imageURL
            focusedButton = .promptMode
        }
        .onExitCommand {
            isPresented = false
        }
        .alert("Invalid URL", isPresented: $showValidationAlert) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(validationMessage)
        }
        .alert(resultTitle, isPresented: $showResultAlert) {
            Button("OK") {
                if closeOnResultOK {
                    isPresented = false
                }
            }
        } message: {
            Text(resultMessage)
        }
    }

    private func beginSaveURL(_ rawValue: String) {
        Task {
            await saveURLWithConnectivityTest(rawValue)
        }
    }

    private func saveURLWithConnectivityTest(_ rawValue: String) async {
        guard !isSaving else { return }
        await MainActor.run { isSaving = true }
        defer { DispatchQueue.main.async { [self] in isSaving = false } }

        let trimmed = rawValue.trimmingCharacters(in: .whitespacesAndNewlines)

        guard !trimmed.isEmpty else {
            await MainActor.run {
                validationMessage = "Please enter a URL. Example: https://vibescape.jasonacox.com/image"
                showValidationAlert = true
            }
            return
        }

        guard let url = URL(string: trimmed) else {
            await MainActor.run {
                validationMessage = "That doesn't look like a valid URL. Example: https://vibescape.jasonacox.com/image"
                showValidationAlert = true
            }
            return
        }

        // If the user omitted the scheme, URL(string:) will still parse but scheme will be nil.
        guard let scheme = url.scheme?.lowercased(), (scheme == "https" || scheme == "http") else {
            await MainActor.run {
                validationMessage = "Please include the full URL with http:// or https:// (for example: https://vibescape.jasonacox.com/image)."
                showValidationAlert = true
            }
            return
        }

        do {
            try await testImageEndpoint(url)
        } catch {
            await MainActor.run {
                closeOnResultOK = false
                resultTitle = "Unable to Connect"
                let details = (error as? LocalizedError)?.errorDescription ?? error.localizedDescription
                resultMessage = "Server is not responding or the URL is bad.\n\nPlease verify the address and try again.\n\nDetails: \(details)\nURL: \(trimmed)"
                showResultAlert = true
            }
            return
        }

        await MainActor.run {
            imageURL = trimmed
            closeOnResultOK = true
            resultTitle = "Server URL Saved"
            resultMessage = "The image server URL was saved successfully."
            showResultAlert = true
        }
    }

    private enum EndpointTestError: LocalizedError {
        case nonHTTPResponse
        case httpStatus(Int)
        case emptyResponse
        case missingImageData

        var errorDescription: String? {
            switch self {
            case .nonHTTPResponse:
                return "Non-HTTP response"
            case .httpStatus(let code):
                return "HTTP status \(code)"
            case .emptyResponse:
                return "Empty response body"
            case .missingImageData:
                return "Response did not contain expected JSON field 'image_data'"
            }
        }
    }

    private func testImageEndpoint(_ url: URL) async throws {
        var request = URLRequest(url: url)
        request.cachePolicy = .reloadIgnoringLocalAndRemoteCacheData
        request.timeoutInterval = 6

        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse else {
            throw EndpointTestError.nonHTTPResponse
        }
        guard (200...299).contains(http.statusCode) else {
            throw EndpointTestError.httpStatus(http.statusCode)
        }
        guard !data.isEmpty else { throw EndpointTestError.emptyResponse }

        // Light validation: ensure this looks like the expected JSON payload.
        if let obj = try? JSONSerialization.jsonObject(with: data),
           let dict = obj as? [String: Any],
           dict["image_data"] != nil {
            return
        }

        // If it's not the expected JSON shape, treat as invalid.
        throw EndpointTestError.missingImageData
    }
}

#Preview {
    SplashView(isPresented: .constant(true), promptMode: .constant(.autoFade), imageURL: .constant(ImageService.defaultImageURL))
}
