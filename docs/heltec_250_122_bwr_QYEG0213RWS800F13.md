# Heltec 250x122 Black/White/Red E-Ink Display

From the manufacturer's website:

> Display some stuff on E-Ink display is a series of chemical changes. For E-Ink display, power only needed during 
> refresh time, pictures can keep shown in the display without any power for more than 180 days. The content displayed 
> is the same as written on paper. Very suitable for shelf labeling, ID tag.

## Wiring

_TODO_

## Software

The display is controlled via Serial Peripheral Interface (SPI), and must go through an initialization phase at startup
to be ready for use. There is no read capability from the peripheral module, so only MOSI/TX needs to be wired to the 
SDI pin. Afterwards, data can be written to the BW and Red LUTs in memory. Once these locations are written, the next
refresh will show the data.

Check out the [SPI interface documentation](data_sheets/QYEG0213RWS800F13_V1.2.pdf)
