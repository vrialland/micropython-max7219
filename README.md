# micropython-max7219

> MicroPython driver for MAX7219 8x8 LED matrix

[![Build Status](https://travis-ci.org/vrialland/micropython-max7219.svg?branch=master)](https://travis-ci.org/vrialland/micropython-max7219)

# What is it?

This library provides support for the MAX7219 8x8 LED matrix on ESP8266 with MicroPython.
It uses `[framebuf](https://docs.micropython.org/en/latest/esp8266/library/framebuf.html)` internally to provide drawing primitives and text support.
You can chain several matrices the way you like: if you use two 4x 8x8 matrices, you can have 
one of the left, and the other on the right giving you a 64x8 area, or have one on top of the other to have a 32x16 display!

The library has only been tested on an ESP8266 (yet!) but may work on other systems.

# Connecting on ESP8266

ESP8266     | MAX7219
----------- | --------
5V          | VCC
GND         | GND
D7 (GPIO13) | DIN
D8 (GPIO15) | CS
D5 (GPIO14) | CLK

# Examples

Using `10000000` as `baudrate` is recommended as greater values don't seem to work well...

## Single 8x8 matrix

```python

from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = Max7219(8, 8, spi, Pin(15))
screen.text('A', 0, 0, 1)
screen.show()
```

## Single 4x 8x8 matrix

```python

from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = Max7219(32, 8, spi, Pin(15))
screen.text('ABCD', 0, 0, 1)
screen.show()
```

## Two 4x 8x8 matrices (left/right)

```python

from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = Max7219(64, 8, spi, Pin(15))
screen.text('ABCDEFGH', 0, 0, 1)
screen.show()
```

## Two 4x 8x8 matrices (top/bottom)

```python

from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = Max7219(32, 16, spi, Pin(15))
screen.text('ABCD', 0, 0, 1)
screen.text('EFGH', 0, 8, 1)
screen.show()
```

# Credits
This library is based on:
- [Official Micropython SSD1306 driver](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py)
- [micropython-max7219](https://github.com/mcauser/micropython-max7219) by [mcauser](https://github.com/mcauser)
- [Redgick GFX](https://github.com/redgick/Redgick_GFX/tree/master/Redgick_MatrixMAX72XX) by [jlebunetel](https://github.com/jlebunetel)

Thank you for the inspiration!