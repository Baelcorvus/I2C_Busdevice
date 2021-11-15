# I2C_Busdevice
I2C_Busdevice is a stadard library for use in creating libraries for I2C devices, such as sensors or remote I/O.
This allows for simpler to understand code in the library, fatser creation of micropython library code and
standaised error checking.

To use the code you need to put the library in the default directory of the Pico, and then import it into your code:

```micropython
from machine import Pin, I2C
from I2C_bus_device import I2CDevice
```

You then need to create a bus by defining which pins the I2C bus is connect to.

```micropython
sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
i2c_bus = 0
addr = 0x09

i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)  #define the i2c bus
```

Here the bus is connected to Pin (0) for SDA and Pin (1) for SCL.
The I2C Bus is give by which pins you use. A pin out of you Pico should tell you which bus you use. SDA0 is bus 0, SDA1 us bus 1 for example.

We then define the device:
```micropython
device = I2CDevice(i2c, addr)
```

This will intialise an I2C bus device and check if it is present on the bus.
The address will be the addreess of the device on the bus.

You can create multiple devices with different addresses to talk to different devices, for example to talk to a SHTC3 temperature
and humidity sensor as well as a TSL2591 Light sensor we can create:

```micropython
sht_addr = 0x70
lux_addr = 0x29
sht = I2CDevice(i2c, sht_addr)
lux = I2CDevice(i2c, lux_addr)
```

This willl create two devicess, each talking to a diffecnt device on the I2C bus.

To write to a device we can use device.write(buf)
This will write the bytearray buf to the device.
So, for example, if we wish to send "hello" to the sht sensor we just created:

```micropython
data = "hello"
outbuf = bytearray(data)
sht.write(outbuf)
```

Reading is done in a similar manner using device.readinto(buf):

```micropython
inbuf = bytearray()
sht.readinto{inbuf}
print(inbuf)
```

In both these cases you can specify a start or an end value that slices the array for sending or receiving.
```micropython
data = "hello"
outbuf = bytearra(data)
sht.write(outbuf, start=1, end=3)
```
will send "ell" to the device.

Also included is a function that writes to a devices, waits a designated time and then reads the decice all in one go.
This is useful if the deevice requires a command to tell it which data to send.
To use this use `device.write_then_readinto(outbuf, inbuf, delay)`
This writes the output buffer to the device waits for delay(s) and then reads the input.

```micropython
cmd = "temp"
outbuf = bytearray(cmd)
inbuf = bytearray()
delay = 0.4
sht.write_then_readinto(outbuf, inbuf, delay)
```

This will write "temp" to the device, wait 0.4s and then read the device.
The function also has out_start, out_end an in_start and in_end arguments if you require slicing of the data.
The default delay time is 0s, so if no delay is required this can be omitted


A note on errors.
By default, when the device is intialised - `device = I2CDEVICE(i2c, addr)` - it will check if the device is present and responsive. If it does not find the device it will set an error.
To not check if the device is present use `probe=false` in the command. `device = I2CDevice(i2c, addr, probe=False)`

The error can be accessed as device.i2c_error. If this is -1 then the device cannot be found on the bus. The property device.i2c_error_device will contain the device address that cannot be found.

So we can use:
```micropython
sht = I2CDevice(i2c, addr)

if (sht.device.i2c_error == 0):
    #device is present and working so read and write
else:
    print(sht.device.i2c_error, sht.device.i2c_error_device)
    sht = I2CDevice(i2c, addr)
```

This will check if the device is connected and if not moans about at and tries again to intialise it. 

An error in the bus (for example a line dropping out) will result in a value of -2 in the device.i2c_error.