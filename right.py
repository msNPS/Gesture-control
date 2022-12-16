import pyautogui as pg
import time
import ctypes
import win32api


DISPLAY_SIZE = 0.7
CLICK_DIST = 0.05
DESKTOP_DIST = 0.1
SWITCH_DIST = 0.35
PAUSE_DIST = 0.04
DELAY = 1

last_gesture = 0

VK_MEDIA_PLAY_PAUSE = 0xB3
hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)


def dist(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def mouse(fingers):
    global last_gesture
    try:
        if (
            dist(fingers[0], fingers[12]) < dist(fingers[0], fingers[9])
            and dist(fingers[0], fingers[16]) < dist(fingers[0], fingers[13])
            and dist(fingers[0], fingers[20]) < dist(fingers[0], fingers[17])
        ):
            pg.moveTo(
                max(fingers[8].x - (1 - DISPLAY_SIZE) / 2, 0) * pg.size()[0] / DISPLAY_SIZE,
                max(fingers[8].y - (1 - DISPLAY_SIZE) / 2, 0) * pg.size()[1] / DISPLAY_SIZE,
                duration=0.0,
                tween=pg.linear,
                logScreenshot=False,
                _pause=False,
            )
            if dist(fingers[4], fingers[10]) <= CLICK_DIST and time.time() - last_gesture >= DELAY:
                pg.click()
                last_gesture = time.time()
    except:
        pass


def lock(fingers):
    global last_gesture
    try:
        if (
            fingers[5].x > fingers[17].x
            and dist(fingers[0], fingers[8]) < dist(fingers[0], fingers[5])
            and dist(fingers[0], fingers[12]) < dist(fingers[0], fingers[9])
            and dist(fingers[0], fingers[16]) < dist(fingers[0], fingers[13])
            and dist(fingers[0], fingers[20]) < dist(fingers[0], fingers[17])
        ):
            ctypes.windll.user32.LockWorkStation()
    except:
        pass


def desktop(fingers):
    global last_gesture
    try:
        if (
            fingers[12].y > fingers[0].y
            and dist(fingers[0], fingers[12]) >= DESKTOP_DIST
            and time.time() - last_gesture >= DELAY
        ):
            pg.hotkey("win", "d")
            last_gesture = time.time()
    except:
        pass


def switch(fingers):
    global last_gesture
    try:
        if (
            fingers[4].x > fingers[20].x
            and dist(fingers[4], fingers[20]) > SWITCH_DIST
            and time.time() - last_gesture >= DELAY
        ):
            pg.hotkey("alt", "tab")
            last_gesture = time.time()
    except:
        pass


def pause(fingers):
    global last_gesture
    try:
        if (
            dist(fingers[4], fingers[8]) <= PAUSE_DIST
            and dist(fingers[4], fingers[12]) <= PAUSE_DIST
            and time.time() - last_gesture >= DELAY
        ):
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)
            last_gesture = time.time()
    except:
        pass
