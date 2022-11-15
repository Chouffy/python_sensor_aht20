import AHT20
import datetime, time

# Initialize an AHT20
aht20 = AHT20.AHT20()

# A different bus can be specified with the BusNum variable
# aht20 = AHT20.AHT20(BusNum = 1)

while 1:

    # Fill a string with date, humidity and temperature
    data = str(datetime.datetime.now()) + ";" + "{:10.2f}".format(aht20.get_humidity()) + " %RH;" + "{:10.2f}".format(aht20.get_temperature()) + " °C"
    # Data with crc8 check
    data_crc8 = str(datetime.datetime.now()) + ";" + "{:10.2f}".format(aht20.get_humidity_crc8()) + " %RH;" + "{:10.2f}".format(aht20.get_temperature_crc8()) + " °C"

    # Print in the console
    print(data)
    print("data with crc check: {0}".format(data_crc8))
    
    # Append in a file
    log = open("log.txt", "a")
    log.write(data + "\n")
    log.close()

    # Wait
    time.sleep(2)
