'''
A simple example to use the I2C Bus Device librart to read and write from a slave device.
Here the I2C bus is connected to the pico pins 0 and 1, which is bus 0.
The progranm reads the value of a button and sends the value to a slave device.
it also reads a value from the slave and sets a LED (connected here to pin 28) accordingly.
 
'''
from machine import Pin, I2C
from time import sleep
from I2C_bus_device import I2CDevice

sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
i2c_bus = 0
addr = 0x09

i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)  #define the i2c bus

device = I2CDevice(i2c, addr)        #create the I2C device

led = machine.Pin(28, Pin.OUT)       #LED connected to pin 28
led.low()

but2 = Pin(20, Pin.IN, Pin.PULL_UP)  #Button connected to pin 20

while True:
    if (device.i2c_error == 0):      #check the device error message. If device is present and the bus is working correctly this value will be 0
        bytes_read = bytearray(1)
        device.readinto(bytes_read)  #read one byte from the slave
        button = bytes_read [0]        
        if (button == 1):            #set the LED
            led.high()
        else:
            led.low()
        
        data1 = bytearray([but2.value()]) #aquire the state of the button and create a bytearray with this in it.
        device.write(data1)               #send the value of the button to the slave
        
    else:
        print("no device")                                    #if the error bit is set then the bus has failed. 
        print(device.i2c_error, device.i2c_error_device)      #print the error number and the device it waas trying to commincate with
        device = I2CDevice(i2c, addr)                         #reinitialise the device to check it again