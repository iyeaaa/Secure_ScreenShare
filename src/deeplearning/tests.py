import mss
import numpy as np
import cv2

with mss.mss() as sct:
    monitor = sct.monitors[1]
    while True:
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        cv2.imshow("Screen Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
