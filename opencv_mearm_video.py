import cv2
import numpy as np
import mraa
import time

pin = [3, 5, 6, 9]
servo = []
for p in pin:
    servo.append(mraa.Pwm(p))

for s in servo:
    s.period_us(20000)
    s.enable(False)

max_duty = 2300.0 #us
min_duty = 500.0

def servo_rotate(servo_number, degree): #servo_number (0, 1, 2, 3) = (3, 5, 6, 9)
    duty_cycle = ((max_duty - min_duty) * degree / 180.0 + min_duty) / 20000.0
    servo[servo_number].enable(True)
    servo[servo_number].write(duty_cycle)
    # print "duty_cycle = ", duty_cycle, "\n"



def grip_motion(object_direction):
    for s in servo:
        s.enable(True)

    motion_idle = [object_direction, 130, 50, 40] #targeted
    for i in range(len(motion_idle)):
        servo_rotate(i, motion_idle[i])
    time.sleep(1)
    servo_rotate(1, 70) #down
    servo_rotate(2, 130) #down
    time.sleep(1)
    for deg in range(130 - 70):
        servo_rotate(1, 70 + deg)
        time.sleep(0.01)
    # servo_rotate(1, 130) #strecth
    servo_rotate(3, 160) #catch
    time.sleep(1)
    servo_rotate(2, 50) #lift
    time.sleep(1)
    servo_rotate(0, 150) #rotate
    time.sleep(1)
    servo_rotate(3, 40) #release
    time.sleep(1)

    for s in servo:
        s.enable(False)

window_size = 500
cap = cv2.VideoCapture(0)
cap.set(3, window_size)
cap.set(4, window_size)

video = cv2.VideoWriter("video_test.avi", cv2.cv.FOURCC('m', 'p', '4', 'v'), 5, (window_size, window_size))


lower_bound = np.array([0,0,0])
upper_bound = np.array([0,0,0])
font = cv2.FONT_HERSHEY_SIMPLEX


def print_hsv(frame, lower_bound, upper_bound):
    cv2.putText(frame, "lower_bound: " + str(lower_bound), (5,window_size - 20), font, 0.4, (0,255,255), 1)
    cv2.putText(frame, "upper_bound: " + str(upper_bound), (5,window_size - 40), font, 0.4, (0,255,255), 1)

lower_bound[0] = 20
lower_bound[1] = 0
lower_bound[2] = 90
                
upper_bound[0] = 45
upper_bound[1] = 255
upper_bound[2] = 255

def object_direction(x_err):
    if x_err < 100:
        return 70
    elif x_err > 150:
        return 90
    else:
        return 80


sum_x_err = 0
x_err = 0
last_x_err = 0
count = 0
sample_number = 5
rectangle_color = (0, 255, 0)
rectangle_color = (0, 0, 255)

while True:

    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    mask = cv2.erode(mask, None, iterations = 3)
    mask = cv2.dilate(mask, None, iterations = 3)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
#    print "cnts = ", len(cnts)
    print "hsv_value = ", hsv[int(window_size / 2), int(window_size / 2)]
    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), rectangle_color, 2)
        print "area ", h * w
        if  h > w and h * w > 10000:
            last_x_err = x_err
            x_err = window_size / 2 - x
            if abs(x_err - last_x_err) > 200:
                sum_x_err = 0
                count = 0
                rectangle_color = (0, 255, 0)
            elif count > sample_number:
                mean_x_err = sum_x_err / count
                sum_x_err = 0
                count = 0
                rectangle_color = (0, 0, 255)
                print "mean x err = ", mean_x_err
                print "direction = ",object_direction(mean_x_err)
                grip_motion(object_direction(mean_x_err))
            else:
                rectangle_color = (0, 255, 0)
                print "x_err = ", x_err
                sum_x_err += x_err
                count += 1
                print "count = ", count
            print "got it!"
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        video.write(frame)
           
    print_hsv(frame, lower_bound, upper_bound)
    cv2.imwrite("contour_test.jpg", frame)


