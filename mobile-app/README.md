# Flutter Mobile App Setup Guide

## Prerequisites

Flutter SDK is required to run this mobile app. 

### Install Flutter on Windows

1. Download Flutter SDK from: https://flutter.dev/docs/get-started/install/windows
2. Extract to a folder (e.g., `C:\flutter`)
3. Add to PATH: `C:\flutter\bin`
4. Run: `flutter doctor` to verify installation

## Setup Instructions

After installing Flutter:

```bash
cd "f:\RevoU\APP STORE\mobile-app"

# Get dependencies
flutter pub get

# Run on connected device/emulator
flutter run

# Build APK for release
flutter build apk
```

## Configuration

Edit `lib/services/job_service.dart` to change the API URL:

```dart
// For Android Emulator (localhost)
static const String baseUrl = 'http://10.0.2.2:8000';

// For Physical Device (use your computer's IP)
static const String baseUrl = 'http://192.168.x.x:8000';

// For Production
static const String baseUrl = 'https://your-api.com';
```

## Project Structure

```
mobile-app/
├── lib/
│   ├── main.dart          # App entry point
│   ├── models/
│   │   └── job.dart       # Job data model
│   ├── screens/
│   │   └── home_page.dart # Main UI screen
│   ├── services/
│   │   └── job_service.dart # API client
│   └── widgets/
│       └── job_card.dart   # Job card component
├── pubspec.yaml           # Dependencies
└── analysis_options.yaml  # Lint rules
```

## Features

- Material 3 design with dark mode support
- Job listings with search and filter
- Infinite scroll pagination
- Job detail bottom sheet
- Apply button with URL launcher
