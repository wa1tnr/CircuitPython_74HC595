# Christopher W Hafey, wa1tnr    14 March 2018  02:19 UTC
# LICENSE: MIT

# works for a single shift register.  Assumed to work
# with two of them cascaded (needs proving on hardware).

import board
import busio
import digitalio
import time
from adafruit_bus_device import spi_device
from micropython import const
data   = board.D4 # grey wire Pin 14 74HC595
clk    = board.D3 # yellow wire is Pin 11 74HC595
latch  = digitalio.DigitalInOut(board.D2) # pin 12 74HC595
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



#            Dg3  Dg2  Dg1  Dg0
# Notches:  0x02 0x04 0x08 0x10

  # 0001 1110
  #    1    e

# all notched out:  14 + 16 0x1e

# enable Dg0:  0x0e

#   0001 0110
# enable Dg1:  0x16

#   0001 1110
#   0001 1010
# enable Dg2:  0x1a


#   0001 1110
#   0001 1100
# enable Dg3:  0x1c

# write an 'A' on the 7-segment display

def write_char_A2():
    global mbytes
    # i = 1 + 2 + 4 + 16 + 32 + 64;
    # 0111 0111
    mbytes = bytearray(b'\x1c\x77')
    bytes_out()

"""

  // i =   1;  // segment A
  // i =   2;  // segment B
  // i =   4;  // segment C
  // i =   8;  // segment D
  // i =  16;  // segment E
  // i =  32;  // segment F
  // i =  64;  // segment G
  // i = 128;  // colon


  // 0 
  i = 1 + 2 + 4 + 8 + 16 + 32 +  0 +   0;

  // 1
  i = 0 + 2 + 4 + 0 +  0 +  0 +  0 +   0;

  // 2
  i = 1 + 2 + 0 + 8 + 16 +  0 + 64 +   0;

  // 3
  i = 1 + 2 + 4 + 8 +  0 +  0 + 64 +   0;

  // 4
  i = 0 + 2 + 4 + 0 +  0 + 32 + 64 +   0;

  // 5
  i = 1 + 0 + 4 + 8 +  0 + 32 + 64 +   0;

  // 6
  i = 1 + 0 + 4 + 8 + 16 + 32 + 64 +   0;

  // 7
  i = 1 + 2 + 4 + 0 +  0 +  0 +  0 +   0;

  // 8
  i = 1 + 2 + 4 + 8 + 16 + 32 + 64 +   0;

  // 9
  i = 1 + 2 + 4 + 0 +  0 + 32 + 64 +   0;

  // A
  i = 1 + 2 + 4 + 16 + 32 + 64;

  // b
  i = 4 + 8 + 16 + 32 + 64;

  // C
  i = 1 + 8 + 16 + 32;

  // d
  i = 2 + 4 + 8 + 16 + 64;

  // E
  i = 1 + 8 + 16 + 32 + 64;

  // F
  i = 1 + 0 + 16 + 32 + 64;


  i = 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128;

}
"""



# write a 'b' on the 7-segment display

def write_char_b():
    global mbytes
    # i = 4 + 8 + 16 + 32 + 64;
    # 0111 1100
    mbytes = bytearray(b'\x00\x7c')
    bytes_out()



# write a 'C' on the 7-segment display

def write_char_C():
    global mbytes
    # i = 1 + 8 + 16 + 32;
    # 0011 1001
    mbytes = bytearray(b'\x00\x39')
    bytes_out()


# write 'd'

def write_char_d():
    global mbytes
    # i = 2 + 4 + 8 + 16 + 64;
    # 0101 1110
    mbytes = bytearray(b'\x00\x5e')
    bytes_out()


# write 'E'

def write_char_E():
    global mbytes
    # i = 1 + 8 + 16 + 32 + 64;
    # 0111 1001
    mbytes = bytearray(b'\x00\x79')
    bytes_out()





# - - - -   The Program   - - - -
write_blank();   time.sleep(0.1)
write_char_A2();  time.sleep(2.0)

time.sleep(22.0);

write_blank();   time.sleep(2.0)
write_char_b();  time.sleep(2.0)

write_blank();   time.sleep(2.0)
write_char_C();  time.sleep(2.0)

write_blank();   time.sleep(2.0)
write_char_d();  time.sleep(2.0)

write_blank();   time.sleep(2.0)
write_char_E();  time.sleep(2.0)

time.sleep(9);   write_blank();


# END.
