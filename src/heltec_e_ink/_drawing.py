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
            self._buffers[pixel_type] = [0x00] * self._get_bytes_needed(self.width_px) * self.height_px

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
        if len(buffer) != len(buf):
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

    def _draw_pixel_absolute(self, x: int, y: int, color: PixelType):
        if x < 0 or x >= self.width_px or y < 0 or y >= self.height_px \
                or color not in self._display.supported_pixel_types:
            return

        self._buffers[color][y * self.width_px + x] |= 0x80 >> (x % 8)

    @staticmethod
    def _get_bytes_needed(num_px: int) -> int:
        """
        If width isn't divisible by 8, we have to pad one extra byte to hold the data.
        :param num_px:
        :return:
        """
        if num_px % 8 == 0:
            return int(num_px / 8)
        else:
            return int(num_px / 8) + 1
