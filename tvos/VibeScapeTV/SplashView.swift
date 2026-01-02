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
    @Binding var showPrompt: Bool
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
        case toggle
        case urlField
        case saveURL
        case resetURL
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

                    // Image URL
                    VStack(spacing: 12) {
                        Text("VibeScape Image Server URL")
                            .font(.system(size: 24))
                            .foregroundColor(.white)

                        TextField("https://…/image", text: $draftImageURL)
                            .textFieldStyle(.plain)
                            .font(.system(size: 20))
                            .textInputAutocapitalization(.never)
                            .autocorrectionDisabled()
                            .padding(.horizontal, 14)
                            .padding(.vertical, 12)
                            .background(Color.white.opacity(0.12))
                            .cornerRadius(10)
                            .overlay(
                                RoundedRectangle(cornerRadius: 10)
                                    .stroke(Color.white.opacity(0.25), lineWidth: 1)
                            )
                            .frame(width: 800)
                            .focused($focusedButton, equals: .urlField)

                        HStack(spacing: 20) {
                            Button(action: {
                                beginSaveURL(draftImageURL)
                            }) {
                                Text(isSaving ? "Saving…" : "Save")
                                    .font(.system(size: 22, weight: .semibold))
                                    .foregroundColor(.white)
                                    .frame(width: 180, height: 56)
                                    .background(Color.white.opacity(0.2))
                                    .cornerRadius(10)
                            }
                            .buttonStyle(.card)
                            .focused($focusedButton, equals: .saveURL)
                            .disabled(isSaving)

                            Button(action: {
                                draftImageURL = ImageService.defaultImageURL
                                beginSaveURL(draftImageURL)
                            }) {
                                Text("Reset")
                                    .font(.system(size: 22, weight: .semibold))
                                    .foregroundColor(.white)
                                    .frame(width: 180, height: 56)
                                    .background(Color.white.opacity(0.2))
                                    .cornerRadius(10)
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
            draftImageURL = imageURL
            focusedButton = .toggle
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
    SplashView(isPresented: .constant(true), showPrompt: .constant(true), imageURL: .constant(ImageService.defaultImageURL))
}
