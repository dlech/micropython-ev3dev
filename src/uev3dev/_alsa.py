
from struct import calcsize
from struct import unpack

import ffilib
from uctypes import addressof

from uev3dev.util import debug_print

_alsa = ffilib.open('libasound')
_strerror = _alsa.func('s', 'snd_strerror', 'i')


def _check_error(err):
    if not err:
        return
    raise AlsaError(_strerror(err))


class AlsaError(Exception):
    def __init__(self, message):
        super(AlsaError, self).__init__(message)


class Mixer():
    _open = _alsa.func('i', 'snd_mixer_open', 'pi')
    _close = _alsa.func('i', 'snd_mixer_close', 'p')
    _attach = _alsa.func('i', 'snd_mixer_attach', 'ps')
    _load = _alsa.func('i', 'snd_mixer_load', 'p')

    _selem_register = _alsa.func('i', 'snd_mixer_selem_register', 'ppp')
    _selem_register = _alsa.func('i', 'snd_mixer_selem_register', 'ppp')
    _selem_id_sizeof = _alsa.func('p', 'snd_mixer_selem_id_sizeof', '')
    _selem_id_set_index = _alsa.func('v', 'snd_mixer_selem_id_set_index', 'pI')
    _selem_id_set_name = _alsa.func('v', 'snd_mixer_selem_id_set_name', 'ps')
    _find_selem = _alsa.func('p', 'snd_mixer_find_selem', 'pP')
    _selem_get_playback_volume_range = \
        _alsa.func('i', 'snd_mixer_selem_get_playback_volume_range', 'ppp')
    _selem_set_playback_volume_all = \
        _alsa.func('i', 'snd_mixer_selem_set_playback_volume_all', 'pl')

    def __init__(self):
        self._mixer = bytearray(calcsize('P'))
        err = Mixer._open(self._mixer, 0)
        _check_error(err)
        self._mixer = unpack('P', self._mixer)[0]
        try:
            # use default sound card
            err = Mixer._attach(self._mixer, 'default')
            _check_error(err)
            err = Mixer._selem_register(self._mixer, 0, 0)
            _check_error(err)
            err = Mixer._load(self._mixer)
            _check_error(err)

            self._id_data = bytearray(Mixer._selem_id_sizeof())
            self._id = addressof(self._id_data)
            min = bytearray(calcsize('l'))
            max = bytearray(calcsize('l'))

            # get PCM volume control
            err = Mixer._selem_id_set_index(self._id, 0)
            _check_error(err)
            err = Mixer._selem_id_set_name(self._id, 'PCM')
            _check_error(err)
            self._pcm_elem = Mixer._find_selem(self._mixer, self._id)
            if not self._pcm_elem:
                raise AlsaError('Could not find "PCM" mixer element')
            Mixer._selem_get_playback_volume_range(self._pcm_elem,
                                                   addressof(min),
                                                   addressof(max))
            self._pcm_min = unpack('l', min)[0]
            self._pcm_max = unpack('l', max)[0]

            # get Beep volume control
            err = Mixer._selem_id_set_index(self._id, 0)
            _check_error(err)
            err = Mixer._selem_id_set_name(self._id, 'Beep')
            _check_error(err)
            self._beep_elem = Mixer._find_selem(self._mixer, self._id)
            if not self._beep_elem:
                raise AlsaError('Could not find "Beep" mixer element')
            Mixer._selem_get_playback_volume_range(self._beep_elem,
                                                   addressof(min),
                                                   addressof(max))
            self._beep_min = unpack('l', min)[0]
            self._beep_max = unpack('l', max)[0]
        except:
            Mixer._close(self._mixer)
            raise

    def close(self):
        self._beep_elem = None
        self._pcm_elem = None
        if self._mixer:
            Mixer._close(self._mixer)
            self._mixer = None

    def set_pcm_volume(self, volume):
        # scale the volume, assuming self._pcm_min is 0
        volume = volume * self._pcm_max // 100
        Mixer._selem_set_playback_volume_all(self._pcm_elem, volume)

    def set_beep_volume(self, volume):
        # scale the volume, assuming self._beep_min is 0
        volume = volume * self._beep_max // 100
        Mixer._selem_set_playback_volume_all(self._beep_elem, volume)
