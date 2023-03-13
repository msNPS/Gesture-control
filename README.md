# Computer vision Gesture control

![1671270762383](image/README/1671270762383.png)

## Description

After starting the program, a window with a camera view appears. On it, the camera recognizes hands and gestures. All actions except the last one are performed with the right hand. The camera can recognize both hands at the same time. However, make sure that there are no strangers in the frame.

## All gestures

1. **Swipe left**
    to switch between windows *(similar to Alt+Tab)*
2. **Swipe down**
    to minimize all windows and open the desktop *(similar to Win+D)*
3. **Make a fist and rotate it horizontally**
    to lock the computer *(similar to Win+L)*
4. **Make a fist and raise your index finger**
    to control the computer cursor, the cursor now follows the movements of the index finger
5. **Tap your middle finger**
    to click with the left mouse button
6. **Connect the first 3 fingers**
    to stop/resume video or audio playback
7. **Cross your middle and index fingers**
    to get a surprise
8. **Connect the index and thumb of the left hand**
    to control computer volume, the distance between the index finger and thumb of the left hand is now directly correlated with computer volume. *To stop driving, remove your left hand from the camera's field of view*

## Libraries

The project uses many different libraries. Their full list and role in the project:

* **opencv** - read image from camera, work with it
* **mediapipe** - hand recognition
* **pyautogui** - computer automation
* **time** - measure the delay between actions
* **win32api** - media pause
* **ctypesctypes, comtypes, pycaw** - change computer volume
* **numpy** - converting a number from one segment to another
* **webbrowser** - open links in browser
