import cv2
import pyautogui as pg
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
import numpy as np


START_DIST = 0.05
STOP_DELAY = 1

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
    # try:
    if dist(fingers[4], fingers[8]) <= START_DIST:
        activated = True
    if not activated:
        return

    cv2.circle(
        frame,
        (int(fingers[4].x * frame.shape[1]), int(fingers[4].y * frame.shape[0])),
        10,
        (255, 0, 0),
        -1,
    )
    cv2.circle(
        frame,
        (int(fingers[8].x * frame.shape[1]), int(fingers[8].y * frame.shape[0])),
        10,
        (255, 0, 0),
        -1,
    )
    cv2.line(
        frame,
        (int(fingers[4].x * frame.shape[1]), int(fingers[4].y * frame.shape[0])),
        (int(fingers[8].x * frame.shape[1]), int(fingers[8].y * frame.shape[0])),
        (255, 0, 0),
        5,
    )
    print(dist(fingers[4], fingers[8]))
    vol = np.interp(dist(fingers[4], fingers[8]), [0, 0.35], [vol_min, vol_max])
    volume_cast.SetMasterVolumeLevel(vol, None)
    last_active = time.time()
    # except:
    #     pass
