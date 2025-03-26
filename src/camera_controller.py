import cv2

class CameraController:
    def __init__(self, camera_index=0):
        import EasyPySpin
        self.camera = EasyPySpin.VideoCapture(camera_index)
        self.framerate = 25  # Default framerate
        self.compression = 'MJPG'  # Default compression
        self.is_recording = False
        
        # Initialize the camera with default settings
        if self.camera.isOpened():
            self.set_framerate(self.framerate)

    def start_feed(self):
        if not self.camera.isOpened():
            self.camera.open()

    def stop_feed(self):
        if self.camera.isOpened():
            self.camera.release()

    def set_framerate(self, framerate):
        self.framerate = framerate
        self.camera.set(cv2.CAP_PROP_FPS, self.framerate)

    def set_compression(self, compression):
        self.compression = compression
        # Note: Compression handling would depend on the specific implementation of EasyPySpin

    def get_frame(self):
        if self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None

    def start_recording(self, filename):
        self.is_recording = True
        # Implement recording logic using VideoRecorder class

    def stop_recording(self):
        self.is_recording = False
        # Implement logic to stop recording and save the video file