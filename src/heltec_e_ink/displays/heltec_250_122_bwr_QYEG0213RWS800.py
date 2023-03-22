from micropython import const
from machine import SPI

from .._drawing import EInkCanvas

import time

from .. import PixelType
from heltec_e_ink._serial_interface import ISerialDisplayInterface, SerialInitInfo
from heltec_e_ink._display_interface import IEPaperDisplay


class SerialInterface(ISerialDisplayInterface):
    def __init__(self, init_info: SerialInitInfo):
        super().__init__(init_info)

    def write_buffer(self, buffer: bytearray) -> int:
        buffer_len = len(buffer)
        if buffer_len == 0:
            return 0

        spi = self._spi

        command_byte = buffer[0:1]
        self.select_chip = True
        self.command_mode = True
        spi.write(command_byte)

        self.data_mode = buffer_len > 1
        data = buffer[1:]

        for i, b in enumerate(data):
            self.select_chip = True
            spi.write(bytearray([b]))

        self.select_chip = False

        return buffer_len


class Cmd:
    DRIVER_OUTPUT_CTRL = const(0x01)
    DEEP_SLEEP = const(0x10)
    DATA_ENTRY_MODE = const(0x11)
    SOFT_RESET = const(0x12)
    TEMPERATURE_SENSOR = const(0x18)
    MASTER_ACTIVATION = const(0x20)
    DISPLAY_UPDATE_CONTROL_1 = const(0x21)
    DISPLAY_UPDATE_CONTROL_2 = const(0x22)
    WRITE_BW_RAM = const(0x24)
    WRITE_R_RAM = const(0x26)
    BORDER_WAVEFORM = const(0x3C)
    RAM_X_START = const(0x44)
    RAM_Y_START = const(0x45)
    RAM_X_COUNTER = const(0x4E)
    RAM_Y_COUNTER = const(0x4F)
    ANALOG_BLOCK_CTRL = const(0x74)
    DIGITAL_BLOCK_CTRL = const(0x7E)


class Display(IEPaperDisplay):
    def __init__(self, display_iface: ISerialDisplayInterface):
        self._display_iface: ISerialDisplayInterface = display_iface
        self._initialized = False
        self._pixel_type_cmd = {
            PixelType.BLACK_WHITE: Cmd.WRITE_BW_RAM,
            PixelType.RED: Cmd.WRITE_R_RAM
        }

        if set(self.supported_pixel_types) != set(self._pixel_type_cmd.keys()):
            raise Exception("Supported pixel types don't have supporting commands")

    @property
    def supported_pixel_types(self) -> [PixelType]:
        return [PixelType.BLACK_WHITE, PixelType.RED]

    @property
    def width_px(self) -> int:
        return 122

    @property
    def height_px(self) -> int:
        return 250

    @property
    def display_ready(self) -> bool:
        return not self._display_iface.is_busy

    @property
    def bits_per_pixel(self) -> int:
        return 1

    def initialize_display(self) -> None:
        if self._initialized:
            return

        try:
            self._initialized = True

            # Wait for the screen to initialize its state machine
            time.sleep_ms(100)
            self.power_on_reset()

            # TODO: Can't figure out what this does, it's not in the command sheet
            # set analog block control
            self.write(Cmd.ANALOG_BLOCK_CTRL, [0x54])
            # set digital block control
            self.write(Cmd.DIGITAL_BLOCK_CTRL, [0x3B])

            # driver output control
            self.write(Cmd.DRIVER_OUTPUT_CTRL, [0xF9, 0x00, 0x00])

            # data entry mode
            self.write(Cmd.DATA_ENTRY_MODE, [0x01])

            # set RAM X address start/end position
            self.write(Cmd.RAM_X_START, [0x01, 0x10])

            # set RAM Y address start/end position
            self.write(Cmd.RAM_Y_START, [0xF9, 0x00, 0x00, 0x00])

            # border waveform
            self.write(Cmd.BORDER_WAVEFORM, [0x01])

            # temperature sensor selection (internal)
            self.write(Cmd.TEMPERATURE_SENSOR, [0x80])

            # set RAM X address count to 0
            # TODO: Decipher what this next comment means; it was copied from Heltec code
            # 0x0F --> (15+1)*8 = 128
            self.write(Cmd.RAM_X_COUNTER, [0x01])

            # TODO: Decipher what this next comment means; it was copied from Heltec code
            # set RAM Y address count to 0xF9 -->(249+1)=250
            self.write(Cmd.RAM_Y_COUNTER, [0xF9, 0x00])

            self.wait_until_ready()

            self._initialized = True

        except Exception as e:
            self._initialized = False
            raise e

    def power_on_reset(self):
        self.wait_until_ready()
        # self.exit_deep_sleep()
        self.write(Cmd.SOFT_RESET)
        self.wait_until_ready()

    def enter_deep_sleep(self) -> None:
        self.write(Cmd.DEEP_SLEEP, [0x01])

    def exit_deep_sleep(self) -> None:
        self.write(Cmd.DEEP_SLEEP, [0x00])

    def refresh_display(self) -> None:
        self.write(Cmd.DISPLAY_UPDATE_CONTROL_2, [0xF7])
        self.write(Cmd.MASTER_ACTIVATION)

    def set_pixels(self, pixel_flags: PixelType, img_bytes: bytearray, start_byte: int = None) -> None:
        if pixel_flags not in self.supported_pixel_types:
            raise Exception(f"Unsupported pixel type {pixel_flags}")

        if start_byte is None:
            start_byte = 0

        pixel_cmd = self._pixel_type_cmd[pixel_flags]
        self.write(pixel_cmd, img_bytes)

    def draw_test_pattern(self, canvas: EInkCanvas) -> {PixelType: bytearray}:
        rows_b = self.width_px + 1
        cols_b = self.height_px
        resolution = int(rows_b * cols_b / 8)
        bw_buffer = bytearray([0x00] * 4000)
        r_buffer = bytearray([0x0F] * 4000)

        for r in range(250):
            for c in range(16):
                offset = r * 16 + c
                # print(offset)
                if (c == 0 or c % 2 == 0) or (r == 0 or r % 16 < 4):
                    bw_buffer[offset] = 0xFF
                else:
                    bw_buffer[offset] = 0x00
        #
        #
        # for i in range(0, l):
        #     bw_buffer[i] = 0xFF

        # for i in range(400, 800):
        #     bw_buffer[i] = 0xFF >> 2

        #
        # black = 0
        # white = 1
        # red = 2
        # square_color = black
        # square_len_bytes = 3
        #
        # def set_pixels(buffer, row_start, row_end, col_start, col_end, val):
        #     row_end = min(row_end, rows_b)
        #     col_end = min(col_end, cols_b)
        #     for r in range(row_start, row_end):
        #         for c in range(col_start, col_end):
        #             buffer[r * cols_b + c] = val
        #
        # # The test pattern is 3-byte squares
        # for col in range(10):
        #     for row in range(5):
        #         if square_color is black:
        #             set_pixels(bw_buffer, row, row + square_len_bytes, col, col + square_len_bytes, 0x00)
        #             set_pixels(r_buffer, row, row + square_len_bytes, col, col + square_len_bytes, 0x00)
        #         if square_color is white:
        #             set_pixels(bw_buffer, row, row + square_len_bytes, col, col + square_len_bytes, 0xFF)
        #             set_pixels(r_buffer, row, row + square_len_bytes, col, col + square_len_bytes, 0x00)
        #         if square_color is red:
        #             set_pixels(r_buffer, row, row + square_len_bytes, col, col + square_len_bytes, 0xFF)
        #     if square_color is black:
        #         square_color = white
        #     if square_color is white:
        #         square_color = red
        #     if square_color is red:
        #         square_color = black

        canvas.draw_buffer(PixelType.BLACK_WHITE, bw_buffer)
        canvas.draw_buffer(PixelType.RED, r_buffer)

    def write(self, command: int, data: [int] = None) -> int:
        if data is None:
            data = []
        return self._display_iface.write_buffer(bytearray([command]) + bytearray(data))

    def wait_until_ready(self):
        while self._display_iface.is_busy:
            # 60Hz poll
            time.sleep_ms(100)
