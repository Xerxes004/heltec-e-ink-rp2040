from typing import Sequence, Optional
from abc import ABC, abstractmethod
from enum import Enum
from machine import SPI


class PixelType(Enum):
    BLACK = 0b0001
    WHITE = 0b0010
    RED = 0b0100
    YELLOW = 0b1000


class IEPaperDisplay(ABC):
    """
    Abstract interface for all electrophoretic displays
    """

    #
    # Display properties
    #

    @property
    @abstractmethod
    def supported_pixel_types(self) -> Sequence[PixelType]:
        pass

    @property
    @abstractmethod
    def display_ready(self) -> bool:
        """
        The display is ready for commands if True, otherwise it's busy
        """

    @property
    @abstractmethod
    def width_px(self) -> int:
        """
        The display width in pixels
        """

    @property
    @abstractmethod
    def height_px(self) -> int:
        """
        The display height in px
        """

    @property
    @abstractmethod
    def bits_per_pixel(self) -> int:
        """
        Number of bits per pixel
        """

    #
    # Display functions
    #

    @abstractmethod
    def initialize_display(self, display_serial_interface: SPI) -> None:
        """
        Initialize the display directly after applying power
        """

    @abstractmethod
    def set_pixels(self, pixel_flag: PixelType, img_bytes: bytearray, start_byte: Optional[int] = None) -> None:
        """
        Set the pixels in RAM without refreshing
        :param pixel_flag: Type of pixels being set, or'd together as flags (like BLACK|WHITE)
        :param img_bytes: Image byte array
        :param start_byte: Start location in memory to begin writing the data
        """

    @abstractmethod
    def refresh_display(self) -> None:
        """
        Display the current LUT buffers on the screen
        """

    @abstractmethod
    def power_on_reset(self) -> None:
        """
        Software reset of the display
        """

    @abstractmethod
    def enter_deep_sleep(self) -> None:
        """
        Enter deep sleep mode (usually when done updating the display)
        """
