from picamera2 import Picamera2
import time

def capture_image():
    picam2 = Picamera2()
    picam2.start_preview()  # Start the camera preview (optional for still images)
    time.sleep(2)  # Allow some time for camera to adjust settings
    
    # Configure the camera settings (if needed)
    picam2.configure(picam2.create_still_configuration())

    # Capture the image
    picam2.capture_file("captured_image.jpg")
    print("Image captured successfully!")

if __name__ == "__main__":
    capture_image()
