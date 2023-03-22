from _drawing import EInkCanvas

class PixelType:
    BLACK_WHITE = 0
    RED = 1
    YELLOW = 2


# noinspection PyPropertyDefinition
class IEPaperDisplay:
    """
    Abstract interface for all electrophoretic displays
    """

    #
    # Display properties
    #

    @property
    def supported_pixel_types(self) -> [PixelType]:
        pass

    @property
    def display_ready(self) -> bool:
        """
        The display is ready for commands if True, otherwise it's busy
        """

    @property
    def width_px(self) -> int:
        """
        The display width in pixels
        """

    @property
    def height_px(self) -> int:
        """
        The display height in px
        """

    @property
    def bits_per_pixel(self) -> int:
        """
        Number of bits per pixel
        """

    #
    # Display functions
    #

    def initialize_display(self) -> None:
        """
        Initialize the display directly after applying power
        """

    def display_test_pattern(self, *args, **kwargs):
        """
        Display a test pattern on the screen to see if everything is working
        """

    def set_pixels(self, pixel_type: PixelType, img_bytes: bytearray, start_byte: int = None) -> None:
        """
        Set the pixels in RAM without refreshing
        :param pixel_type: Type of pixels being set
        :param img_bytes: Image byte array
        :param start_byte: Start location in memory to begin writing the data
        """

    def refresh_display(self) -> None:
        """
        Display the current LUT buffers on the screen
        """

    def power_on_reset(self) -> None:
        """
        Software reset of the display
        """

    def enter_deep_sleep(self) -> None:
        """
        Enter deep sleep mode (usually when done updating the display)
        """

    def exit_deep_sleep(self) -> None:
        """
        Exit deep sleep mode (usually when about to update the display)
        """
