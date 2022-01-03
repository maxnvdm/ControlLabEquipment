import pyvisa
import pandas as pd
import time
import numpy as np

rm = pyvisa.ResourceManager()
osc = rm.open_resource("TCPIP0::137.158.93.119::inst0::INSTR")

# osc.write('DVM:SOUrce CH1')
testStartTime = time.strftime("%H:%M:%S", time.localtime())
data = np.array(
    [
        (
            "Timestamp",
            "Offset",
            "Ch1 reading",
            "Ch2 reading",
            "AFG frequency",
            "AFG amplitude",
        )
    ]
)

# 1.2V DC sweep
# dc_start = 1.135
# dc_end = 1.165
# dc_step = 0.005

# 2.5V DC sweep
dc_start = 1.95
dc_end = 2.02  # 2.01
dc_step = 0.01  # 0.005
# preset waveforms: sine, square, ramp, noise, DC, etc...
waveform = "DC"
offset = dc_start
# offset = 1.21

# amplitude is the peak to peak voltage in volts
amplitude = 0.02
osc.write("AFG:FUNCtion " + str(waveform))
osc.write("AFG:OFFSet " + str(offset))

def sweep_dc(dc_start, dc_end, dc_step, arr):
    print("Starting DC sweep test")
    voltages = [round(volt, 3) for volt in np.arange(dc_start, dc_end, dc_step)]
    for v in voltages:
        testRunTime = 0
        print(v)
        input("Stop previous BERT test and restart. Press any key to continue")
        osc.write("AFG:OFFSet " + str(v))
        testStart = time.time()
        while testRunTime < 120:
            print(v)
            if v > 2.68:  # 1.3 for 1.2V line, 2.68V for 2.5V line
                return arr

            osc.write("DVM:SOUrce CH1")
            time.sleep(1.25)
            timestamp1 = time.time() + 2082844800
            ch1 = float(osc.query("DVM:MEASU:VAL?"))

            if ch1 >= 1.29:
                osc.write("AFG:OFFSet " + str(1))
                print("Voltage reached 1.29, test reset to safe levels")
                return arr

            osc.write("DVM:SOUrce CH2")
            time.sleep(1.25)
            ch2 = float(osc.query("DVM:MEASU:VAL?"))

            if ch2 >= 2.71:
                osc.write("AFG:OFFSet " + str(2.1))
                print("Voltage reached 2.71, test reset to safe levels")
                return arr

            freq_read = "DC"
            amp_read = "DC"

            row = np.array(
                [round(timestamp1, 2), offset, ch1, ch2, freq_read, amp_read]
            )
            arr = np.append(arr, [row], axis=0)
            print(arr)
            testRunTime = time.time() - testStart
    return arr


def loop_infinite(arr):
    try:
        while True:
            osc.write("DVM:SOUrce CH1")
            time.sleep(1.25)
            timestamp1 = time.time() + 2082844800
            ch1 = float(osc.query("DVM:MEASU:VAL?"))
            # row1 = np.array([round(timestamp1, 2), 'CH1', ch1])
            if ch1 >= 1.29:
                osc.write("AFG:OFFSet " + str(1))
                print("Voltage reached 1.29, test reset to safe levels")
                return arr
            # time.sleep(0.3)
            osc.write("DVM:SOUrce CH2")
            time.sleep(1.25)
            # timestamp2 = time.time() + 2082844800
            ch2 = float(osc.query("DVM:MEASU:VAL?"))
            # row2 = np.array([round(timestamp2, 2), 'CH2', ch2])

            # freq_read = float(osc.query('AFG:FREQuency?'))
            freq_read = "DC"
            # time.sleep(1.5)
            # amp_read = float(osc.query('AFG:AMPLitude?'))
            amp_read = "DC"
            # timestamp3 = time.time() + 2082844800
            # row3 = np.array([round(timestamp3, 2), 'Frequency', freq_read, 'Amplitude', amp_read])

            row = np.array(
                [round(timestamp1, 2), offset, ch1, ch2, freq_read, amp_read]
            )
            arr = np.append(arr, [row], axis=0)
            print(arr)

    except KeyboardInterrupt:
        return arr


# dataRecord = loop_infinite(data)
dataRecord = sweep_dc(dc_start, dc_end, dc_step, data)
pd.DataFrame(dataRecord).to_csv(
    "oscData\\oscilloscope"
    + str(offset)
    + str(waveform)
    + "start"
    + str(freq_low)
    + "end"
    + str(freq_high)
    + "time"
    + str(testStartTime).replace(":", "-")
    + ".csv"
)
