import mraa
import time

pin = [3, 5, 6, 9]
servo = []
for p in pin:
    servo.append(mraa.Pwm(p))
    
for s in servo:
    s.period_us(20000) #50Hz
    s.enable(False)

max_duty = 2300.0 #us
min_duty = 500.0

def servo_rotate(servo_number, degree): #servo_number (0, 1, 2, 3) = (3, 5, 6, 9)
    duty_cycle = ((max_duty - min_duty) * degree / 180.0 + min_duty) / 20000.0
    servo[servo_number].enable(True)
    servo[servo_number].write(duty_cycle)
    # print "duty_cycle = ", duty_cycle, "\n"


for s in servo:
    s.enable(False)

motion_idle = [80, 130, 50, 40]

motion_grip = []
motion_grip.append(motion_idle)
motion_grip.append([80, 70, 130, 40]) #down
motion_grip.append([80, 130, 130, 160]) #strecth and catch
motion_grip.append([80, 130, 50, 160]) #lift
motion_grip.append([180, 130, 50, 160])
motion_grip.append([180, 130, 50, 40])



while True:
    for m in motion_grip:
        for i in range(len(m)):
            servo_rotate(i, m[i])
        time.sleep(1)



