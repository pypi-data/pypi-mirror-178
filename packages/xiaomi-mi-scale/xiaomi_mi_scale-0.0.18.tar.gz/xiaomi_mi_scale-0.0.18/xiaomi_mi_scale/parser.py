"""Parser for Xiaomi Mi Scale advertisements.
This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/oral_b.py
MIT License applies.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum, auto
import binascii

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data.enum import StrEnum

_LOGGER = logging.getLogger(__name__)


class MiScaleSensor(StrEnum):

    WEIGHT = "weight"
    IMPEDANCE = "impedance"
    SIGNAL_STRENGTH = "signal_strength"


OLD_MEASURE = None

class Models(Enum):

    MiScaleV1 = auto()
    MiScaleV2 = auto()


UNIT_TYPES = {
    1: "jin",
    2: "kg",
    3: "lb",
}


@dataclass
class ModelDescription:
    device_type: str
    unit_type: dict[int, str]


DEVICE_TYPES = {
    Models.MiScaleV1: ModelDescription(
        device_type="Mi Body Fat Scale",
        unit_type=UNIT_TYPES,
        ),
    Models.MiScaleV2: ModelDescription(
        device_type="Mi Body Composition Scale",
        unit_type=UNIT_TYPES,
        ),
}



class MiScaleBluetoothDeviceData(BluetoothData):
    """Data for Xiaomi Mi Scale sensors."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        global OLD_MEASURE
        """Update from BLE advertisement data."""
        manufacturer_data = service_info.manufacturer_data
        address = service_info.address
        #service_data = service_info.service_data


        if "0000181b-0000-1000-8000-00805f9b34fb" in list(service_info.service_data.keys()):
            ### Xiaomi V2 Scale ###
            data = binascii.b2a_hex(service_info.service_data['0000181b-0000-1000-8000-00805f9b34fb']).decode('ascii')
            logging.debug(f"miscale v2 with advertising_data: {service_info}")
            self.set_device_manufacturer("Xiaomi")
            model_info = DEVICE_TYPES[Models.MiScaleV2]
            self.set_device_type(model_info.device_type)
            name = f"{model_info.device_type} {short_address(address)}"
            self.set_device_name(name)
            self.set_title(name)
            data2 = bytes.fromhex(data)
            ctrlByte1 = data2[1]
            isStabilized = ctrlByte1 & (1<<5)
            WeightRemoved = ctrlByte & (1 << 7)
            hasImpedance = ctrlByte1 & (1<<1)
            measunit = data[0:2]
            measured = int((data[24:26] + data[22:24]), 16) * 0.01
            #unit = UNIT_TYPES[int(data[0:2])]
            unit = ''
            if measunit == "03": unit = 'lbs'
            if measunit == "02": unit = 'kg' ; measured = measured / 2
            miimpedance = str(int((data[20:22] + data[18:20]), 16))
            if unit and isStabilized:
                if OLD_MEASURE != round(measured, 2) + int(miimpedance):
                    OLD_MEASURE = round(measured, 2) + int(miimpedance)
                    #MQTT_publish(round(measured, 2), unit, str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')), hasImpedance, miimpedance)
                    self.update_sensor(str(MiScaleSensor.WEIGHT), None, measured, None, "Weight")
                    self.update_sensor(str(MiScaleSensor.IMPEDANCE), None, miimpedance, None, "Impedance")
        elif "0000181d-0000-1000-8000-00805f9b34fb" in list(service_info.service_data.keys()):
            ### Xiaomi V1 Scale ###
            data = binascii.b2a_hex(service_info.service_data['0000181d-0000-1000-8000-00805f9b34fb']).decode('ascii')
            logging.debug(f"miscale v1 found with advertising_data: {service_info}")
            self.set_device_manufacturer("Xiaomi")
            model_info = DEVICE_TYPES[Models.MiScaleV1]
            self.set_device_type(model_info.device_type)
            name = f"{model_info.device_type} {short_address(address)}"
            self.set_device_name(name)
            self.set_title(name)
            data2 = bytes.fromhex(data)
            ctrlByte1 = data2[1]
            isStabilized = ctrlByte1 & (1<<5)
            WeightRemoved = ctrlByte & (1 << 7)
            measunit = data[0:2]
            measured = int((data[4:6] + data[2:4]), 16) * 0.01
            unit = ''
            if measunit.startswith(('03', 'a3')): unit = 'lbs'
            if measunit.startswith(('12', 'b2')): unit = 'jin'
            if measunit.startswith(('22', 'a2')): unit = 'kg' ; measured = measured / 2
            if unit and isStabilized:
                if OLD_MEASURE != round(measured, 2):
                    OLD_MEASURE = round(measured, 2)
                    #MQTT_publish(round(measured, 2), unit, str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')), "", "")
                    self.update_sensor(str(MiScaleSensor.WEIGHT), None, measured, None, "Weight")
        else
            return None
