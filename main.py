import cv2
import mediapipe as mp
import pyautogui as pg
import asyncio


CLICK = 0.05


async def mouse_move(x, y):
    try:
        pg.moveTo(x, y)
    except:
        pass


pg.FAILSAFE = False

vid = cv2.VideoCapture(0)
handsDetector = mp.solutions.hands.Hands()

z0 = -1

while True:
    ret, frame = vid.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = handsDetector.process(frame)
    if results.multi_hand_landmarks is not None:
        fingers = results.multi_hand_landmarks[0].landmark-
        if z0 == -1:
            z0 = fingers[8].z
        print(z0, fingers[8].z, z0 - fingers[8].z)
        if z0 - fingers[8].z >= CLICK:
            print("CLICK")
            pg.click()

        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            results.multi_hand_landmarks[0],
            mp.solutions.hands.HAND_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
            mp.solutions.drawing_styles.get_default_hand_connections_style(),
        )

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()
