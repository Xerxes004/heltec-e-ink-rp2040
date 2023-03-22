import time
from machine import Pin
from heltec_e_ink import connect_to_display, Displays, SerialInitInfo, IEPaperDisplay, EInkCanvas, Rotation

# Turn on LED
led_pin = Pin(25, mode=Pin.OUT, value=1)
time.sleep_ms(200)


print(f"Initializing display QYEG0213RWS800")
init_info: SerialInitInfo = SerialInitInfo(0, 19, 18, 20, 14, 15, 2_000_000)
print(init_info)

print("Connecting to display...")
display: IEPaperDisplay = connect_to_display(Displays.QYEG0213RWS800, init_info)
print("\bDONE")

print("Initializing display...")
display.initialize_display()
print("\bDONE")


print("Displaying test pattern...")

canvas = EInkCanvas(display)
canvas.clear()
display.draw_test_pattern(canvas)
canvas.flush_to_display()
display.refresh_display()

print("Program complete")
