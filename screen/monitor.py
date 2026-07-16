import mss

def list_monitors():
    """Returns info on all connected monitors (index 0 = 'all monitors combined')."""
    with mss.MSS() as sct:
        return sct.monitors

def get_primary_monitor():
    """Returns dict with top/left/width/height of the main monitor."""
    with mss.MSS() as sct:
        return sct.monitors[1]  # index 0 is the combined virtual screen

if __name__ == "__main__":
    print(list_monitors())