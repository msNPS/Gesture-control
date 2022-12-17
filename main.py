import cv2
import mediapipe as mp
import right
import left


def camera_loop():  # Main camera cycle
    run = True
    vid = cv2.VideoCapture(0)
    handsDetector = mp.solutions.hands.Hands(max_num_hands=2)

    while run:
        _, frame = vid.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = handsDetector.process(frame)  # Analyze hands
        if results.multi_hand_landmarks is not None:
            for hand in range(len(results.multi_handedness)):
                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    results.multi_hand_landmarks[hand],
                    mp.solutions.hands.HAND_CONNECTIONS,
                )  # Draw hand connections
                fingers = results.multi_hand_landmarks[hand].landmark
                if "Right" in str(results.multi_handedness[hand]):
                    right.mouse(fingers, frame)  # Right hand
                    right.lock(fingers)
                    right.desktop(fingers)
                    right.switch(fingers)
                    right.pause(fingers, frame)
                else:
                    left.volume(fingers, frame)  # Left hand

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Show the frame
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            run = False

    vid.release()  # Close the program
    cv2.destroyAllWindows()


camera_loop()
