import mraa
import sys
import time

pin = [3, 5, 6, 9]
servo = []
for p in pin:
    servo.append(mraa.Pwm(p))
    
for s in servo:
    s.period_us(20000) #50Hz
    s.enable(True)

max_duty = 2300.0 #us
min_duty = 500.0

def servo_rotate(pin_number, degree):
    duty_cycle = ((max_duty - min_duty) * degree / 180.0 + min_duty) / 20000.0
    servo[pin.index(pin_number)].enable(True)
    servo[pin.index(pin_number)].write(duty_cycle)
    print "duty_cycle = ", duty_cycle, "\n"

dt = 0.01

for s in servo:
    s.enable(False)



pin_number = int(sys.argv[-1])
#servo[pin.index(pin_number)].enable(True)



while True:
    for d in range(180):
        servo_rotate(pin_number, d)
        time.sleep(dt)
        print "degree = ", d

    for d in range(180):
        servo_rotate(pin_number, 180 - d)
        time.sleep(dt)
        print "degree = ", d

