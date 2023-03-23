from math import sqrt
from ._display_interface import IEPaperDisplay, PixelType


class Rotation:
    ROTATE_0 = 0
    ROTATE_90 = 1
    ROTATE_180 = 2
    ROTATE_270 = 3


class EInkCanvas:
    def __init__(self, display: IEPaperDisplay, rotation: Rotation = Rotation.ROTATE_0):
        self._display = display
        self._rotation = rotation
        self._buffers = {}

        for pixel_type in display.supported_pixel_types:
            self._buffers[pixel_type] = bytearray([0x00] * self._display.width_bytes * self.height_px)

    def __del__(self):
        del self._buffers

    def __enter__(self):
        return self

    @property
    def width_px(self):
        return self._display.width_px

    @property
    def height_px(self):
        return self._display.height_px

    @property
    def resolution(self):
        return self.width_px * self.height_px

    @property
    def rotation(self):
        return self._rotation

    def draw_buffer(self, color: PixelType, buffer: bytearray):
        buf = self._buffers[color]
        if len(buffer) > len(buf):
            raise Exception(f"Can't draw buffer of size {len(buffer)} to one of size {len(buf)}")

        for i, v in enumerate(buffer):
            buf[i] = v

    def flush_to_display(self):
        for p in self._display.supported_pixel_types:
            self._display.set_pixels(p, bytearray(self._buffers[p]))

    def clear(self, color_types: [PixelType] = None):
        if color_types is None:
            color_types = self._display.supported_pixel_types

        for c in color_types:
            buf = self._buffers[c]
            for i in range(len(buf)):
                buf[i] = 0xFF if c is PixelType.BLACK_WHITE else 0x00

    def draw_pixel(self, x: int, y: int, color: PixelType):
        if self.rotation is Rotation.ROTATE_0:
            pass
        elif self.rotation is Rotation.ROTATE_90:
            (x, y) = (self.width_px - y, x)
        elif self.rotation is Rotation.ROTATE_180:
            (x, y) = (self.width_px - x, self.height_px - y)
        elif self.rotation is Rotation.ROTATE_270:
            (x, y) = (y, self.height_px - x)

        self._display.draw_pixel_absolute(self._buffers[color], x, y, color)

    def draw_line(self, p1: (int, int), p2: (int, int), color: PixelType):
        (x1, y1) = p1
        (x2, y2) = p2
        ld = round(sqrt((x2 - x1)**2 + (y2 - y1)**2))
        if ld is 0:
            return
        dx = (x2 - x1) / ld
        dy = (y2 - y1) / ld
        x = x1
        y = y1

        for p in range(round(ld) + 1):
            self.draw_pixel(round(x), round(y), color)
            x += dx
            y += dy
