from PyQt5 import QtWidgets, QtCore

class SettingsPanel(QtWidgets.QWidget):
    def __init__(self, camera_controller):
        super().__init__()
        self.camera_controller = camera_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Settings Panel")

        # Framerate selection
        self.framerate_label = QtWidgets.QLabel("Select Framerate:")
        self.framerate_combo = QtWidgets.QComboBox()
        self.framerate_combo.addItems(["15", "30", "60"])
        self.framerate_combo.currentIndexChanged.connect(self.update_framerate)

        # Compression selection
        self.compression_label = QtWidgets.QLabel("Select Compression:")
        self.compression_combo = QtWidgets.QComboBox()
        self.compression_combo.addItems(["None", "Low", "Medium", "High"])
        self.compression_combo.currentIndexChanged.connect(self.update_compression)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.framerate_label)
        layout.addWidget(self.framerate_combo)
        layout.addWidget(self.compression_label)
        layout.addWidget(self.compression_combo)

        self.setLayout(layout)

    def update_framerate(self):
        framerate = int(self.framerate_combo.currentText())
        self.camera_controller.set_framerate(framerate)

    def update_compression(self):
        compression = self.compression_combo.currentText()
        self.camera_controller.set_compression(compression)