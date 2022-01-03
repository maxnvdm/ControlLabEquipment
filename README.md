# Control Lab Equipment
This repo contains scripts used to control a PSU and oscilloscope/function generator through [PyVISA](https://pyvisa.readthedocs.io). VISA provides an abstraction from the technical interfaces and bus systems (e.g. GPIB, USB, Ethernet) used when communicating with different equipment. By following the command syntax of each instrument, it is possible to control multiple devices using the PyVISA package and automate testing procedures.

Undervoltage and power supply noise tests are implemented using a PSU and oscilloscope with a built-in function generator. The PSU provides the nominal DC supply voltages while the oscilloscope measures the voltage at the input to the device under test (DUT) and the function generator is used to adjust the voltage level as well as superimpose AC waveforms ("noise") on the DC rails.

## Requirements
Python packages:
- PyVISA
- Numpy
- Pandas
- Time

## Programmanble Power Supply
Model: GW INSTEK GPP-3323 \
Files: noiseReadings.py \
The PSU program connects to the PSU through the serial USB interface, and takes readings of the voltage, current and power output. Each reading is timestamped and exported to a csv file. An example of the output can be seen in the psuData folder.

## Oscilloscope with function generator
Model: Tektronix MS064B \
Files: oscVoltageTest.py, oscFrequencyTest.py, safetyChecks.py
The oscilloscope programs connects to the oscilloscope over Ethernet. The voltage test program (oscVoltageTest.py) sweeps through voltage levels, incrementing the voltage after a set duration. Readings of the voltages at the input to the DUT are recorded along with a timestamp for each reading. 

The frequency test program (oscFrequencyTest.py) cycles through four waveforms (sine, ramp, sinc and square). Each cycle starts at 1 Hz and increments the frequency after a set duration, up to a maximum of 100000 Hz. In addition to recording the voltages, this program also records the amplitude and frequency of the AC noise signal being fed to the DUT. Examples of the output from these programs can be found in the oscData folder.

On top of the test programs, an additional file (safetyChecks.py) is used to provide a fail safe against setting the output voltage outside the device's specified operating limits. 