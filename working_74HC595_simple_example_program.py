# Christopher W Hafey, wa1tnr    14 March 2018  02:19 UTC
# LICENSE: MIT

import board
import busio
import digitalio
import time
from adafruit_bus_device import spi_device
from micropython import const
data   = board.D4
clk    = board.D3
latch  = digitalio.DigitalInOut(board.D2)
latch.switch_to_output(value =True, drive_mode=digitalio.DriveMode.PUSH_PULL)
spi = busio.SPI(clk, MOSI=data)

spi_device = spi_device.SPIDevice(spi, latch) # minimum parameters found in the REPL

def write_data_out(cmd):
    with spi_device as spi:
        spi.write(bytearray([cmd]))


# There are two chained 74HC595 shift registers.
# write two bytes at a time, for a 16-bit wide
# user interface to them.

def bytes_out():
    global cmd, mbytes
    for p in range(0,2):
        cmd = mbytes[p]
        write_data_out(cmd)



# blank the 7-segment display
def write_blank():
    global mbytes
    mbytes = bytearray(b'\x00\x00')
    bytes_out()



# write an 'A' on the 7-segment display

def write_char_A():
    global mbytes
    # i = 1 + 2 + 4 + 16 + 32 + 64;
    # 0111 0111
    mbytes = bytearray(b'\x00\x77')
    bytes_out()


# write a 'B' on the 7-segment display

def write_char_b():
    global mbytes
    # i = 4 + 8 + 16 + 32 + 64;
    # 0111 1100
    mbytes = bytearray(b'\x00\x7f')
    bytes_out()




# - - - -   The Program   - - - -
write_char_A()
time.sleep(2.0)
write_blank()
time.sleep(2.0)
write_char_b()
time.sleep(2.0)

"""

  // i =   1; ledval = i; outeye(); // segment A
  // i =   2; ledval = i; outeye(); // segment B
  // i =   4; ledval = i; outeye(); // segment C
  // i =   8; ledval = i; outeye(); // segment D
  // i =  16; ledval = i; outeye(); // segment E
  // i =  32; ledval = i; outeye(); // segment F
  // i =  64; ledval = i; outeye(); // segment G
  // i = 128; ledval = i; outeye(); // colon


  // 0 
  i = 1 + 2 + 4 + 8 + 16 + 32 +  0 +   0;
      ledval = i; outeye();

  // 1
  i = 0 + 2 + 4 + 0 +  0 +  0 +  0 +   0;
      ledval = i; outeye();

  // 2     // 1 2 8 16 64
  i = 1 + 2 + 0 + 8 + 16 +  0 + 64 +   0;
      ledval = i; outeye();

  // 3
  i = 1 + 2 + 4 + 8 +  0 +  0 + 64 +   0;
      ledval = i; outeye();

  // 4   //  2 4 32 64
  i = 0 + 2 + 4 + 0 +  0 + 32 + 64 +   0;
      ledval = i; outeye();

  // 5   // like 2
  i = 1 + 0 + 4 + 8 +  0 + 32 + 64 +   0;
      ledval = i; outeye();

  // 6
  i = 1 + 0 + 4 + 8 + 16 + 32 + 64 +   0;
      ledval = i; outeye();

  // 7
  i = 1 + 2 + 4 + 0 +  0 +  0 +  0 +   0;
      ledval = i; outeye();

  // 8
  i = 1 + 2 + 4 + 8 + 16 + 32 + 64 +   0;
      ledval = i; outeye();

  // 9
  i = 1 + 2 + 4 + 0 +  0 + 32 + 64 +   0;
      ledval = i; outeye();

  // A
  i = 1 + 2 + 4 + 16 + 32 + 64;
      ledval = i; outeye();

  // b
  i = 4 + 8 + 16 + 32 + 64;
      ledval = i; outeye();

  // C
  i = 1 + 8 + 16 + 32;
      ledval = i; outeye();

  // d
  i = 2 + 4 + 8 + 16 + 64;
      ledval = i; outeye();

  // E
  i = 1 + 8 + 16 + 32 + 64;
      ledval = i; outeye();

  // F
  i = 1 + 0 + 16 + 32 + 64;
      ledval = i; outeye();


  i = 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128;
  i = 0;

  i = 128; ledval = i; outeye(); blankleds(); delay(255);
  i = 128; ledval = i; outeye(); blankleds(); delay(255);

}
"""

