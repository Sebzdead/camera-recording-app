import cv2
import os
import time
import numpy as np

class VideoRecorder:
    def __init__(self, output_directory, framerate=25, codec='H264', feed_width=4000, feed_height=3000):
        self.output_directory = output_directory
        self.framerate = framerate
        self.codec = codec
        self.feed_width = feed_width
        self.feed_height = feed_height
        self.is_recording = False
        self.video_writer = None

    def start_recording(self, filename):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        
        try:
            fourcc = cv2.VideoWriter_fourcc(*self.codec)
            output_path = os.path.join(self.output_directory, filename)
            self.video_writer = cv2.VideoWriter(
                output_path, 
                fourcc, 
                self.framerate, 
                (self.feed_width, self.feed_height)
            )
            
            if not self.video_writer.isOpened():
                print(f"Error: Failed to open video writer with codec {self.codec}")
                return False
                
            self.is_recording = True
            return True
        except Exception as e:
            print(f"Error starting recording: {str(e)}")
            return False

    def stop_recording(self):
        if self.is_recording and self.video_writer is not None:
            try:
                self.video_writer.release()
            except Exception as e:
                print(f"Error stopping recording: {str(e)}")
            finally:
                self.is_recording = False

    def record_frame(self, frame):
        if not self.is_recording or self.video_writer is None:
            return False
            
        try:
            # Validate frame
            if frame is None or not isinstance(frame, np.ndarray):
                return False
                
            # Check frame dimensions match expected dimensions
            if frame.shape[1] != self.feed_width or frame.shape[0] != self.feed_height:
                # Resize frame if dimensions don't match
                frame = cv2.resize(frame, (self.feed_width, self.feed_height))
                
            self.video_writer.write(frame)
            return True
        except Exception as e:
            print(f"Error recording frame: {str(e)}")
            return False

    def record_for_duration(self, duration):
        start_time = time.time()
        while self.is_recording and (time.time() - start_time) < duration:
            pass  # This would be replaced with actual frame capturing logic

    def is_recording_active(self):
        return self.is_recording