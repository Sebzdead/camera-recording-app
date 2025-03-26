from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
import json
import EasyPySpin
import cv2
from camera_controller import CameraController
from video_recorder import VideoRecorder

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Recording App")
        self.setGeometry(100, 100, 800, 600)
        
        # Load default settings
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'default_settings.json')
        with open(config_path, 'r') as f:
            self.settings = json.load(f)
            
        self.save_directory = self.settings.get('default_save_directory', '/Users/sebastian/Videos')
        self.camera_controller = CameraController()
        self.video_recorder = VideoRecorder(self.save_directory)

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
        self.compression_input.addItems(["XVID", "MJPG", "X264", "DIVX"])
        # Set default from settings
        default_compression = self.settings.get('default_compression', 'XVID')
        index = self.compression_input.findText(default_compression)
        if index >= 0:
            self.compression_input.setCurrentIndex(index)
        self.layout.addWidget(self.compression_input)
        
        # Add directory selection
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
        default_framerate = self.settings.get('default_framerate', 30)
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
            qt_image = QtGui.QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], 
                                  rgb_frame.strides[0], QtGui.QImage.Format_RGB888)
            self.video_feed_label.setPixmap(QtGui.QPixmap.fromImage(qt_image))
            
            # If recording, pass frame to video recorder
            if self.video_recorder.is_recording_active():
                self.video_recorder.record_frame(frame)

    def browse_directory(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.save_directory)
        if dir_path:
            self.save_directory = dir_path
            self.dir_input.setText(dir_path)
            self.video_recorder.output_directory = dir_path
    
    def start_recording(self):
        framerate = self.framerate_input.value()
        self.camera_controller.set_framerate(framerate)
        
        # Update video recorder settings
        codec = self.compression_input.currentText()
        self.video_recorder.framerate = framerate
        self.video_recorder.codec = codec
        
        # Generate filename with timestamp
        timestamp = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        filename = f"recording_{timestamp}.avi"
        
        # Start recording
        self.video_recorder.start_recording(filename)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # Handle auto-stop if enabled
        if self.duration_check.isChecked():
            duration = self.duration_input.value()
            # Use QTimer for auto-stop
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