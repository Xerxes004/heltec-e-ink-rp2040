# Contributing

Pull requests are welcome!

## Basic Requirements for Acceptance

These requirements are intended to mitigate the shortfalls of Python as a professional language. Duck typing is great 
for writing scripts, but not for working with low-level interfaces. Here there be monsters!

1. Follow the style used generally throughout the code
2. Use interrupts instead of polling
3. Use dependency-injection for interfaces; don't arbitrarily assign pins for users
4. Don't use global variables
5. Use type hints for all function parameters, return values, and variables

## Requirements for Adding Display Support

If you want to add support for a new screen, that's awesome! But please follow these guidelines to ensure that others
get maximum value from your contribution:

1. Follow the pattern used for other displays for instantiation, initialization, and interaction
3. Provide a markdown document in the `docs/` with the following (at minimum)
    * Name the document &lt;manufacturer&gt;\_&lt;width_height&gt;\_&lt;pixel type&gt;\_&lt;part number&gt;.md
      * For example: [`heltec_250_122_bwr_QYEG0213RWS800F13.md`](heltec_250_122_bwr_QYEG0213RWS800F13.md)
    * Follow the style of other display markdown docs
    * Include the manufacturer's part number
    * Include the display width and height in pixels
    * Include the display pixel information
    * Include a wiring diagram photograph (or equivalent)
4. Provide the manufacturer's data sheet with serial port information matching the manufacturer's part number in (2.)