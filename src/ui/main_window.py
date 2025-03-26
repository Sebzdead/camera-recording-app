from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
import json
import cv2
from camera_controller import CameraController
from video_recorder import VideoRecorder

# Add lib directory to PATH at runtime
lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'lib')
if lib_path not in os.environ['PATH']:
    os.environ['PATH'] = lib_path + os.pathsep + os.environ['PATH']

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Recording App")
        
        # Initialize camera first to get dimensions
        self.camera_controller = CameraController()
        
        # Get camera feed dimensions
        frame = self.camera_controller.get_frame()
        if frame is not None:
            self.feed_width = int(self.camera_controller.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.feed_height = int(self.camera_controller.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            # Default dimensions if camera feed not available
            self.feed_width = 4000
            self.feed_height = 3000
            
        # Calculate window size to fit screen
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        scale_factor = min(screen.width() * 0.8 / self.feed_width, 
                         screen.height() * 0.6 / self.feed_height)
        
        self.display_width = int(self.feed_width * scale_factor)
        self.display_height = int(self.feed_height * scale_factor)
        
        # Set window size with space for controls
        window_width = self.display_width
        window_height = self.display_height + 200  # Extra space for controls
        self.setGeometry(
            (screen.width() - window_width) // 2,  # Center horizontally
            (screen.height() - window_height) // 2,  # Center vertically
            window_width,
            window_height
        )
        
        # Load default settings
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'default_settings.json')
        with open(config_path, 'r') as f:
            self.settings = json.load(f)
            
        # Use forward slashes for paths to avoid issues
        self.save_directory = self.settings.get('default_save_directory', '')
        self.camera_controller = CameraController()
        self.video_recorder = VideoRecorder(
            output_directory=self.save_directory,
            framerate=self.settings.get('default_framerate', 25),
            codec=self.settings.get('default_compression', 'H264'),
            feed_width=self.feed_width,
            feed_height=self.feed_height
        )

        self.init_ui()

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout()

        self.video_feed_label = QtWidgets.QLabel()
        self.layout.addWidget(self.video_feed_label)

        self.start_button = QtWidgets.QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)
        self.layout.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        self.layout.addWidget(self.stop_button)

        self.framerate_label = QtWidgets.QLabel("Framerate:")
        self.layout.addWidget(self.framerate_label)

        self.framerate_input = QtWidgets.QSpinBox()
        self.framerate_input.setRange(1, 60)
        self.framerate_input.setValue(30)
        self.layout.addWidget(self.framerate_input)

        self.compression_label = QtWidgets.QLabel("Compression:")
        self.layout.addWidget(self.compression_label)

        self.compression_input = QtWidgets.QComboBox()
        self.compression_input.addItems(["H264", "XVID", "MJPG", "DIVX"])
        # Set default from settings
        default_compression = self.settings.get('default_compression', 'H264')
        index = self.compression_input.findText(default_compression)
        if index >= 0:
            self.compression_input.setCurrentIndex(index)
        self.layout.addWidget(self.compression_input)
        
        # Add filename input before directory selection
        self.filename_layout = QtWidgets.QHBoxLayout()
        self.filename_label = QtWidgets.QLabel("Filename:")
        self.filename_input = QtWidgets.QLineEdit()
        # Set default filename with timestamp
        timestamp = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        self.filename_input.setText(f"recording_{timestamp}.mp4")
        
        self.filename_layout.addWidget(self.filename_label)
        self.filename_layout.addWidget(self.filename_input)
        self.layout.addLayout(self.filename_layout)
        
        # Directory selection comes after filename input
        self.dir_layout = QtWidgets.QHBoxLayout()
        self.dir_label = QtWidgets.QLabel("Save Directory:")
        self.dir_input = QtWidgets.QLineEdit(self.save_directory)
        self.dir_browse = QtWidgets.QPushButton("Browse")
        self.dir_browse.clicked.connect(self.browse_directory)
        
        self.dir_layout.addWidget(self.dir_label)
        self.dir_layout.addWidget(self.dir_input)
        self.dir_layout.addWidget(self.dir_browse)
        self.layout.addLayout(self.dir_layout)
        
        # Add recording duration option
        self.duration_layout = QtWidgets.QHBoxLayout()
        self.duration_check = QtWidgets.QCheckBox("Auto-stop after:")
        self.duration_input = QtWidgets.QSpinBox()
        self.duration_input.setRange(1, 3600)
        self.duration_input.setValue(60)
        self.duration_input.setSuffix(" seconds")
        self.duration_input.setEnabled(False)
        self.duration_check.toggled.connect(self.duration_input.setEnabled)
        
        self.duration_layout.addWidget(self.duration_check)
        self.duration_layout.addWidget(self.duration_input)
        self.layout.addLayout(self.duration_layout)

        self.setLayout(self.layout)

        # Setting up the UI controls
        self.stop_button.setEnabled(False)
        
        # Set framerate from settings
        default_framerate = self.settings.get('default_framerate', 25)
        self.framerate_input.setValue(default_framerate)
        
        # Start camera feed timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_video_feed)
        self.timer.start(30)  # Update roughly 30 times per second

    def update_video_feed(self):
        frame = self.camera_controller.get_frame()
        if frame is not None:
            # Convert BGR to RGB format for PyQt display
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize frame to fit display area
            resized_frame = cv2.resize(rgb_frame, (self.display_width, self.display_height))
            
            qt_image = QtGui.QImage(
                resized_frame.data,
                resized_frame.shape[1],
                resized_frame.shape[0],
                resized_frame.strides[0],
                QtGui.QImage.Format_RGB888
            )
            self.video_feed_label.setPixmap(QtGui.QPixmap.fromImage(qt_image))
            self.video_feed_label.setFixedSize(self.display_width, self.display_height)
            
            # If recording, pass original frame to video recorder
            if self.video_recorder.is_recording_active():
                # Use original frame for recording, error handling is inside record_frame method
                success = self.video_recorder.record_frame(frame)
                if not success:
                    # This will only print to console - could add UI indicator if needed
                    print("Failed to record frame")

    def browse_directory(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.save_directory)
        if dir_path:
            self.save_directory = dir_path
            self.dir_input.setText(dir_path)
            self.video_recorder.output_directory = dir_path
    
    def start_recording(self):
        # Get filename from input field
        filename = self.filename_input.text()
        if not filename:
            # If empty, generate default filename
            timestamp = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
            filename = f"recording_{timestamp}.mp4"
            self.filename_input.setText(filename)
        
        # Ensure filename ends with .mp4
        if not filename.lower().endswith('.mp4'):
            filename += '.mp4'
            self.filename_input.setText(filename)
        
        framerate = self.framerate_input.value()
        self.camera_controller.set_framerate(framerate)
        
        # Update video recorder settings
        codec = self.compression_input.currentText()
        self.video_recorder.framerate = framerate
        self.video_recorder.codec = codec
        self.video_recorder.feed_width = self.feed_width
        self.video_recorder.feed_height = self.feed_height
        
        # Start recording with user-specified filename
        success = self.video_recorder.start_recording(filename)
        if success:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            # Show error message to user
            QtWidgets.QMessageBox.critical(self, "Recording Error", 
                                         "Failed to start recording. Please check codec and file path.")
        
        # Handle auto-stop if enabled
        if self.duration_check.isChecked():
            duration = self.duration_input.value()
            QtCore.QTimer.singleShot(duration * 1000, self.stop_recording)

    def stop_recording(self):
        self.video_recorder.stop_recording()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())