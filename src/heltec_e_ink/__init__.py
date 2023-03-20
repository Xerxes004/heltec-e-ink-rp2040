from ._display_interface import IEPaperDisplay, PixelType
from ._serial_interface import SerialInitInfo


class Displays:
    QYEG0213RWS800 = 0


def connect_to_display(display_name: Displays, init_info: SerialInitInfo) -> IEPaperDisplay:
    """
    Get the display of the given type.
    :param display_name: The name of the display.
    :param init_info: Initialization info for display pin connections
    :return: The display NOT INITIALIZED.
    """
    if display_name is Displays.QYEG0213RWS800:
        from .displays.heltec_250_122_bwr_QYEG0213RWS800 import Display, SerialInterface
        iface = SerialInterface(init_info=init_info)
        display = Display(iface)
        return display

    raise Exception(f"Couldn't find {display_name}")

