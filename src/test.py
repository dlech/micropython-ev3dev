#!/usr/bin/env micropython
"""Sample program using EXPLOR3R"""

import uos
import utime

from uev3dev import *

# init motors
left_motor = LargeMotor(OutputPort.B)
right_motor = LargeMotor(OutputPort.C)
us_sensor = Ev3UltrasonicSensor(InputPort.N4)

# init display
display = Display()
fbuf, fbuf_data = display.framebuffer()

# do a little song and dance

left_motor.run_for_rotations(400, 1, wait=False)
right_motor.run_for_rotations(-400, 1)

right_motor.run_for_rotations(400, 1, wait=False)
left_motor.run_for_rotations(-400, 1)

uos.system('beep -f 100 -n -f 200')
utime.sleep(2)

# now, a "real" program
while True:
    dist = us_sensor.read_cm()
    fbuf.fill(1)
    fbuf.text(str(dist), 50, 50, 0)
    display.update(fbuf_data)
    if dist > 50:
        left_motor.run(400)
        right_motor.run(400)
    elif dist < 25:
        left_motor.run(-400)
        right_motor.run(-400)
    else:
        left_motor.stop()
        right_motor.stop()
