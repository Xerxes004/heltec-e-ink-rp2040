from micropython import const

from machine import Pin, SPI


class SerialInitInfo:
    def __init__(self, spi_id: int, tx_pin: int, sck_pin: int, cs_pin: int, data_command_pin: int, busy_pin: int,
                 baud_hz: int):
        self.spi_id: const(int) = const(spi_id)
        self.tx_pin: const(int) = const(tx_pin)
        self.sck_pin: const(int) = const(sck_pin)
        self.cs_pin: const(int) = const(cs_pin)
        self.data_command_pin: const(int) = const(data_command_pin)
        self.busy_pin: const(int) = const(busy_pin)
        self.baud_hz: const(int) = const(baud_hz)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
            f"Serial Info: spi={self.spi_id} baud={self.baud_hz}Hz tx={self.tx_pin} sck={self.sck_pin} " +
            f"cs={self.cs_pin} dc={self.data_command_pin} busy={self.busy_pin}")


class ISerialDisplayInterface:
    #
    # Properties
    #

    @property
    def select_chip(self) -> bool:
        """
        Whether the chip is selected
        """
        return self._cs_pin.value() == 0

    @select_chip.setter
    def select_chip(self, select: bool):
        self._cs_pin.value(0 if select else 1)

    @property
    def data_mode(self) -> bool:
        """
        True for data, False for command
        """
        return self._data_command_pin.value() == 1

    @data_mode.setter
    def data_mode(self, is_data: bool):
        """
        :param is_data: True to set data mode, False for command mode
        """
        self._data_command_pin.value(1 if is_data else 0)

    @property
    def command_mode(self) -> bool:
        """
        True for command, False for data
        """
        return not self.data_mode

    @command_mode.setter
    def command_mode(self, is_command: bool):
        """
        :param is_command: True to set command mode, False for data mode
        """
        self.data_mode = not is_command

    @property
    def is_busy(self) -> bool:
        """
        Whether the interface is busy
        """
        return self._busy_pin.value() == 1

    #
    # Methods
    #

    def __init__(self, init_info: SerialInitInfo):
        """
        Initialize the interface (write only)
        """

        spi_id = init_info.spi_id
        tx_pin = init_info.tx_pin
        sck_pin = init_info.sck_pin
        cs_pin = init_info.cs_pin
        data_command_pin = init_info.data_command_pin
        busy_pin = init_info.busy_pin
        baud_hz = init_info.baud_hz

        if spi_id not in [0, 1]:
            raise Exception(f"Valid SPI id's are 0 or 1 (got {spi_id})")

        invalid_spi0_cs_pins = [1, 5, 17]
        invalid_spi1_cs_pins = [9, 13]
        invalid_pin_map = {0: invalid_spi0_cs_pins,
                           1: invalid_spi1_cs_pins}

        err_msg = \
            f"""
            Due to the PL022 SPI implementation, these default SPI CSn pins cannot be used to automatically select the
            display. For SPI 0, you cannot use {invalid_spi0_cs_pins}. For SPI 1, you cannot use 
            {invalid_spi1_cs_pins}.\n
            See: https://github.com/raspberrypi/pico-sdk/issues/88#issuecomment-774113818
            """

        if cs_pin in invalid_pin_map[spi_id]:
            raise Exception(f"In SPI {spi_id} mode, pins {invalid_pin_map[spi_id]} cannot be used as CS.\n" + err_msg)

        self._tx_pin = Pin(tx_pin, mode=Pin.OUT)
        self._sck_pin = Pin(sck_pin, mode=Pin.OUT)
        self._cs_pin = Pin(cs_pin, mode=Pin.OUT, value=1)
        self._data_command_pin = Pin(data_command_pin, mode=Pin.OUT, value=0)
        self._busy_pin = Pin(busy_pin, mode=Pin.IN)
        self._spi = SPI(spi_id, baud_hz, firstbit=SPI.MSB, polarity=0, phase=0, sck=self._sck_pin, mosi=self._tx_pin)

    @classmethod
    def write_buffer(cls, buffer: bytearray) -> int:
        """
        Write the buffer to the SPI interface.
        :param buffer: Buffer to write
        :return: Number of bytes written
        """
