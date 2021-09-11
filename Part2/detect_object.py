# Things to detect:
# 0. Empty space
# 1. Walls/Solid objects
# 2. Stop signs - Come to complete stop, look around for traffic, then continue moving
# 3. Traffic cones - Reduce power to 20
# 4. Not defined
# 5. Not defined
# 6. Not defined
# 7. Not defined
# 8. Not defined
# 9. Current car position

from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image

class Eye:

    def __init__(self):
        self.stream = BytesIO()
        self.camera = PiCamera()
        self.camera.start_preview()
        self.image = None

    def captureImage(self):
        self.camera.capture(self.stream, format='jpeg')
        # "Rewind" the stream to the beginning so we can read its content
        self.stream.seek(0)
        self.image = Image.open(self.stream)

    def classifyImage(self):
        self.image.show()

