import cv2
import pyautogui as pg
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
import numpy as np


START_DIST = 0.05
STOP_DELAY = 1
TEXT_MOVED = 10
COLOR = (57, 237, 111)

last_active = 0
activated = False

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_cast = cast(interface, POINTER(IAudioEndpointVolume))
vol_min, vol_max = volume_cast.GetVolumeRange()[:2]


def dist(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def volume(fingers, frame):
    global activated, last_active

    if time.time() - last_active >= STOP_DELAY:
        activated = False
    if dist(fingers[4], fingers[8]) <= START_DIST:
        activated = True
    if not activated:
        return

    x4, y4 = int(fingers[4].x * frame.shape[1]), int(fingers[4].y * frame.shape[0])
    x8, y8 = int(fingers[8].x * frame.shape[1]), int(fingers[8].y * frame.shape[0])

    cv2.circle(frame, (x4, y4), 10, COLOR, -1, 0)
    cv2.circle(frame, (x8, y8), 10, COLOR, -1, 0)
    cv2.line(frame, (x4, y4), (x8, y8), COLOR, 5)

    vol1 = np.interp(dist(fingers[4], fingers[8]), [0, 0.35], [vol_min, vol_max])
    vol2 = np.interp(dist(fingers[4], fingers[8]), [0, 0.35], [0, 100])
    volume_cast.SetMasterVolumeLevel(vol1, None)
    cv2.putText(
        frame,
        f"{round(vol2)}%",
        ((x4 + x8) // 2 + TEXT_MOVED, (y4 + y8) // 2),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        COLOR,
        2,
    )

    last_active = time.time()
