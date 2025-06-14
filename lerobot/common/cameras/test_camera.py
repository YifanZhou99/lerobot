import cv2
from lerobot.common.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.common.cameras.opencv.camera_opencv import OpenCVCamera
from lerobot.common.cameras.configs import ColorMode, Cv2Rotation

# Construct an `OpenCVCameraConfig` with your desired FPS, resolution, color mode, and rotation.
config = OpenCVCameraConfig(
    index_or_path='/dev/video2',
    fps=30,
    width=640,
    height=480,
    color_mode=ColorMode.RGB,  # This may not guarantee RGB in the raw frame, so we'll manually convert
    rotation=Cv2Rotation.NO_ROTATION
)

# Instantiate and connect an `OpenCVCamera`, performing a warm-up read (default).
camera = OpenCVCamera(config)
camera.connect()

# Read frames asynchronously in a loop via `async_read(timeout_ms)`
try:
    for i in range(10000):
        frame = camera.async_read(timeout_ms=200)
        if frame is not None:
            print(f"Async frame {i} shape:", frame.shape)
            # Convert BGR to RGB for accurate color display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow("Camera Frame", frame_rgb)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print(f"Frame {i} is None")
finally:
    camera.disconnect()
    cv2.destroyAllWindows()
