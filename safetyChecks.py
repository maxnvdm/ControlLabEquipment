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
    if offset > 1.2:
        raise Exception(f'Offset value is unsafe <{offset}>, maximum is 1.2')
    else:
        return offset


def offset_check2_5(offset):
    if offset > 2.35:
        raise Exception(f'Offset value is unsafe <{offset}>, maximum is 2.35')
    else:
        return offset

