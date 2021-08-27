import pyvisa
import time
import csv
import numpy as np
import pandas as pd

# inital params
data = np.array([("time[s]", "Voltage CH1", "Voltage CH2", "Current CH1", "Current CH2", "Power CH1", "Power CH2")])
# testTime = time.time() + 2082844800
voltage = 1.165

# Create the resource manager
rm = pyvisa.ResourceManager()

# Create an instance for the PSU
psu = rm.open_resource('ASRL4::INSTR')

psu.read_termination = '\n'
psu.write_termination = '\n'
psu.baud_rate = 115200
psu.write(':SOURce1:VOLTage '+str(voltage))

duration = 5
def readings(duration, arr):
    for x in range (duration):
        time.sleep(1)
        voltReadings = psu.query(':MEASure:VOLTage:ALL?')
        voltReadings = voltReadings.split(',')
        v1 = voltReadings[0]
        v2 = voltReadings[1]
        currReadings = psu.query(':MEASure:CURRent:ALL?')
        currReadings = currReadings.split(',')
        c1 = currReadings[0]
        c2 = currReadings[1]
        powReadings = psu.query(':MEASure:POWEr:ALL?')
        powReadings = powReadings.split(',')
        p1 = powReadings[0]
        p2 = powReadings[1]
        timestamp = time.time() + 2082844800 # Using MAC timestamp epoch to be in the same format as labview
        row = np.array([timestamp, v1, v2, c1, c2, p1, p2])
        arr = np.append(arr, [row], axis=0)
        print(arr)
    return arr

def loopReading(arr):
    try:
        while True:
            time.sleep(1)
            voltReadings = psu.query(':MEASure:VOLTage:ALL?')
            voltReadings = voltReadings.split(',')
            v1 = voltReadings[0]
            v2 = voltReadings[1]
            currReadings = psu.query(':MEASure:CURRent:ALL?')
            currReadings = currReadings.split(',')
            c1 = currReadings[0]
            c2 = currReadings[1]
            powReadings = psu.query(':MEASure:POWEr:ALL?')
            powReadings = powReadings.split(',')
            p1 = powReadings[0]
            p2 = powReadings[1]
            timestamp = time.time() + 2082844800 # Using MAC timestamp epoch to be in the same format as labview
            row = np.array([timestamp, v1, v2, c1, c2, p1, p2])
            arr = np.append(arr, [row], axis=0)
            print(arr)
    except KeyboardInterrupt:
        return arr
# lpgbt 1.027 to 1.036 DESY
# manual max is 1.32, min is 1.08
dataOut = loopReading(data)
# dataOut = loopReading(data)
# # Write data to csv file
# with open('lpGBTtest0.csv', mode='w') as test_file:
#     writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# pd.DataFrame(dataOut).to_csv('readings'+str(duration)+'.csv')
pd.DataFrame(dataOut).to_csv('readings'+str(voltage)+'.csv')