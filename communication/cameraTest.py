from picamera import PiCamera


# Initialize the camera
camera = PiCamera()

# Optional: Configure camera settings (resolution, rotation, etc.)
# camera.resolution = (1024, 768)  # You can adjust the resolution
# camera.rotation = 0  # Rotate the image if necessary

# # Start the camera preview (useful if you're connected to a display)
# camera.start_preview()

# # Optional: Sleep for a few seconds to allow the camera to adjust
# sleep(2)

# Capture the image and save it to a file
camera.capture('/home/pi/Desktop/image.jpg')

# # Stop the camera preview
# camera.stop_preview()

# Close the camera to release resources
camera.close()

