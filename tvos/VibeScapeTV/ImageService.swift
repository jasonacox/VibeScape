//
//  ImageService.swift
//  VibeScapeTV
//
//  by Jason A. Cox
//  https://github.com/jasonacox/VibeScape
//  1 January 2026
//

import Foundation
import SwiftUI
import Combine

/// JSON payload returned by the VibeScape `/image` endpoint.
struct ImageResponse: Codable {
    let prompt: String
    let image_data: String
    
    enum CodingKeys: String, CodingKey {
        case prompt
        case image_data
    }
}

/// Periodically polls the VibeScape server for new images and publishes the latest image + prompt.
///
/// Notes:
/// - Polling occurs every `refreshInterval` seconds.
/// - UI updates are only published when `image_data` changes to avoid unnecessary transitions.
class ImageService: ObservableObject {
    @Published var currentImage: UIImage?
    @Published var currentPrompt: String?
    @Published var errorMessage: String?
    
    private var timer: Timer?
    private var lastImageData: String?

    static let defaultImageURL = "https://vibescape.jasonacox.com/image"
    static let imageURLUserDefaultsKey = "vibescape.imageURL"

    private(set) var imageURL: String
    private let refreshInterval: TimeInterval = 10.0

    init() {
        self.imageURL = Self.loadImageURL()
    }

    /// Loads the configured image URL (or the default if not set).
    static func loadImageURL() -> String {
        UserDefaults.standard.string(forKey: imageURLUserDefaultsKey) ?? defaultImageURL
    }

    /// Updates the image URL if valid and persists it.
    /// Returns `true` if the URL was accepted.
    @discardableResult
    func setImageURL(_ newValue: String) -> Bool {
        let trimmed = newValue.trimmingCharacters(in: .whitespacesAndNewlines)
        guard let url = URL(string: trimmed),
              let scheme = url.scheme?.lowercased(),
              (scheme == "https" || scheme == "http") else {
            DispatchQueue.main.async {
                self.errorMessage = "Invalid image URL"
            }
            return false
        }

        imageURL = trimmed
        UserDefaults.standard.set(trimmed, forKey: Self.imageURLUserDefaultsKey)
        fetchImage()
        return true
    }
    
    /// Starts polling immediately and then every `refreshInterval` seconds.
    func startFetching() {
        // Fetch immediately
        fetchImage()
        
        // Then fetch every 10 seconds
        timer = Timer.scheduledTimer(withTimeInterval: refreshInterval, repeats: true) { [weak self] _ in
            self?.fetchImage()
        }
    }
    
    /// Stops polling.
    func stopFetching() {
        timer?.invalidate()
        timer = nil
    }
    
    private func fetchImage() {
        guard let url = URL(string: imageURL) else {
            DispatchQueue.main.async {
                self.errorMessage = "Invalid URL"
            }
            return
        }
        
        URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            guard let self = self else { return }
            
            if let error = error {
                DispatchQueue.main.async {
                    self.errorMessage = "Network error: \(error.localizedDescription)"
                }
                return
            }
            
            guard let data = data else {
                DispatchQueue.main.async {
                    self.errorMessage = "No data received"
                }
                return
            }
            
            do {
                let imageResponse = try JSONDecoder().decode(ImageResponse.self, from: data)
                
                // Only update if the image data has changed
                if imageResponse.image_data != self.lastImageData {
                    // Parse base64 image data
                    if let imageData = self.parseBase64Image(imageResponse.image_data),
                       let uiImage = UIImage(data: imageData) {
                        DispatchQueue.main.async {
                            self.currentImage = uiImage
                            self.currentPrompt = imageResponse.prompt
                            self.errorMessage = nil
                            self.lastImageData = imageResponse.image_data
                        }
                    } else {
                        DispatchQueue.main.async {
                            self.errorMessage = "Failed to decode image data"
                        }
                    }
                } else {
                    // Same image, just update prompt if needed and clear errors
                    DispatchQueue.main.async {
                        self.currentPrompt = imageResponse.prompt
                        self.errorMessage = nil
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    self.errorMessage = "Failed to parse response: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
    
    /// Extracts base64 bytes from a data-URL string (supports JPEG/PNG prefixes).
    private func parseBase64Image(_ base64String: String) -> Data? {
        // Remove the "data:image/jpeg;base64," prefix if present
        let base64 = base64String.replacingOccurrences(of: "data:image/jpeg;base64,", with: "")
            .replacingOccurrences(of: "data:image/png;base64,", with: "")
        
        return Data(base64Encoded: base64, options: .ignoreUnknownCharacters)
    }
}
