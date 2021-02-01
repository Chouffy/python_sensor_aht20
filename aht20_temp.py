from smbus2 import SMBus
import time
 
# Functions
def get_normalized_bit(value, bit_index):
    return (value >> bit_index) & 1

AHT20_I2CADDR = 0x38
AHT20_CMD_SOFTRESET = 0xBA
AHT20_CMD_INITIALIZE = [0xBE, 0x08, 0x00]
AHT20_CMD_MEASURE = [0xAC, 0x33, 0x00]
AHT20_STATUSBIT_BUSY = 7                    # The 7th bit is the Busy indication bit. 1 = Busy, 0 = not.
AHT20_STATUSBIT_CALIBRATED = 3              # The 3rd bit is the CAL (calibration) Enable bit. 1 = Calibrated, 0 = not

# I2C commands
# bus.read_i2c_block_data(i2c_address, register, lenght)
# bus.write_i2c_block_data(i2c_addr, register, data)

# Setup

i2c_bus = SMBus(1)  # Create a new I2C bus

# Soft reset: send 0xBA
i2c_bus.write_i2c_block_data(AHT20_I2CADDR, 0x0, [AHT20_CMD_SOFTRESET])
time.sleep(0.04)    ## Wait 40 ms

## If calibrated bit is NOT 1, send Initialization command and wait 10 ms until the calibrated bit is 1
if not get_normalized_bit(i2c_bus.read_i2c_block_data(AHT20_I2CADDR, 0x0, 1)[0], AHT20_STATUSBIT_CALIBRATED) == 1:
    i2c_bus.write_i2c_block_data(AHT20_I2CADDR, 0x0 , AHT20_CMD_INITIALIZE)
    while not get_normalized_bit(i2c_bus.read_i2c_block_data(AHT20_I2CADDR, 0x0, 1)[0], AHT20_STATUSBIT_CALIBRATED) == 1:
        time.sleep(0.01)
    
# Send Measure command
i2c_bus.write_i2c_block_data(AHT20_I2CADDR, 0, AHT20_CMD_MEASURE)

# While busy bit = 1, wait 80 ms and retry
while get_normalized_bit(i2c_bus.read_i2c_block_data(AHT20_I2CADDR, 0x0, 1)[0], AHT20_STATUSBIT_BUSY) == 1:
    time.sleep(0.08)

# Read data, 7 bits
measure = i2c_bus.read_i2c_block_data(AHT20_I2CADDR, 0x0, 7)

# Interpret data
## Humdity
measurement_humidity =  (measure[1] << 12) | (measure[2] << 4) | (measure[3] >> 4)
humidity = measurement_humidity * 100 / pow(2,20)
print("Humidity:    " + "{:10.2f}".format(humidity) + " %RH")

## Temperature
measurement_temp = ((measure[3] & 0xF) << 16) | (measure[4] << 8) | measure[5]
temp = (measurement_temp / (pow(2,20)))*200-50
print("Temperature: " + "{:10.2f}".format(temp) + " °C")

## TODO: Check CRC
