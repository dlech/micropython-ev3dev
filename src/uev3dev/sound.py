
import _thread
import ffilib
import os

from multiprocessing import Process
from time import sleep

from uctypes import addressof
from uctypes import INT32
from uctypes import sizeof
from uctypes import struct
from uctypes import UINT16
from uctypes import UINT64

from uev3dev.util import Timeout

# TODO: signal.SIGKILL is not defined in micropython-lib
_SIGKILL = 9
_SIGTERM = 15

_BEEP_DEV = '/dev/input/by-path/platform-sound-event'


# stuff from linux/prctl.h

_libc = ffilib.libc()
_prctl = _libc.func('i', 'prctl', 'il')
_PR_SET_PDEATHSIG = 1

# stuff from linux/input.h and linux/input-event-codes.h

_EV_SND = 0x12
_SND_TONE = 0x02
_input_event = {
    'time': UINT64 | 0,  # struct timeval
    'type': UINT16 | 8,
    'code': UINT16 | 10,
    'value': INT32 | 12,
}

# from lms2012

_NOTES = {
  'C4': 262,
  'D4': 294,
  'E4': 330,
  'F4': 349,
  'G4': 392,
  'A4': 440,
  'B4': 494,
  'C5': 523,
  'D5': 587,
  'E5': 659,
  'F5': 698,
  'G5': 784,
  'A5': 880,
  'B5': 988,
  'C6': 1047,
  'D6': 1175,
  'E6': 1319,
  'F6': 1397,
  'G6': 1568,
  'A6': 1760,
  'B6': 1976,
  'C#4': 277,
  'D#4': 311,
  'F#4': 370,
  'G#4': 415,
  'A#4': 466,
  'C#5': 554,
  'D#5': 622,
  'F#5': 740,
  'G#5': 831,
  'A#5': 932,
  'C#6': 1109,
  'D#6': 1245,
  'F#6': 1480,
  'G#6': 1661,
  'A#6': 1865,
}


class PlayType():
    """List of values for ``play_type`` in sound playback methods"""
    WAIT = 0
    """Play the sound once and wait until it is finished before returning"""
    ONCE = 1
    """Play the sound once in the background"""
    REPEAT = 2
    """Play the sound repeating in the background"""


class Sound():
    """Object for making sounds"""
    def __init__(self):
        self._pid = 0
        self._beep_dev = open(_BEEP_DEV, 'b+')
        self._tone_data = bytearray(sizeof(_input_event))
        self._tone_event = struct(addressof(self._tone_data), _input_event)
        self._timeout = Timeout(0, None)
        self._lock = _thread.allocate_lock()

    def _play_tone(self, frequency):
        self._tone_event.type = _EV_SND
        self._tone_event.code = _SND_TONE
        self._tone_event.value = int(frequency)
        self._beep_dev.write(self._tone_data)

    def play_tone(self, frequency, duration, volume, play_type):
        """Play a tone

        Parameters:
            frequency (int): The frequency of the tone in Hz
            duration (float): The duration of the tone in seconds
            volume (int): The playback volume in percent [0..100]
            play_type (PlayType): Controls how many times the sound is played
                and when the function returns
        """
        with self._lock:
            self._stop()
            self._timeout._interval = duration
            self._timeout._repeat = play_type == PlayType.REPEAT
            if self._timeout._repeat:
                self._timeout._func = lambda: self._play_tone(frequency)
            else:
                self._timeout._func = lambda: self._play_tone(0)
            self._play_tone(frequency)
            self._timeout.start()

        if play_type == PlayType.WAIT:
            self._timeout.wait()

    def play_note(self, note, duration, volume, play_type):
        """Play a musical note

        Parameters:
            note (int): The name of the note ['C4'..'B6'] (use # for sharp)
            duration (float): The duration of the note in seconds
            volume (int): The playback volume in percent [0..100]
            play_type (PlayType): Controls how many times the sound is played
                and when the function returns
        """
        frequency = _NOTES[note]
        self.play_tone(frequency, duration, volume, play_type)

    def play_file(self, file, volume, play_type):
        """Play a .WAV file

        Parameters:
            file (str): The file path
            volume (int): The playback volume in percent [0..100]
            play_type (PlayType): Controls how many times the sound is played
                and when the function returns
        """
        with self._lock:
            self._stop()
            self._pid = os.fork()
            if self._pid:
                if play_type == PlayType.WAIT:
                    os.waitpid(self._pid, 0)
            else:
                # terminate this process when parent dies
                _prctl(_PR_SET_PDEATHSIG, _SIGTERM)
                while True:
                    err = os.system('aplay --quiet {}'.format(file))
                    if err or play_type != PlayType.REPEAT:
                        break
                os._exit(0)

    def _stop(self):
        self._timeout.cancel()
        pid = self._pid
        if pid:
            self._pid = 0
            try:
                os.kill(pid, _SIGTERM)
            except:
                # we tried
                pass
        self._play_tone(0)

    def stop(self):
        """Stop any sound that is playing"""
        with self._lock:
            self._stop()
