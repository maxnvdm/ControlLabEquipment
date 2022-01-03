import pyvisa
import pandas as pd
import time
import numpy as np
import safetyChecks

# Setup pyvisa comms with oscilloscope
rm = pyvisa.ResourceManager()
osc = rm.open_resource("TCPIP0::137.158.93.119::inst0::INSTR")

# Create list of frequency ranges to sweep through
low_frequencies = list(range(0, 1000, 10))
low_frequencies[0] = 1
mid_frequencies = list(range(1000, 10000, 100))
high_frequencies = list(range(10000, 100000, 1000))
all_frequencies = low_frequencies + mid_frequencies + high_frequencies

# Create dictionaries for waveforms and their config
waves_1 = {
    "SINE": {"offset": 1.212, "amplitude": 0.15},
    "RAMP": {"offset": 1.212, "amplitude": 0.15},
    "SINC": {"offset": 1.175, "amplitude": 0.14},
    "SQUARE": {"offset": 1.212, "amplitude": 0.15},
}
waves_2 = {
    "SINE": {"offset": 2.345, "amplitude": 0.45},
    "RAMP": {"offset": 2.345, "amplitude": 0.5},
    "SINC": {"offset": 2.15, "amplitude": 0.45},
    "SQUARE": {"offset": 2.322, "amplitude": 0.45},
}

# Select 1.2 or 2.5 waveforms
line = 2
if line == 2:
    waves_line = waves_2
elif line == 1:
    waves_line = waves_1

# Initial waveform settings
if waves_line == waves_1:
    offset = safetyChecks.safe_values1_2["offset"]
    amplitude = safetyChecks.safe_values1_2["amplitude"]
    amplitude = safetyChecks.amplitude_check1_2(amplitude)
    offset = safetyChecks.offset_check1_2(offset)
else:
    offset = safetyChecks.safe_values2_5["offset"]
    amplitude = safetyChecks.safe_values2_5["amplitude"]
    amplitude = safetyChecks.amplitude_check2_5(amplitude)
    offset = safetyChecks.offset_check2_5(offset)

osc.write("AFG:FUNCtion DC")
osc.write("AFG:FREQuency 1")
osc.write("AFG:OFFSet " + str(offset))
osc.write("AFG:AMPLitude " + str(amplitude))
osc.write("AFG:OUTPut:STATE ON")

testStartTime = time.strftime("%H:%M:%S", time.localtime())
data = np.array(
    [
        (
            "Timestamp start",
            "Timestamp end" "Offset",
            "Ch1 reading",
            "Ch2 reading",
            "AFG frequency",
            "AFG amplitude",
            "maximum1",
            "maximum2",
            "minimum1",
            "minimum2",
            "mean1",
            "mean2",
            "pkpk1",
            "pkpk2",
        )
    ]
)


def sweep_frequency(waves_line, frequencies, arr, line):
    print("Starting frequency sweep test")
    for wave in list(waves_line.keys()):
        input("About to move onto next waveform, press any key to continue")
        osc.write("AFG:FUNCtion " + str(wave))

        if line == 1:
            wave_offset = safetyChecks.offset_check1_2(waves_line[wave]["offset"])
            wave_amplitude = safetyChecks.amplitude_check1_2(waves_line[wave]["offset"])
        elif line == 2:
            wave_offset = safetyChecks.offset_check2_5(waves_line[wave]["offset"])
            wave_amplitude = safetyChecks.amplitude_check2_5(waves_line[wave]["offset"])

        osc.write("AFG:OFFSet " + str(wave_offset))
        osc.write("AFG:AMPLitude " + str(wave_amplitude))

        for freq in frequencies:
            osc.write("AFG:FREQuency " + str(freq))
            timestamp1 = time.time() + 2082844800
            time.sleep(3)
            osc.write("DVM:SOUrce CH1")
            time.sleep(1.25)
            ch1 = float(osc.query("DVM:MEASU:VAL?"))

            if line == 1:
                if ch1 >= 1.29:
                    osc.write("AFG:OFFSet " + str(1.17))
                    print("Voltage reached 1.29, test reset to safe levels")
                    return arr

            osc.write("DVM:SOUrce CH2")
            time.sleep(1.25)
            ch2 = float(osc.query("DVM:MEASU:VAL?"))

            if line == 2:
                if ch2 >= 2.71:
                    osc.write("AFG:OFFSet " + str(2.15))
                    print("Voltage reached 2.71, test reset to safe levels")
                    return arr

            freq_read = float(osc.query("AFG:FREQuency?"))
            amp_read = float(osc.query("AFG:AMPLitude?"))
            measurements = safetyChecks.measurements(osc)
            timestamp2 = time.time() + 2082844800
            row = np.array(
                [
                    round(timestamp1, 2),
                    round(timestamp2, 2),
                    wave_offset,
                    ch1,
                    ch2,
                    freq_read,
                    amp_read,
                ]
                + measurements
            )
            arr = np.append(arr, [row], axis=0)
            print(arr)
        # Writing safe values before changing waveforms
        if line == 1:
            wave_offset = safetyChecks.safe_values1_2["offset"]
            wave_amplitude = safetyChecks.safe_values1_2["amplitude"]
        elif line == 2:
            wave_offset = safetyChecks.safe_values2_5["offset"]
            wave_amplitude = safetyChecks.safe_values2_5["amplitude"]
        osc.write("AFG:OFFSet " + str(wave_offset))
        osc.write("AFG:AMPLitude " + str(wave_amplitude))
    return arr


def test_settings(waveforms, arr):
    print("Starting frequency settings test")
    for wave in waveforms:
        osc.write("DVM:SOUrce CH1")
        time.sleep(1.25)
        ch1 = float(osc.query("DVM:MEASU:VAL?"))

        # if ch1 >= 1.29:
        #     osc.write('AFG:OFFSet ' + str(1))
        #     print("Voltage reached 1.29, test reset to safe levels")
        #     return arr

        osc.write("DVM:SOUrce CH2")
        time.sleep(1.25)
        ch2 = float(osc.query("DVM:MEASU:VAL?"))

        if ch2 >= 2.71:
            osc.write("AFG:OFFSet " + str(2.1))
            print("Voltage reached 2.71, test reset to safe levels")
            return arr
        input("Verify settings and press any key to continue")

        osc.write("DVM:SOUrce CH1")
        time.sleep(1.25)
        ch1 = float(osc.query("DVM:MEASU:VAL?"))

        # if ch1 >= 1.29:
        #     osc.write('AFG:OFFSet ' + str(1))
        #     print("Voltage reached 1.29, test reset to safe levels")
        #     return arr

        osc.write("DVM:SOUrce CH2")
        time.sleep(1.25)
        ch2 = float(osc.query("DVM:MEASU:VAL?"))

        if ch2 >= 2.71:
            osc.write("AFG:OFFSet " + str(2.1))
            print("Voltage reached 2.71, test reset to safe levels")
            return arr

        # ch1 = "N/A"
        timestamp1 = time.time() + 2082844800
        freq_read = float(osc.query("AFG:FREQuency?"))
        amp_read = float(osc.query("AFG:AMPLitude?"))
        selected_offset = float(osc.query("AFG:OFFSet?"))
        row = np.array(
            [round(timestamp1, 2), selected_offset, ch1, ch2, freq_read, amp_read]
        )
        arr = np.append(arr, [row], axis=0)
        print(arr)
        osc.write("AFG:OFFSet 2.2")
        osc.write("AFG:AMPLitude 0.05")
        osc.write("AFG:FUNCtion " + str(wave))
    return arr


# config_settings = test_settings(waveforms, data)
dataRecord = sweep_frequency(waves_line, data, line)
pd.DataFrame(dataRecord).to_csv(
    "oscData\\oscilloscopeFrequencySweep"
    + str(line)
    + str(testStartTime).replace(":", "-")
    + ".csv"
)
# pd.DataFrame(config_settings).to_csv('oscData\\testSettings' + str(testStartTime).replace(':', '-') + '.csv')
