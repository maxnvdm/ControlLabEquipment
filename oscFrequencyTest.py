import pyvisa
import pandas as pd
import time
import numpy as np
import safetyChecks

rm = pyvisa.ResourceManager()
osc = rm.open_resource('TCPIP0::137.158.93.119::inst0::INSTR')

testStartTime = time.strftime("%H:%M:%S", time.localtime())
data = np.array([('Timestamp', 'Offset', 'Ch1 reading', 'Ch2 reading', 'AFG frequency', 'AFG amplitude')])

waves_1 = {"SINE": {"offset": 1.2, "amplitude": 0.05,
                    "low_freq_start": 1, "low_freq_end": 1000, "low_freq_step": 10,
                    "mid_freq_start": 1000, "mid_freq_end": 10000, "mid_freq_step": 100,
                    "high_freq_start": 10000, "high_freq_end": 300000, "high_freq_step": 1000},
           "RAMP": {"offset": 1.17, "amplitude": 0.1},
           "SINC": {"offset": 1.1, "amplitude": 0.1},
           "SQUARE": {"offset": 1.17, "amplitude": 0.1}}
waves_2 = {"SINE": {"offset": 2.2, "amplitude": 0.05,
                    "low_freq_start": 1, "low_freq_end": 1000, "low_freq_step": 10},
           "RAMP": {"offset": 2.2, "amplitude": 0.05},
           "SINC": {"offset": 2.2, "amplitude": 0.05},
           "SQUARE": {"offset": 2.2, "amplitude": 0.05}}

waves_line = waves_2

waveforms = list(waves_line.keys())
waveform = waveforms[0]
freq_start = waves_line[waveform]["low_freq_start"]
freq_end = waves_line[waveform]["low_freq_end"]
freq_step = waves_line[waveform]["low_freq_step"]
offset = waves_line[waveform]["offset"]
amplitude = waves_line[waveform]["amplitude"]

if waves_line == waves_1:
    safetyChecks.amplitude_check1_2(amplitude)
    safetyChecks.offset_check1_2(offset)
else:
    safetyChecks.amplitude_check2_5(amplitude)
    safetyChecks.offset_check2_5(offset)

osc.write('AFG:FUNCtion ' + str(waveform))
osc.write('AFG:FREQuency ' + str(freq_start))
osc.write('AFG:OFFSet ' + str(offset))
osc.write('AFG:AMPLitude ' + str(amplitude))
osc.write('AFG:OUTPut:STATE ON')

testStartTime = time.strftime("%H:%M:%S", time.localtime())
data = np.array([('Timestamp', 'Offset', 'Ch1 reading', 'Ch2 reading', 'AFG frequency', 'AFG amplitude')])


def sweep_frequency(freq_start, freq_end, freq_step, arr):
    print("Starting frequency sweep test")
    frequencies = [f for f in np.arange(freq_start, freq_end, freq_step)]
    for freq in frequencies:
        osc.write('DVM:SOUrce CH1')
        time.sleep(1.25)
        timestamp1 = time.time() + 2082844800
        ch1 = float(osc.query('DVM:MEASU:VAL?'))

        if ch1 >= 1.29:
            osc.write('AFG:OFFSet ' + str(1))
            print("Voltage reached 1.29, test reset to safe levels")
            return arr

        osc.write('DVM:SOUrce CH2')
        time.sleep(1.25)
        ch2 = float(osc.query('DVM:MEASU:VAL?'))

        if ch2 >= 2.71:
            osc.write('AFG:OFFSet ' + str(2.1))
            print("Voltage reached 2.71, test reset to safe levels")
            return arr

        freq_read = float(osc.query('AFG:FREQuency?'))
        amp_read = float(osc.query('AFG:AMPLitude?'))

        row = np.array([round(timestamp1, 2), offset, ch1, ch2, freq_read, amp_read])
        arr = np.append(arr, [row], axis=0)
        print(arr)

        osc.write('AFG:FREQuency ' + str(freq))
    return arr


def test_settings(waveforms, arr):
    print("Starting frequency settings test")
    for wave in waveforms:
        osc.write('DVM:SOUrce CH1')
        time.sleep(1.25)
        ch1 = float(osc.query('DVM:MEASU:VAL?'))

        # if ch1 >= 1.29:
        #     osc.write('AFG:OFFSet ' + str(1))
        #     print("Voltage reached 1.29, test reset to safe levels")
        #     return arr

        osc.write('DVM:SOUrce CH2')
        time.sleep(1.25)
        ch2 = float(osc.query('DVM:MEASU:VAL?'))

        if ch2 >= 2.71:
            osc.write('AFG:OFFSet ' + str(2.1))
            print("Voltage reached 2.71, test reset to safe levels")
            return arr
        input("Verify settings and press any key to continue")

        osc.write('DVM:SOUrce CH1')
        time.sleep(1.25)
        ch1 = float(osc.query('DVM:MEASU:VAL?'))

        # if ch1 >= 1.29:
        #     osc.write('AFG:OFFSet ' + str(1))
        #     print("Voltage reached 1.29, test reset to safe levels")
        #     return arr

        osc.write('DVM:SOUrce CH2')
        time.sleep(1.25)
        ch2 = float(osc.query('DVM:MEASU:VAL?'))

        if ch2 >= 2.71:
            osc.write('AFG:OFFSet ' + str(2.1))
            print("Voltage reached 2.71, test reset to safe levels")
            return arr

        # ch1 = "N/A"
        timestamp1 = time.time() + 2082844800
        freq_read = float(osc.query('AFG:FREQuency?'))
        amp_read = float(osc.query('AFG:AMPLitude?'))
        selected_offset = float(osc.query('AFG:OFFSet?'))
        row = np.array([round(timestamp1, 2), selected_offset, ch1, ch2, freq_read, amp_read])
        arr = np.append(arr, [row], axis=0)
        print(arr)
        osc.write('AFG:OFFSet 2.2')
        osc.write('AFG:AMPLitude 0.05')
        osc.write('AFG:FUNCtion ' + str(wave))
    return arr


config_settings = test_settings(waveforms, data)
# dataRecord = sweep_frequency(freq_start, freq_end, freq_step, data)
# pd.DataFrame(dataRecord).to_csv('oscData\\oscilloscope' + str(offset) + str(waveform) + 'start' + str(freq_start) + 'end'
#                                 + str(freq_end) + 'time' + str(testStartTime).replace(':', '-') + '.csv')
pd.DataFrame(config_settings).to_csv('oscData\\testSettings' + str(testStartTime).replace(':', '-') + '.csv')