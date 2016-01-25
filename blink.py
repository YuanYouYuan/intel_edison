import mraa
import time
import sys

pin = int(sys.argv[-1])
x = mraa.Gpio(pin)
x.dir(mraa.DIR_OUT)

while True:
	x.write(1)
	time.sleep(1)
	print pin, "ON"
	x.write(0)
	time.sleep(1)
	print pin, "OFF"
