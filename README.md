# RP2040 micropython for Heltec e-ink displays

This is a pico+micropython library for working with the Heltec e-paper displays mounted to their e-paper module. It 
provides basic functionality for updating the color LUTs, refreshing the display, and querying the pins.

Supported displays:

* [X] 2.13" with 250x122 BWR pixels (QYEG0213RWS800F13)

## Background

I wanted to port the C/CPP code into micropython as a personal challenge, and for another project I'm working on.

I got my first screen (QYEG0213RWS800F13) on Amazon from a company called JESSINIE. It was advertised as a 212x104 
resolution display, but I got the 250x122 one instead. I think the 212x104 version is discontinued by Heltec.

## Roadmap

* [X] Port HeltecAutomation code directly from C/CPP to Python, changing almost nothing
* [ ] Refactor to simplify interfaces & use interrupts instead of polling
* [ ] Add more screens

## Contributing

Please feel free to make pull requests for new screen support and bug fixes!

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for requirements.

## Disclaimer

The name "Heltec" is copyright to its owner; no relationship with the owner and this repository is expressed or implied.
I have no affiliation with this company in any way. Please reach out to them with any questions about their products.
