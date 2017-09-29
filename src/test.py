#!/usr/bin/env micropython
"""Test program for testing whatever"""

import time

from uev3dev.messaging import BluetoothRemote
from uev3dev.messaging import BluetoothServer
from uev3dev.util import debug_print

bt = BluetoothRemote('00:16:53:4c:5b:1f')
w = bt._sock.write(b'\x0C\x00\x00\x00\x80\x00\x00\xA4\x00\x01\x14\xA6\x00\x01')
debug_print(w)
time.sleep(5)
w = bt._sock.write(b'\x09\x00\x01\x00\x80\x00\x00\xA3\x00\x01\x00')
debug_print(w)

bt.close()

bt = BluetoothServer()
bt.start()
bt._accept()
bt.close()
