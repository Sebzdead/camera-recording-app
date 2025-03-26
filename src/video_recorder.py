import cv2
import os
import time

class VideoRecorder:
    def __init__(self, output_directory, framerate=30, codec='XVID'):
        self.output_directory = output_directory
        self.framerate = framerate
        self.codec = codec
        self.is_recording = False
        self.video_writer = None

    def start_recording(self, filename):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        output_path = os.path.join(self.output_directory, filename)
        self.video_writer = cv2.VideoWriter(output_path, fourcc, self.framerate, (640, 480))
        self.is_recording = True

    def stop_recording(self):
        if self.is_recording:
            self.video_writer.release()
            self.is_recording = False

    def record_frame(self, frame):
        if self.is_recording and self.video_writer is not None:
            self.video_writer.write(frame)

    def record_for_duration(self, duration):
        start_time = time.time()
        while self.is_recording and (time.time() - start_time) < duration:
            pass  # This would be replaced with actual frame capturing logic

    def is_recording_active(self):
        return self.is_recording