"""Screen"""

from fcntl import ioctl

# FIXME: These micropython modules don't have python equivalents, so building
# docs fails
import framebuf
import uctypes

FBIOGET_VSCREENINFO = 0x4600
FBIOGET_FSCREENINFO = 0x4602

FB_VISUAL_MONO01 = 0
FB_VISUAL_MONO10 = 1

FIX_SCREEN_INFO = {
    'id_name': (uctypes.ARRAY | 0, uctypes.UINT8 | 16),
    'smem_start': uctypes.UINT32 | 16,  # long
    'smem_len': uctypes.UINT32 | 20,
    'type': uctypes.UINT32 | 24,
    'type_aux': uctypes.UINT32 | 28,
    'visual': uctypes.UINT32 | 32,
    'xpanstep': uctypes.UINT16 | 36,
    'ypanstep': uctypes.UINT16 | 38,
    'ywrapstep': uctypes.UINT16 | 40,
    'line_length': uctypes.UINT32 | 44,
    'mmio_start': uctypes.UINT32 | 48,  # long
    'mmio_len': uctypes.UINT32 | 52,
    'accel': uctypes.UINT32 | 56,
    'reserved': (uctypes.ARRAY | 60, uctypes.UINT16 | 3),
}

VAR_SCREEN_INFO = {
    'xres': uctypes.UINT32 | 0,
    'yres': uctypes.UINT32 | 4,
    'xres_virtual': uctypes.UINT32 | 8,
    'yres_virtual': uctypes.UINT32 | 12,
    'xoffset': uctypes.UINT32 | 16,
    'yoffset': uctypes.UINT32 | 20,
    'bits_per_pixel': uctypes.UINT32 | 24,
    'grayscale': uctypes.UINT32 | 28,
    'red': (32, {
        'offset': uctypes.UINT32 | 0,
        'length': uctypes.UINT32 | 4,
        'msb_right': uctypes.UINT32 | 8,
    }),
    'green': (44, {
        'offset': uctypes.UINT32 | 0,
        'length': uctypes.UINT32 | 4,
        'msb_right': uctypes.UINT32 | 8,
    }),
    'blue': (56, {
        'offset': uctypes.UINT32 | 0,
        'length': uctypes.UINT32 | 4,
        'msb_right': uctypes.UINT32 | 8,
    }),
    'transp': (68, {
        'offset': uctypes.UINT32 | 0,
        'length': uctypes.UINT32 | 4,
        'msb_right': uctypes.UINT32 | 8,
    }),
}


class Display():
    """Object that represents a display"""

    def __init__(self):
        self._fbdev = open('/dev/fb0', 'w+')
        self._fix_info_data = bytearray(66)
        fd = self._fbdev.fileno()
        ioctl(fd, FBIOGET_FSCREENINFO, self._fix_info_data, mut=True)
        self._fix_info = uctypes.struct(uctypes.addressof(self._fix_info_data),
                                        FIX_SCREEN_INFO)
        self._var_info_data = bytearray(80)
        ioctl(fd, FBIOGET_VSCREENINFO, self._var_info_data, mut=True)
        self._var_info = uctypes.struct(uctypes.addressof(self._var_info_data),
                                        VAR_SCREEN_INFO)
        self._fb_data = {}

    @property
    def width(self):
        """Gets the width of the display in pixels"""
        return self._var_info.xres_virtual

    @property
    def height(self):
        """Gets the height of the display in pixels"""
        return self._var_info.yres_virtual

    @property
    def bpp(self):
        """Gets the color depth of the screen in bits per pixel"""
        return self._var_info.bits_per_pixel

    def update(self, data):
        """Updates the display with the framebuffer data.

        Must be data returned by self.framebuffer().
        """
        self._fbdev.seek(0)
        self._fbdev.write(data)

    def framebuffer(self):
        """Creates a new framebuffer for the display

        returns a framebuf.FrameBuffer object used for drawing and a bytearray
        object to be passed to self.update()
        """
        data = bytearray(self._fix_info.line_length * self.height)
        if self._fix_info.visual in (FB_VISUAL_MONO01, FB_VISUAL_MONO10):
            format = framebuf.MONO_HMSB
        fbuf = framebuf.FrameBuffer(data, self.width, self.height, format,
                                    self._fix_info.line_length // self.bpp * 8)
        return fbuf, data
