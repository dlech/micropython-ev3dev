
import time
import _thread


class Messaging():
    def wait_update(self, title):
        # FIXME: implement messaging
        self._lock = _thread.allocate_lock()
        self._lock.acquire()
        # just wait forever for now
        self._lock.acquire()
