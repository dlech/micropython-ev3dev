#!/usr/bin/env micropython
"""Sample program using EXPLOR3R"""

from uev3dev import *

# init display
display = Display()
fbuf, fbuf_data = display.framebuffer()

# init motors
left_motor = LargeMotor('B')
right_motor = LargeMotor('C')


# fun with I2C

in4 = EV3InputPort('4')
in4.mode = 'other-i2c'
bus4 = SMBus('/dev/i2c-in4')
bus4.set_address(0x01)

firmware = bytes(bus4.read_i2c_block_data(0x00, 8)).decode().strip()
vendor = bytes(bus4.read_i2c_block_data(0x08, 8)).decode().strip()
product = bytes(bus4.read_i2c_block_data(0x10, 8)).decode().strip()
debug_print(firmware, vendor, product)

if vendor != 'mndsnsrs' or product != 'NXTcam5':
    raise ValueError('Wrong sensor')


# functions

def scale(x1, y1, x2, y2):
    """Convert points from NXTCam to screen rectangle"""
    x1 = x1 * display.width // 240
    y1 = y1 * display.height // 160
    x2 = x2 * display.width // 240
    y2 = y2 * display.height // 160
    return x1, y1, x2 - x1, y2 - y1


# Main loop

bus4.write_byte_data(0x41, 0x46)  # set face tracking mode

while True:
    n = bus4.read_byte_data(0x42)
    fbuf.fill(1)
    for i in range(0, n):
        data = bus4.read_i2c_block_data(0x43 + i * 5, 5)
        color = data[0]
        x1 = data[1]
        y1 = data[2]
        x2 = data[3]
        y2 = data[4]
        x, y, w, h = scale(x1, y1, x2, y2)
        fbuf.rect(x, y, w, h, 0)
    display.update(fbuf_data)

    speed = n and ((x1 + x2 // 2) - 128) // 4
    left_motor.on_unregulated(-speed)
    right_motor.on_unregulated(speed)
