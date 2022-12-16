import cv2
import mediapipe as mp
import pyautogui as pg
import numpy
import time
import ctypes


CLICK_DIST = 0.05
CLICK_TIME = 2
DESKTOP_DIST = 0.1
DESKTOP_DELAY = 1
SWITCH_DIST = 0.38


last_desktop = 0


def dist(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def rel_dist(p):
    global fingers
    return dist(fingers[0], p)


def gesture_mouse(fingers):
    try:
        if (
            time.time() - last_desktop >= DESKTOP_DELAY
            and rel_dist(fingers[12]) < rel_dist(fingers[9])
            and rel_dist(fingers[16]) < rel_dist(fingers[13])
            and rel_dist(fingers[20]) < rel_dist(fingers[17])
        ):
            pg.moveTo(
                fingers[8].x * pg.size()[0],
                fingers[8].y * pg.size()[1],
                duration=0.0,
                tween=pg.linear,
                logScreenshot=False,
                _pause=False,
            )
    except:
        pass


def gesture_lock(fingers):
    try:
        if (
            fingers[5].x > fingers[17].x
            and rel_dist(fingers[8]) < rel_dist(fingers[5])
            and rel_dist(fingers[12]) < rel_dist(fingers[9])
            and rel_dist(fingers[16]) < rel_dist(fingers[13])
            and rel_dist(fingers[20]) < rel_dist(fingers[17])
        ):
            ctypes.windll.user32.LockWorkStation()
    except:
        pass


def gesture_desktop(fingers):
    global last_desktop
    try:
        if (
            fingers[12].y > fingers[0].y
            and rel_dist(fingers[12]) >= DESKTOP_DIST
            and time.time() - last_desktop >= DESKTOP_DELAY
        ):
            last_desktop = time.time()
            pg.hotkey("win", "d")
    except:
        pass


def gesture_switch(fingers):
    global last_desktop
    try:
        if fingers[4].x > fingers[20].x and dist(fingers[4], fingers[20]) > SWITCH_DIST:
            pg.hotkey("alt", "tab")
    except:
        pass


def camera_loop():
    global run, fingers

    run = True
    vid = cv2.VideoCapture(0)
    handsDetector = mp.solutions.hands.Hands()

    while run:
        _, frame = vid.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = handsDetector.process(frame)
        if results.multi_hand_landmarks is not None:
            fingers = results.multi_hand_landmarks[0].landmark
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.multi_hand_landmarks[0],
                mp.solutions.hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                mp.solutions.drawing_styles.get_default_hand_connections_style(),
            )

            gestures = [gesture_mouse, gesture_lock, gesture_desktop, gesture_switch]
            for gesture in gestures:
                gesture(fingers)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            run = False

    vid.release()
    cv2.destroyAllWindows()


camera_loop()
