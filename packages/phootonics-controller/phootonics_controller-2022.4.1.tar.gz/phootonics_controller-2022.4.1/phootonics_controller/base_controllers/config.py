import numpy

VCM_PORT = '/dev/tty.ec_vcm_main'
EXT_VCM_PORT = '/dev/tty.ec_vcm_ext'
LAST_POSITION = 1
LAST_CAVITY = 1
CAVITY1_INDEX = 'ec1'
CAVITY2_INDEX = 'ec2'
CAVITY3_INDEX = 'ec3'
CAVITY4_INDEX = 'ec4'
CAVITY1_URL = 'http://0.0.0.0:5001/ec/api/v1.0'
CAVITY2_URL = 'http://0.0.0.0:5002/ec/api/v1.0'
CAVITY3_URL = 'http://0.0.0.0:5003/ec/api/v1.0'
CAVITY4_URL = 'http://0.0.0.0:5004/ec/api/v1.0'

ADC_CHANNEL = 0
REF = 5.08  # Modify according to actual voltage (read voltage) external AVDD and AVSS (Default), or internal 2.5V
configuration_dictionary = {
    CAVITY1_INDEX: {'wavelength': [1037.2, 1353.6], 'x_position': -18.65, 'y_position': 0.5,
                    's2params': {'pulse_period': 6000, 'pulse_width': 300,
                                 'pulsing_mode': 'internal', 'applied_voltage': 18.6}, 'temperature_setpoint': 18},
    CAVITY2_INDEX: {'wavelength': [846.0, 1037.1], 'x_position': -16.75, 'y_position': -0.65,
                    's2params': {'pulse_period': 6000, 'pulse_width': 300,
                                 'pulsing_mode': 'internal', 'applied_voltage': 19.3}, 'temperature_setpoint': 18},
    CAVITY3_INDEX: {'wavelength': [1600.8, 1813.9], 'x_position': -14.35, 'y_position': -0.1,
                    's2params': {'pulse_period': 6000, 'pulse_width': 300,
                                 'pulsing_mode': 'internal', 'applied_voltage': 15.4}, 'temperature_setpoint': 18},
    CAVITY4_INDEX: {'wavelength': [1354, 1600], 'x_position': -5.5, 'y_position': -1.5,
                    's2params': {'pulse_period': 6000, 'pulse_width': 300,
                                 'pulsing_mode': 'internal', 'applied_voltage': 17.2}, 'temperature_setpoint': 18}
}

WL_INCREMENT = 1.0


def get_scanning_wavelengths(wl_step=WL_INCREMENT):
    intervals = [configuration_dictionary[CAVITY1_INDEX]['wavelength'],
                 configuration_dictionary[CAVITY2_INDEX]['wavelength'],
                 configuration_dictionary[CAVITY3_INDEX]['wavelength'],
                 configuration_dictionary[CAVITY4_INDEX]['wavelength']]
    min_wl = min(x[0] for x in intervals)
    max_wl = max(x[1] for x in intervals)
    return numpy.arange(min_wl, max_wl, wl_step).tolist()


if __name__ == '__main__':
    print(get_scanning_wavelengths())
