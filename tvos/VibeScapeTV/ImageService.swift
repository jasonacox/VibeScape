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

/// JSON payload returned by the VibeScape `/image/status` endpoint.
struct StatusResponse: Codable {
    let available: Bool
    let timestamp: Double?
    let age_seconds: Double?
}

/// JSON payload returned by the VibeScape `/image` endpoint.
struct ImageResponse: Codable {
    let prompt: String?
    let image_data: String?
    let timestamp: Double?
    
    enum CodingKeys: String, CodingKey {
        case prompt
        case image_data
        case timestamp
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
    
    private var pollTimer: DispatchSourceTimer?
    private let pollQueue = DispatchQueue(label: "com.jasonacox.vibescape.poll", qos: .userInitiated)
    private var lastImageTimestamp: Double?
    private var isFetching = false

    static let defaultImageURL = "https://vibescape.jasonacox.com/image"
    static let imageURLUserDefaultsKey = "vibescape.imageURL"

    private(set) var imageURL: String
    private let refreshInterval: TimeInterval = 10.0
    
    /// Computed property to get status URL from image URL
    private var statusURL: String {
        // Replace /image with /image/status
        if imageURL.hasSuffix("/image") {
            return imageURL + "/status"
        } else {
            // Fallback: append /status
            return imageURL.replacingOccurrences(of: "/image", with: "/image/status")
        }
    }
    
    /// Dedicated URL session with caching disabled to ensure fresh requests hit the server.
    private lazy var urlSession: URLSession = {
        let config = URLSessionConfiguration.default
        config.requestCachePolicy = .reloadIgnoringLocalAndRemoteCacheData
        config.urlCache = nil
        return URLSession(configuration: config)
    }()

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
        stopFetching()

        // Fetch immediately (first time, always fetch full image)
        fetchImage()

        // Poll reliably on a dispatch queue (avoids run-loop mode pauses).
        let timer = DispatchSource.makeTimerSource(flags: .strict, queue: pollQueue)
        timer.schedule(deadline: .now() + refreshInterval, repeating: refreshInterval, leeway: .milliseconds(100))
        timer.setEventHandler { [weak self] in
            self?.checkStatus()
        }
        pollTimer = timer
        timer.resume()
    }
    
    /// Stops polling.
    func stopFetching() {
        pollTimer?.setEventHandler {}
        pollTimer?.cancel()
        pollTimer = nil
        isFetching = false
    }
    
    /// Checks the lightweight status endpoint to see if a new image is available.
    /// Only fetches the full image if the timestamp has changed.
    private func checkStatus() {
        guard let url = URL(string: statusURL) else {
            // Fallback to full fetch if status URL is invalid
            fetchImage()
            return
        }
        
        urlSession.dataTask(with: url) { [weak self] data, response, error in
            guard let self = self else { return }
            
            if error != nil {
                // On error, try full fetch as fallback
                self.fetchImage()
                return
            }
            
            guard let data = data else {
                self.fetchImage()
                return
            }
            
            do {
                let status = try JSONDecoder().decode(StatusResponse.self, from: data)
                
                // If no image available yet, skip
                guard status.available, let timestamp = status.timestamp else {
                    return
                }
                
                // If timestamp hasn't changed, skip download
                if let lastTimestamp = self.lastImageTimestamp, timestamp == lastTimestamp {
                    return
                }
                
                // New image available - fetch it
                self.fetchImage()
                
            } catch {
                // On parse error, try full fetch as fallback
                self.fetchImage()
            }
        }.resume()
    }
    
    private func fetchImage() {
        if isFetching { return }
        isFetching = true

        guard let url = URL(string: imageURL) else {
            DispatchQueue.main.async {
                self.errorMessage = "Invalid URL"
            }
            isFetching = false
            return
        }
        
        urlSession.dataTask(with: url) { [weak self] data, response, error in
            guard let self = self else { return }
            defer { self.isFetching = false }
            
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
                
                // Check if we have valid image data
                guard let imageDataString = imageResponse.image_data else {
                    // No image data (still generating)
                    return
                }
                
                // Parse base64 image data
                if let imageData = self.parseBase64Image(imageDataString),
                   let uiImage = UIImage(data: imageData) {
                    DispatchQueue.main.async {
                        self.currentImage = uiImage
                        self.currentPrompt = imageResponse.prompt
                        self.errorMessage = nil
                        // Update timestamp to track this image
                        self.lastImageTimestamp = imageResponse.timestamp
                    }
                } else {
                    DispatchQueue.main.async {
                        self.errorMessage = "Failed to decode image data"
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
