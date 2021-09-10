def amplitude_check1_2(amp):
    if amp > 0.15:
        raise Exception(f'Amplitude value is unsafe <{amp}>, maximum is 0.15')
    else:
        return amp


def amplitude_check2_5(amp):
    if amp > 0.5:
        raise Exception(f'Amplitude value is unsafe <{amp}>, maximum is 0.5')
    else:
        return amp


def offset_check1_2(offset):
    if offset > 1.22:
        raise Exception(f'Offset value is unsafe <{offset}>, maximum is 1.22')
    else:
        return offset


def offset_check2_5(offset):
    if offset > 2.35:
        raise Exception(f'Offset value is unsafe <{offset}>, maximum is 2.35')
    else:
        return offset


def measurements(osc):
    # Maximum
    maximum1 = osc.query('MEASUREMENT:MEAS1:RESUlts:CURRentacq:MEAN?')
    maximum2 = osc.query('MEASUREMENT:MEAS3:RESUlts:CURRentacq:MEAN?')
    # Minimum
    minimum1 = osc.query('MEASUREMENT:MEAS2:RESUlts:CURRentacq:MEAN?')
    minimum2 = osc.query('MEASUREMENT:MEAS4:RESUlts:CURRentacq:MEAN?')
    # Mean
    mean1 = osc.query('MEASUREMENT:MEAS5:RESUlts:CURRentacq:MEAN?')
    mean2 = osc.query('MEASUREMENT:MEAS6:RESUlts:CURRentacq:MEAN?')
    # Peak to Peak
    pkpk1 = osc.query('MEASUREMENT:MEAS7:RESUlts:CURRentacq:MEAN?')
    pkpk2 = osc.query('MEASUREMENT:MEAS8:RESUlts:CURRentacq:MEAN?')
    return [maximum1, maximum2, minimum1, minimum2, mean1, mean2, pkpk1, pkpk2]


safe_values1_2 = {"offset": 1.14,
                  "amplitude": 0.03,
                  "frequency": 1}
safe_values2_5 = {"offset": 2.15,
                  "amplitude": 0.03,
                  "frequency": 1}
