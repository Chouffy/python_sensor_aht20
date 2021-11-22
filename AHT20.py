from smbus2 import SMBus
import time

def get_normalized_bit(value, bit_index):
    # Return only one bit from value indicated in bit_index
    return (value >> bit_index) & 1

AHT20_I2CADDR = 0x38
AHT20_CMD_SOFTRESET = [0xBA]
AHT20_CMD_INITIALIZE = [0xBE, 0x08, 0x00]
AHT20_CMD_MEASURE = [0xAC, 0x33, 0x00]
AHT20_STATUSBIT_BUSY = 7                    # The 7th bit is the Busy indication bit. 1 = Busy, 0 = not.
AHT20_STATUSBIT_CALIBRATED = 3              # The 3rd bit is the CAL (calibration) Enable bit. 1 = Calibrated, 0 = not

class AHT20:
    # I2C communication driver for AHT20, using only smbus2

    def __init__(self, BusNum=1):
        # Initialize AHT20
        self.BusNum = BusNum
        self.cmd_soft_reset()

        # Check for calibration, if not done then do and wait 10 ms
        if not self.get_status_calibrated == 1:
            self.cmd_initialize()
            while not self.get_status_calibrated() == 1:
                time.sleep(0.01)
        
    def cmd_soft_reset(self):
        # Send the command to soft reset
        with SMBus(self.BusNum) as i2c_bus:
            i2c_bus.write_i2c_block_data(AHT20_I2CADDR, 0x0, AHT20_CMD_SOFTRESET)
        time.sleep(0.04)    # Wait 40 ms after poweron
        return True

    def cmd_initialize(self):
        # Send the command to initialize (calibrate)
        with SMBus(self.BusNum) as i2c_bus:
            i2c_bus.write_i2c_block_data(AHT20_I2CADDR, 0x0 , AHT20_CMD_INITIALIZE)
        return True

    def cmd_measure(self):
        # Send the command to measure
        with SMBus(self.BusNum) as i2c_bus:
            i2c_bus.write_i2c_block_data(AHT20_I2CADDR, 0, AHT20_CMD_MEASURE)
        time.sleep(0.08)    # Wait 80 ms after measure
        return True

    def get_status(self):
        # Get the full status byte
        with SMBus(self.BusNum) as i2c_bus:
            return i2c_bus.read_i2c_block_data(AHT20_I2CADDR, 0x0, 1)[0]
        return True

    def get_status_calibrated(self):
        # Get the calibrated bit
        return get_normalized_bit(self.get_status(), AHT20_STATUSBIT_CALIBRATED)

    def get_status_busy(self):
        # Get the busy bit
        return get_normalized_bit(self.get_status(), AHT20_STATUSBIT_BUSY)
            
    def get_measure(self):
        # Get the full measure

        # Command a measure
        self.cmd_measure()

        # Check if busy bit = 0, otherwise wait 80 ms and retry
        while self.get_status_busy() == 1:
            time.sleep(0.08) # Wait 80 ns
        
        # TODO: do CRC check

        # Read data and return it
        with SMBus(self.BusNum) as i2c_bus:
            return i2c_bus.read_i2c_block_data(AHT20_I2CADDR, 0x0, 7)

    def get_temperature(self):
        # Get a measure, select proper bytes, return converted data
        measure = self.get_measure()
        measure = ((measure[3] & 0xF) << 16) | (measure[4] << 8) | measure[5]
        measure = measure / (pow(2,20))*200-50
        return measure

    def get_humidity(self):
        # Get a measure, select proper bytes, return converted data
        measure = self.get_measure()
        measure = (measure[1] << 12) | (measure[2] << 4) | (measure[3] >> 4)
        measure = measure * 100 / pow(2,20)
        return measure
