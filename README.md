# AHT20 Temperature & Humidity for Python I2C

Standadone communication driver for the AHT20 Temperature & Humidity sensor, running on a Raspberry Pi on Python.

* [Board](https://www.adafruit.com/product/4566)
* [Datasheet](./AHT20-datasheet-2020-4-16.pdf)

## Pinout

The AHT20 sensor is connected to the Rasperry Pi via the following pins:

Pin # | Pin Name | Connection
:-:|:-:|:-:
1 | 3.3v | Voltage in
3 | GPIO2 | I2C SDA
5 | GPIO3 | I2C SDL
9 | GND | Ground

[The Raspberry Pi GPIO pinout map can be viewed here.](https://www.raspberrypi.org/documentation/usage/gpio/)

## Pre-requistes

* Raspberry Pi, but could run elsewhere
* On the machine: `python3-smbus` installed
* On Python: `smbus2` installed

## Notes

* The I2C bus is `1` by default, as it's the default one for the Raspberry Pi. Another bus can be specified with the `BusNum` variable when calling the module.

## Authors

* [Chouffy](https://github.com/Chouffy/) for the original module
* [Zifeng1997](https://github.com/xzf89718) for the CRC8 checker

## Sources

* [Adafruit original driver with CircuitPython](https://github.com/adafruit/Adafruit_CircuitPython_AHTx0)
