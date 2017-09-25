"""Screen"""

from fcntl import ioctl

import framebuf
import uctypes

FBIOGET_VSCREENINFO = 0x4600
FBIOGET_FSCREENINFO = 0x4602

FB_VISUAL_MONO01 = 0
FB_VISUAL_MONO10 = 1

fb_fix_screeninfo = {
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
    'capabilities': uctypes.UINT16 | 60,
    'reserved0': uctypes.UINT16 | 62,
    'reserved1': uctypes.UINT16 | 64,
}

fb_bitfield = {
    'offset': uctypes.UINT32 | 0,
    'length': uctypes.UINT32 | 4,
    'msb_right': uctypes.UINT32 | 8,
}

fb_var_screeninfo = {
    'xres': uctypes.UINT32 | 0,
    'yres': uctypes.UINT32 | 4,
    'xres_virtual': uctypes.UINT32 | 8,
    'yres_virtual': uctypes.UINT32 | 12,
    'xoffset': uctypes.UINT32 | 16,
    'yoffset': uctypes.UINT32 | 20,
    'bits_per_pixel': uctypes.UINT32 | 24,
    'grayscale': uctypes.UINT32 | 28,
    'red': (32, fb_bitfield),
    'green': (44, fb_bitfield),
    'blue': (56, fb_bitfield),
    'transp': (68, fb_bitfield),
    'nonstd': uctypes.UINT32 | 80,
    'activate': uctypes.UINT32 | 84,
    'height': uctypes.UINT32 | 88,
    'width': uctypes.UINT32 | 92,
    'accel_flags': uctypes.UINT32 | 96,
    'pixclock': uctypes.UINT32 | 100,
    'left_margin': uctypes.UINT32 | 104,
    'right_margin': uctypes.UINT32 | 108,
    'upper_margin': uctypes.UINT32 | 112,
    'lower_margin': uctypes.UINT32 | 116,
    'hsync_len': uctypes.UINT32 | 120,
    'vsync_len': uctypes.UINT32 | 124,
    'sync': uctypes.UINT32 | 128,
    'vmode': uctypes.UINT32 | 132,
    'rotate': uctypes.UINT32 | 136,
    'colorspace': uctypes.UINT32 | 140,
    'reserved0': uctypes.UINT32 | 144,
    'reserved1': uctypes.UINT32 | 148,
    'reserved2': uctypes.UINT32 | 152,
    'reserved3': uctypes.UINT32 | 156,
}


class _Screen():
    """Object that represents a screen"""

    BLACK = 0
    WHITE = 1

    def __init__(self):
        self._fbdev = open('/dev/fb0', 'w+')
        self._fix_info_data = bytearray(uctypes.sizeof(fb_fix_screeninfo))
        fd = self._fbdev.fileno()
        ioctl(fd, FBIOGET_FSCREENINFO, self._fix_info_data, mut=True)
        self._fix_info = uctypes.struct(uctypes.addressof(self._fix_info_data),
                                        fb_fix_screeninfo)
        self._var_info_data = bytearray(uctypes.sizeof(fb_var_screeninfo))
        ioctl(fd, FBIOGET_VSCREENINFO, self._var_info_data, mut=True)
        self._var_info = uctypes.struct(uctypes.addressof(self._var_info_data),
                                        fb_var_screeninfo)
        self._fb_data = {}

    @property
    def width(self):
        """Gets the width of the screen in pixels"""
        return self._var_info.xres_virtual

    @property
    def height(self):
        """Gets the height of the screen in pixels"""
        return self._var_info.yres_virtual

    @property
    def bpp(self):
        """Gets the color depth of the screen in bits per pixel"""
        return self._var_info.bits_per_pixel

    def update(self, data):
        """Updates the screen with the framebuffer data.

        Must be data returned by self.framebuffer().
        """
        self._fbdev.seek(0)
        self._fbdev.write(data)

    def framebuffer(self):
        """Creates a new framebuffer for the screen

        returns a framebuf.FrameBuffer object used for drawing and a bytearray
        object to be passed to self.update()
        """
        data = bytearray(self._fix_info.line_length * self.height)
        if self._fix_info.visual in (FB_VISUAL_MONO01, FB_VISUAL_MONO10):
            format = framebuf.MONO_HMSB
        fbuf = framebuf.FrameBuffer(data, self.width, self.height, format,
                                    self._fix_info.line_length // self.bpp * 8)
        return fbuf, data


class Display():
    def __init__(self):
        self._screen = _Screen()
        self._fb, self._data = self._screen.framebuffer()

    def text_pixels(self, text, clear, x, y, color, font):
        if clear:
            self._fb.fill(_Screen.WHITE)
        if color:
            color = _Screen.WHITE
        else:
            color = _Screen.BLACK
        # TODO: micropython framebuf only has one font
        self._fb.text(str(text), x, y, color)
        self._screen.update(self._data)
