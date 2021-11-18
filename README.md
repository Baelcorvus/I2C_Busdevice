# I2C_Busdevice
I2C bus device library in micropython fora pico microcontroller.
I2C_Busdevice is a stadard library for use in creating libraries for I2C devices, such as sensors or remote I/O.
This allows for simpler to understand code in the library, fatser creation of micropython library code and
standaised error checking.

To use the code you need to put the library in the default directory of the Pico, and then import it into your code:

```micropython
from machine import Pin, I2C
from I2C_bus_device import I2CDevice
```

You then need to create a bus by defining which pins the I2C bus is connect to.

```python
sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
i2c_bus = 0
addr = 0x09

i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)  #define the i2c bus
```

Here the bus is connected to Pin (0) for SDA and Pin (1) for SCL.
The I2C Bus is give by which pins you use. A pin out of you Pico should tell you which bus you use. SDA0 is bus 0, SDA1 us bus 1 for example.

We then define the device:
```python
device = I2CDevice(i2c, addr)
```

This will intialise an I2C bus device and check if it is present on the bus.
The address will be the addreess of the device on the bus.

You can create multiple devices with different addresses to talk to different devices, for example to talk to a SHTC3 temperature
and humidity sensor as well as a TSL2591 Light sensor we can create:

```python
sht_addr = 0x70
lux_addr = 0x29
sht = I2CDevice(i2c, sht_addr)
lux = I2CDevice(i2c, lux_addr)
```

This willl create two devicess, each talking to a diffecnt device on the I2C bus.

To write to a device we can use device.write(buf)6
This will write the bytearray buf to the device.
So, for example, if we wish to send "hello" to the sht sensor we just created:

```python
data = "hello"
outbuf = bytearray(data)
sht.write(outbuf)
```

Reading is done in a similar manner using device.readinto(buf):

```python
inbuf = bytearray()
sht.readinto(inbuf)
print(inbuf)
```

In both these cases you can specify a start or an end value that slices the array for sending or receiving.
```python
data = "hello"
outbuf = bytearra(data)
sht.write(outbuf, start=1, end=3)
```
will send "ell" to the device.

Also included is a function that writes to a device, waits a designated time and then reads the device all in one go.
This is useful if the device requires a command to tell it which data to send.
To use this use `device.write_then_readinto(outbuf, inbuf, delay)`
This writes the output buffer to the device waits for delay (s) and then reads the input.

```python
cmd = "temp"
outbuf = bytearray(cmd)
inbuf = bytearray()
delay = 0.4
sht.write_then_readinto(outbuf, inbuf, delay)
```

This will write "temp" to the device, wait 0.4s and then read the device.
The function also has out_start, out_end, in_start and in_end arguments if you require slicing of the data.
The default delay time is 0s, so if no delay is required this can be omitted


***A note on errors.***
By default, when the device is intialised - `device = I2CDEVICE(i2c, addr)` - it will check if the device is present and responsive. If it does not find the device it will trigger an exeption.
To check if an error has occured you can use Try: and Exexcept OSError:
For example:
```python
Try:
    tsl = TSL2591.TSL2591(i2c, lux_addr)
except OSError:
    ptint ("device not present")
```
 This will intialise a TSL2591 seonsor and report an error if it is not found.

 You can also use try: except: when your read a sensor:
 ```python
 try:
    bytes_read = bytearray(1)
    device.readinto(bytes_read)  #read one byte from the slave
    button = bytes_read [0]        
    if (button == 1):            #set the LED
        led.high()
    else:
        led.low()
    
    data1 = bytearray([but2.value()]) #aquire the state of the button and create a bytearray with this in it.
    device.write(data1)               #send the value of the button to the slave
except OSError:                  #If there is a bus error, retry the connection
    print("device I/O error - retrying")
    try:
        device = I2CDevice(i2c, addr)
    except OSError:
        pass    
```
This reads a value from the device, and if it receives an error retries the sensor.         