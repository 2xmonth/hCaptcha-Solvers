import pyautogui
from curves.humancurve import HumanCurve

def setup_pyautogui():
    # Any duration less than this is rounded to 0.0 to instantly move the mouse.
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    # Minimal number of seconds to sleep between mouse moves.
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    # The number of seconds to pause after EVERY public function call.
    pyautogui.PAUSE = 0.015  # Default: 0.1

setup_pyautogui()

class HumanClicker():
    points = []
    def __init__(self):
        pass

    def get_points(self, humanCurve=None, start=None, end=None, **kwargs):
        """Adapted for my ReCAPTCHA solver. original is at github.com/patrikoss/pyclick/"""
        points = []
        if not humanCurve:
            humanCurve = HumanCurve(start, end, **kwargs)

        for point in humanCurve.points:
            points.append(point)

        return points
