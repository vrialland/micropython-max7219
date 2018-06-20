from machine import Pin
from micropython import const
import framebuf

DIGIT_0 = const(0x1)

DECODE_MODE = const(0x9)
NO_DECODE = const(0x0)

INTENSITY = const(0xa)
INTENSITY_MIN = const(0x0)

SCAN_LIMIT = const(0xb)
DISPLAY_ALL_DIGITS = const(0x7)

SHUTDOWN = const(0xc)
SHUTDOWN_MODE = const(0x0)
NORMAL_OPERATION = const(0x1)

DISPLAY_TEST = const(0xf)
DISPLAY_TEST_NORMAL_OPERATION = const(0x0)

MATRIX_SIZE = const(8)


class Max7219(framebuf.FrameBuffer):
    """
    Driver for MAX7219 8x8 LED matrices

    Example for ESP8266 with 2x4 matrices (one on top, one on bottom),
    so we have a 32x16 display area:

    >>> from machine import Pin, SPI
    >>> import max7219
    >>> spi = SPI(1, baudrate=10000000)
    >>> screen = Max7219(32, 16, spi, Pin(15))
    >>> screen.rect(0, 0, 32, 16, 1)  # Draws a frame
    >>> screen.text('Hi!', 4, 4, 1)
    >>> screen.show()
    """
    def __init__(self, width, height, spi, cs):
        # Pins setup
        self.spi = spi
        self.cs = cs
        self.cs.init(Pin.OUT, True)

        # Dimensions
        self.width = width
        self.height = height
        # Guess matrices disposition
        self.cols = width // MATRIX_SIZE
        self.rows = height // MATRIX_SIZE
        self.nb_matrices = self.cols * self.rows

        # 1 bit per pixel (on / off) -> 8 bytes per matrix
        self.buffer = bytearray(width * height // 8)
        super().__init__(self.buffer, width, height, framebuf.MONO_HLSB)

        # Init display
        self.init_display()

    def _write_command(self, command, data):
        """Write command on SPI"""
        cmd = bytearray([command, data])
        self.cs(0)
        for matrix in range(self.nb_matrices):
            self.spi.write(cmd)
        self.cs(1)

    def init_display(self):
        """Init hardware"""
        for command, data in (
                (SHUTDOWN, SHUTDOWN_MODE),  # Prevent flash during init
                (DECODE_MODE, NO_DECODE),
                (DISPLAY_TEST, DISPLAY_TEST_NORMAL_OPERATION),
                (INTENSITY, INTENSITY_MIN),
                (SCAN_LIMIT, DISPLAY_ALL_DIGITS),
                (SHUTDOWN, NORMAL_OPERATION),  # Let's go
        ):
            self._write_command(command, data)

        self.fill(0)
        self.show()

    def brightness(self, value):
        """Set display brightness (0 to 15)"""
        if not 0 <= value < 16:
            raise ValueError('Brightness must be between 0 and 15')
        self._write_command(INTENSITY, value)

    def show(self):
        """Update display"""
        # Write line per line on the matrices
        for line in range(8):
            self.cs(0)

            for matrix in range(self.nb_matrices):
                # Guess where the matrix is placed
                row, col = divmod(matrix, self.cols)
                # Compute where the data starts
                offset = row * 8 * self.cols
                index = col + line * self.cols + offset
                self.spi.write(bytearray([DIGIT_0 + line, self.buffer[index]]))

            self.cs(1)
