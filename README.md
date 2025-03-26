# Camera Recording App

## Overview
The Camera Recording App is a Python application that allows users to capture live video feeds from a camera, adjust settings such as framerate and compression, and record videos to a specified directory. The application features a user-friendly interface for easy operation.

## Features
- Live camera feed display
- Adjustable framerate and compression settings
- Start and stop recording functionality
- Automatic stopping of recordings after a specified duration
- Save recorded videos in .avi format

## Project Structure
```
camera-recording-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── camera_controller.py    # Handles camera operations
│   ├── video_recorder.py       # Manages video recording functionality
│   └── ui
│       ├── main_window.py      # Main user interface
│       └── settings_panel.py    # Settings interface for framerate and compression
├── config
│   └── default_settings.json    # Default configuration settings
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd camera-recording-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Add the lib directory to your system PATH:
   Right-click on Start → System
   Click "Advanced system settings"
   Click "Environment Variables"
   Under "System variables", find and select "Path"
   Click "Edit"
   Click "New"
   Add c:yourdirectory\camera-recording-app\lib
   Click "OK" on all windows

## Usage
1. Run the application:
   ```
   python src/main.py
   ```
2. Use the user interface to select the desired framerate and compression settings.
3. Click the "Start Recording" button to begin capturing video.
4. Click the "Stop Recording" button to end the recording session.
5. Videos will be saved in the specified directory in .avi format.

## Configuration
Default settings can be modified in the `config/default_settings.json` file. This includes options for framerate, compression level, and the directory for saving videos.

## Dependencies
- EasyPySpin
- Other necessary libraries (listed in `requirements.txt`)

## License
This project is licensed under the MIT License. See the LICENSE file for more details.