#!/usr/bin/env micropython
"""Sample program using EXPLOR3R"""

# import framebuf
import os
import utime

from uev3dev import *

left_motor = LargeMotor(OutputPort.B)
right_motor = LargeMotor(OutputPort.C)
us_sensor = Ev3UltrasonicSensor(InputPort.N4)

# fbuf = framebuf.FrameBuffer(bytearray((178 + 7) / 8 * 128), 178, 128,
#                             framebuf.MVLSB, (178 + 7) / 8)

left_motor.run_for_rotations(400, 1, wait=False)
right_motor.run_for_rotations(-400, 1)

right_motor.run_for_rotations(400, 1, wait=False)
left_motor.run_for_rotations(-400, 1)

os.system('beep -f 100 -n -f 200')
utime.sleep(2)

while True:
    dist = us_sensor.read_cm()
    # fbuf.fill(0)
    # fbuf.text(dist, 50, 50)
    if dist > 30:
        left_motor.run(400)
        right_motor.run(400)
    elif dist < 15:
        left_motor.run(-400)
        right_motor.run(-400)
    else:
        left_motor.stop()
        right_motor.stop()
