import pyvisa
import time
import numpy as np
import pandas as pd

# inital params
data = np.array(
    [
        (
            "time[s]",
            "Voltage CH1",
            "Voltage CH2",
            "Current CH1",
            "Current CH2",
            "Power CH1",
            "Power CH2",
        )
    ]
)
testStartTime = time.strftime("%H:%M:%S", time.localtime())
voltage = 15

# Create the resource manager
rm = pyvisa.ResourceManager()

# Create an instance for the PSU
psu = rm.open_resource("ASRL4::INSTR")

psu.read_termination = "\n"
psu.write_termination = "\n"
psu.baud_rate = 115200
# psu.write(':SOURce1:VOLTage ' + str(voltage))

duration = 5


def readings(duration, arr):
    for x in range(duration):
        time.sleep(1)
        volt_readings = psu.query(":MEASure:VOLTage:ALL?")
        volt_readings = volt_readings.split(",")
        v1 = volt_readings[0]
        v2 = volt_readings[1]
        curr_readings = psu.query(":MEASure:CURRent:ALL?")
        curr_readings = curr_readings.split(",")
        c1 = curr_readings[0]
        c2 = curr_readings[1]
        pow_readings = psu.query(":MEASure:POWEr:ALL?")
        pow_readings = pow_readings.split(",")
        p1 = pow_readings[0]
        p2 = pow_readings[1]
        timestamp = (
            time.time() + 2082844800
        )  # Using MAC timestamp epoch to be in the same format as labview
        row = np.array([timestamp, v1, v2, c1, c2, p1, p2])
        arr = np.append(arr, [row], axis=0)
        print(arr)
    return arr


def loop_reading(arr):
    try:
        while True:
            time.sleep(1)
            volt_readings = psu.query(":MEASure:VOLTage:ALL?")
            volt_readings = volt_readings.split(",")
            v1 = volt_readings[0]
            v2 = volt_readings[1]
            curr_readings = psu.query(":MEASure:CURRent:ALL?")
            curr_readings = curr_readings.split(",")
            c1 = curr_readings[0]
            c2 = curr_readings[1]
            pow_readings = psu.query(":MEASure:POWEr:ALL?")
            pow_readings = pow_readings.split(",")
            p1 = pow_readings[0]
            p2 = pow_readings[1]
            timestamp = (
                time.time() + 2082844800
            )  # Using MAC timestamp epoch to be in the same format as labview
            row = np.array([timestamp, v1, v2, c1, c2, p1, p2])
            arr = np.append(arr, [row], axis=0)
            print(arr)
    except KeyboardInterrupt:
        return arr


# Start reading
dataOut = loop_reading(data)
# Write data to csv file
pd.DataFrame(dataOut).to_csv(
    "psuData\\readings" + str(testStartTime).replace(":", "-") + ".csv"
)
