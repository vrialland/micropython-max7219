# micropython-max7219

> MicroPython driver for MAX7219 8x8 LED matrix

![CI status](https://github.com/vrialland/micropython-max7219/workflows/CI/badge.svg?branch=main)

# What is it?

This library provides support for the MAX7219 8x8 LED matrix on ESP8266 with MicroPython.
It uses [`framebuf`](https://docs.micropython.org/en/latest/esp8266/library/framebuf.html) internally to provide drawing primitives and text support.
You can chain several matrices the way you like: if you use two 4x 8x8 matrices, you can have
one of the left, and the other on the right giving you a 64x8 area, or have one on top of the other to have a 32x16 display!

Tested on ESP8266 and ESP32 systems.

# Connecting on ESP8266

| ESP8266                    | MAX7219 |
| -------------------------- | ------- |
| 5V                         | VCC     |
| GND                        | GND     |
| GPIO13 (HWSPI #1 MOSI)     | DIN     |
| GPIO14 (HWSPI #1 SCK)      | CLK     |
| GPIO15                     | CS      |

# Connecting on ESP32

| ESP32                      | MAX7219 |
| -------------------------- | ------- |
| 5V                         | VCC     |
| GND                        | GND     |
| GPIO13 (HWSPI #1 MOSI)     | DIN     |
| GPIO14 (HWSPI #1 SCK)      | CLK     |
| GPIO15                     | CS      |

# Examples

Using `10000000` as `baudrate` is recommended as greater values don't seem to work well...

## Single 8x8 matrix (8x8 pixels)

```python

from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = max7219.Max7219(8, 8, spi, Pin(15))
screen.text('A', 0, 0, 1)
screen.show()
```

## Single 4x 8x8 matrix (32x8 pixels)

```python

from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = max7219.Max7219(32, 8, spi, Pin(15))
screen.text('ABCD', 0, 0, 1)
screen.show()
```

## Two 4x 8x8 matrices (left/right, 64x8 pixels)

```python

from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = max7219.Max7219(64, 8, spi, Pin(15))
screen.text('ABCDEFGH', 0, 0, 1)
screen.show()
```

## Two 4x 8x8 matrices (top/bottom, 32x16 pixels)

```python

from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = max7219.Max7219(32, 16, spi, Pin(15))
screen.text('ABCD', 0, 0, 1)
screen.text('EFGH', 0, 8, 1)
screen.show()
```

# Credits

This library is based on:

- [Official Micropython SSD1306 driver](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py)
- [micropython-max7219](https://github.com/mcauser/micropython-max7219) by [mcauser](https://github.com/mcauser)
- [Redgick GFX](https://github.com/redgick/Redgick_GFX/tree/master/Redgick_MatrixMAX72XX) by [jlebunetel](https://github.com/jlebunetel)

Thank you for the inspiration!
