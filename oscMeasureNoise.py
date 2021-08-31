import pyvisa
import pandas as pd
import time
import numpy as np

rm = pyvisa.ResourceManager()
osc = rm.open_resource('TCPIP0::137.158.93.119::inst0::INSTR')

# osc.write('DVM:SOUrce CH1')
testStartTime = time.strftime("%H:%M:%S", time.localtime())
data = np.array([('Timestamp', 'Offset', 'Ch1 reading', 'Ch2 reading', 'AFG frequency', 'AFG amplitude')])

# frequency = 5000
freq_low = 10000
freq_high = 400000
freq_step = 1000
# preset waveforms: sine, square, ramp, noise, DC, etc...
waveform = "SINE"
offset = 1.2
# amplitude is the peak to peak voltage in volts
amplitude = 0.02
osc.write('AFG:FUNCtion ' + str(waveform))
osc.write('AFG:FREQuency ' + str(freq_low))
osc.write('AFG:OFFSet ' + str(offset))
osc.write('AFG:AMPLitude ' + str(amplitude))


def sweep_frequency(freq_start, freq_end, freq_step, arr):
    frequencies = [f for f in np.arange(freq_start, freq_end, freq_step)]
    for freq in frequencies:
        osc.write('DVM:SOUrce CH3')
        time.sleep(1.25)
        timestamp1 = time.time() + 2082844800
        ch1 = float(osc.query('DVM:MEASU:VAL?'))

        osc.write('DVM:SOUrce CH3')
        time.sleep(1.25)
        ch2 = float(osc.query('DVM:MEASU:VAL?'))

        freq_read = float(osc.query('AFG:FREQuency?'))
        amp_read = float(osc.query('AFG:AMPLitude?'))

        row = np.array([round(timestamp1, 2), offset, ch1, ch2, freq_read, amp_read])
        arr = np.append(arr, [row], axis=0)
        print(arr)
        osc.write('AFG:FREQuency ' + str(freq))
    return arr


def loop_infinite(arr):
    try:
        while True:
            osc.write('DVM:SOUrce CH3')
            time.sleep(1.25)
            timestamp1 = time.time() + 2082844800
            ch1 = float(osc.query('DVM:MEASU:VAL?'))
            # row1 = np.array([round(timestamp1, 2), 'CH1', ch1])

            # time.sleep(0.3)
            osc.write('DVM:SOUrce CH3')
            time.sleep(1.25)
            # timestamp2 = time.time() + 2082844800
            ch2 = float(osc.query('DVM:MEASU:VAL?'))
            # row2 = np.array([round(timestamp2, 2), 'CH2', ch2])

            freq_read = float(osc.query('AFG:FREQuency?'))
            # time.sleep(1.5)
            amp_read = float(osc.query('AFG:AMPLitude?'))
            # timestamp3 = time.time() + 2082844800
            # row3 = np.array([round(timestamp3, 2), 'Frequency', freq_read, 'Amplitude', amp_read])

            row = np.array([round(timestamp1, 2), offset, ch1, ch2, freq_read, amp_read])
            arr = np.append(arr, [row], axis=0)
            print(arr)
    except KeyboardInterrupt:
        return arr


# dataRecord = recordDuration(5, data)
dataRecord = sweep_frequency(freq_low, freq_high, freq_step, data)
pd.DataFrame(dataRecord).to_csv('oscData\\oscilloscope' + str(offset) + str(waveform) + 'start' + str(freq_low) + 'end'
                                + str(freq_high) + 'time' + str(testStartTime).replace(':', '-') + '.csv')
