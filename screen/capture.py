import mss
import base64
from io import BytesIO
from PIL import Image
from screen.monitor import get_primary_monitor

def capture_screen(monitor=None):
    """Capture a screenshot and return it as a PIL Image."""
    with mss.MSS() as sct:
        region = monitor or get_primary_monitor()
        shot = sct.grab(region)
        img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        return img

def capture_as_base64(monitor=None):
    """Capture and return base64 string, ready to send to a vision LLM API."""
    img = capture_screen(monitor)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

if __name__ == "__main__":
    img = capture_screen()
    img.save("test_screenshot.png")
    print("Saved test_screenshot.png")