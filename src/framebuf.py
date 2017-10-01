"""Dummy module so we can build docs and use auto-completion using standard
python.
"""

MONO_VLSB, MONO_HLSB, MONO_HMSB, RGB565, GS4_HMSB = range(5)


class FrameBuffer():
    def __init__(self, buffer, width, height, format, stride=None):
        pass

    def fill(self, c):
        pass

    def pixel(self, x, y, c=None):
        pass

    def hline(self, x, y, w, c):
        pass

    def vline(self, x, y, h, c):
        pass

    def rect(self, x, y, w, h, c):
        pass

    def fill_rect(self, x, y, w, h, c):
        pass

    def text(self, s, x, y, c=None):
        pass

    def scroll(self, xstep, ystep):
        pass

    def blit(self, fbuf, x, y, key=None):
        pass
