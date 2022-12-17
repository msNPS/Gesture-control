import cv2
import pyautogui as pg
import time
import ctypes
import win32api
import webbrowser


DISPLAY_SIZE = 0.7  # Configurations
CLICK_DIST = 0.05
DESKTOP_DIST = 0.1
SWITCH_DIST = 0.33
PAUSE_DIST = 0.04
LOCK_DIST = 0.06
FUN_DIST = 0.05
DELAY = 1.5
MOUSE_COLOR = (255, 157, 0)
PAUSE_COLOR = (222, 40, 107)

last_gesture = 0  # Temporary variable

VK_MEDIA_PLAY_PAUSE = 0xB3  # Pause setup
hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)


def dist(p1, p2):  # Distance between 2 points
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def mouse(fingers, frame):  # Mouse control gesture
    global last_gesture
    try:
        if (
            dist(fingers[0], fingers[12]) < dist(fingers[0], fingers[9])
            and dist(fingers[0], fingers[16]) < dist(fingers[0], fingers[13])
            and dist(fingers[0], fingers[20]) < dist(fingers[0], fingers[17])
        ):  # Gesture check
            pg.moveTo(
                max(fingers[8].x - (1 - DISPLAY_SIZE) / 2, 0) * pg.size()[0] / DISPLAY_SIZE,
                max(fingers[8].y - (1 - DISPLAY_SIZE) / 2, 0) * pg.size()[1] / DISPLAY_SIZE,
                duration=0.0,
                tween=pg.linear,
                logScreenshot=False,
                _pause=False,
            )  # move mouse
            cv2.circle(
                frame,
                (int(fingers[8].x * frame.shape[1]), int(fingers[8].y * frame.shape[0])),
                15,
                MOUSE_COLOR,
                5,
            )
            if dist(fingers[4], fingers[10]) <= CLICK_DIST:
                if time.time() - last_gesture >= DELAY:
                    pg.click()  # Click gesture
                    last_gesture = time.time()
                cv2.circle(
                    frame,
                    (int(fingers[10].x * frame.shape[1]), int(fingers[10].y * frame.shape[0])),
                    15,
                    MOUSE_COLOR,
                    -1,
                )
    except:
        pass


def lock(fingers):  # Lock pc gesture
    global last_gesture
    try:
        if (
            fingers[5].x > fingers[17].x
            and dist(fingers[0], fingers[5]) - dist(fingers[0], fingers[8]) >= LOCK_DIST
            and dist(fingers[0], fingers[9]) - dist(fingers[0], fingers[12]) >= LOCK_DIST
            and dist(fingers[0], fingers[13]) - dist(fingers[0], fingers[16]) >= LOCK_DIST
            and dist(fingers[0], fingers[17]) - dist(fingers[0], fingers[20]) >= LOCK_DIST
        ):  # Gesture check
            ctypes.windll.user32.LockWorkStation()
    except:
        pass


def desktop(fingers):  # Close all windows gesture
    global last_gesture
    try:
        if (
            fingers[12].y > fingers[0].y
            and dist(fingers[0], fingers[12]) >= DESKTOP_DIST
            and time.time() - last_gesture >= DELAY
        ):  # Gesture check
            pg.hotkey("win", "d")
            last_gesture = time.time()
    except:
        pass


def switch(fingers):  # Switch between windows gesture
    global last_gesture
    try:
        if (
            fingers[4].x > fingers[20].x
            and dist(fingers[4], fingers[20]) > SWITCH_DIST
            and time.time() - last_gesture >= DELAY
        ):  # Gesture check
            pg.hotkey("alt", "tab")
            last_gesture = time.time()
    except:
        pass


def pause(fingers, frame):  # Pause the media
    global last_gesture
    try:  # Gesture check
        if dist(fingers[4], fingers[8]) <= PAUSE_DIST and dist(fingers[4], fingers[12]) <= PAUSE_DIST:
            if time.time() - last_gesture >= DELAY:
                win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)
                last_gesture = time.time()
            cv2.circle(
                frame,
                (int(fingers[4].x * frame.shape[1]), int(fingers[4].y * frame.shape[0])),
                25,
                PAUSE_COLOR,
                8,
            )
    except:
        pass


def fun(fingers):
    global last_gesture
    try:  # Gesture check
        if (
            fingers[4].x < fingers[20].x
            and fingers[12].x < fingers[8].x
            and time.time() - last_gesture >= DELAY
        ):
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            last_gesture = time.time()
    except:
        pass
