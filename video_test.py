import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(3, 300)
cap.set(4, 300)


video = cv2.VideoWriter("video_test.avi", cv2.cv.FOURCC('m','p','4','v'), 20, (300, 300))
timer = time.time()
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        video.write(frame)
        cv2.imshow("video stream", frame)
    else:
        break
    if time.time() - timer > 3:
        break


