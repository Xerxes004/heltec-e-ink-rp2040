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

    def flush(self):
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

    def draw_circle(self, c: (int, int), r: int, color: PixelType, filled: bool = False):
        if r <= 0:
            return
        (x, y) = c

        # Bresenham algorithm

        x_pos = -r
        y_pos = 0
        err = 2 - 2 * r

        while x_pos <= 0:
            self.draw_pixel(x - x_pos, y + y_pos, color)
            self.draw_pixel(x + x_pos, y + y_pos, color)
            self.draw_pixel(x + x_pos, y - y_pos, color)
            self.draw_pixel(x - x_pos, y - y_pos, color)

            if filled:
                s1 = (x + x_pos, y + y_pos)
                e1 = (s1[0] + (2 * (-x_pos) + 1), s1[1])
                s2 = (x + x_pos, y - y_pos)
                e2 = (s2[0] + (2 * (-x_pos) + 1), s2[1])
                self.draw_line(s1, e1, color)
                self.draw_line(s2, e2, color)

            e2 = err
            if e2 <= y_pos:
                y_pos += 1
                err += y_pos * 2 + 1
                if -x_pos == y_pos and e2 <= x_pos:
                    e2 = 0
            if e2 > x_pos:
                x_pos += 1
                err += x_pos * 2 + 1

    def draw_rectangle(self, top_left: (int, int), bottom_right: (int, int), color: PixelType, filled: bool = False):
        bottom_left = (top_left[0], bottom_right[1])
        top_right = (bottom_right[0], top_left[1])

        self.draw_line(bottom_left, bottom_right, color)
        self.draw_line(bottom_left, top_left, color)
        self.draw_line(top_left, top_right, color)
        self.draw_line(top_right, bottom_right, color)

        print(f"filled={filled}")
        if filled:
            s = top_left
            e = top_right
            print(f"1: s={s}  e={e}")
            yd = top_left[1] - bottom_left[1]
            print(f"tl: {top_left}")
            print(f"tr: {top_right}")
            print(f"bl: {bottom_left}")
            print(f"br: {bottom_right}")
            print(f"yd={yd}")
            for i in range(round(yd)):
                self.draw_line(s, e, color)
                s = (s[0], s[1] - 1)
                e = (e[0], e[1] - 1)
                print(f"s={s}  e={e}")
