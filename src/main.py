import time
from machine import Pin
from heltec_e_ink import connect_to_display, Displays, SerialInitInfo, IEPaperDisplay, EInkCanvas, PixelType

# Turn on LED
led_pin = Pin(25, mode=Pin.OUT, value=1)
time.sleep_ms(200)


print(f"Initializing display QYEG0213RWS800")
init_info: SerialInitInfo = SerialInitInfo(0, 19, 18, 20, 14, 15, 2_000_000)
print(init_info)

print("Connecting to display...")
display: IEPaperDisplay = connect_to_display(Displays.QYEG0213RWS800, init_info)
print("DONE")

print("Initializing display...")
display.initialize_display()
print("DONE")


print("Displaying test pattern...")

canvas = EInkCanvas(display)
canvas.clear()
# display.draw_test_pattern(canvas)
for x in range(8):
    for y in range(3):
        canvas.draw_pixel(x * 8, y, PixelType.BLACK_WHITE)
        canvas.draw_pixel(x * 8 + 7, y, PixelType.RED)
canvas.draw_line((4, 1), (4, 4), PixelType.BLACK_WHITE)
canvas.draw_line((10, 10), (25, 25), PixelType.BLACK_WHITE)
canvas.draw_line((10, 25), (25, 10), PixelType.BLACK_WHITE)
canvas.draw_buffer(PixelType.BLACK_WHITE, bytearray([0x00]))
canvas.draw_buffer(PixelType.RED, bytearray([0x00, 0xFF]))
canvas.flush_to_display()
display.refresh_display()

print("Program complete")
