import mraa
import time
import sys


pin = int(sys.argv[-1])
x = mraa.Pwm(pin)
x.period_us(20000)
x.enable(True)

max_duty = 2.4 / 20
min_duty = 0.5 / 20

while True:
	x.write(max_duty)
	time.sleep(0.5)
	x.write(min_duty)
	time.sleep(0.5)
