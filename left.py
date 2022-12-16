import cv2
import pyautogui as pg
import time


START_DIST = 0.05
STOP_DELAY = 1

last_active = 0
activated = False


def dist(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def volume(fingers, frame):
    global activated, last_active
    if time.time() - last_active >= STOP_DELAY:
        activated = False
    try:
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
        last_active = time.time()
    except:
        pass
