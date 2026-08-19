import mss

def _get_mss():
    """Compatibility shim: newer mss uses MSS(), older uses mss()."""
    return mss.MSS() if hasattr(mss, "MSS") else mss.mss()

def list_monitors():
    """Returns info on all connected monitors (index 0 = 'all monitors combined')."""
    with _get_mss() as sct:
        return sct.monitors

def get_primary_monitor():
    """Returns dict with top/left/width/height of the main monitor."""
    with _get_mss() as sct:
        return sct.monitors[1]

if __name__ == "__main__":
    print(list_monitors())