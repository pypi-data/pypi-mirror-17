import logging
from pyhomematic.devicetypes.generic import HMDevice
from pyhomematic.devicetypes.misc import HMEvent, Remote
from pyhomematic.devicetypes.helper import (HelperLowBat, HelperSabotage,
                                            HelperBinaryState,
                                            HelperSensorState)

LOG = logging.getLogger(__name__)


class HMSensor(HMDevice):
    pass


class HMBinarySensor(HMDevice):
    pass


class ShutterContact(HMBinarySensor, HelperBinaryState, HelperLowBat, HelperSabotage):
    """Door / Window contact that emits its open/closed state."""
    def is_open(self, channel=1):
        """ Returns True if the contact is open. """
        return self.get_state(channel)

    def is_closed(self, channel=1):
        """ Returns True if the contact is closed. """
        return not self.get_state(channel)


class TiltSensor(HMBinarySensor, HelperBinaryState, HelperLowBat):
    """Sensor that emits its tilted state."""
    def is_tilted(self, channel=1):
        """ Returns True if the contact is tilted. """
        return self.get_state(channel)

    def is_not_tilted(self, channel=1):
        """ Returns True if the contact is not tilted. """
        return not self.get_state(channel)


class RotaryHandleSensor(HMSensor, HelperSensorState, HelperLowBat, HelperSabotage):
    """Window handle contact."""
    def is_open(self, channel=1):
        """ Returns True if the handle is set to open. """
        return self.get_state(channel) == 2

    def is_closed(self, channel=1):
        """ Returns True if the handle is set to closed. """
        return self.get_state(channel) == 0

    def is_tilted(self, channel=1):
        """ Returns True if the handle is set to tilted. """
        return self.get_state(channel) == 1


class CO2Sensor(HMSensor, HelperSensorState):
    """CO2 Sensor"""
    def is_normal(self, channel=1):
        """ Returns True if CO2 state is normal. """
        return self.get_state(channel) == 0

    def is_added(self, channel=1):
        """ Returns True if CO2 state is added. """
        return self.get_state(channel) == 1

    def is_added_strong(self, channel=1):
        """ Returns True if CO2 state is added strong. """
        return self.get_state(channel) == 2


class WaterSensor(HMSensor, HelperSensorState, HelperLowBat):
    """Watter detect sensor."""

    def is_dry(self, channel=1):
        """Return True if the state is DRY"""
        return self.get_state(channel) == 0

    def is_wet(self, channel=1):
        """Return True if the state is WET"""
        return self.get_state(channel) == 1

    def is_water(self, channel=1):
        """Return True if the state is WATER"""
        return self.get_state(channel) == 2


class PowermeterGas(HMSensor):
    """Powermeter for Gas and energy."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.SENSORNODE.update({"GAS_ENERGY_COUNTER": 1,
                                "GAS_POWER": 1,
                                "ENERGY_COUNTER": 1,
                                "POWER": 1})

    def get_gas_counter(self, channel=1):
        """Return gas counter."""
        return float(self.getSensorData("GAS_ENERGY_COUNTER", channel))

    def get_gas_power(self, channel=1):
        """Return gas power."""
        return float(self.getSensorData("GAS_POWER", channel))

    def get_energy(self, channel=1):
        """Return energy counter."""
        return float(self.getSensorData("ENERGY_COUNTER", channel))

    def get_power(self, channel=1):
        """Return power counter."""
        return float(self.getSensorData("POWER", channel))


class Smoke(HMBinarySensor, HelperBinaryState):
    """Smoke alarm."""

    def is_smoke(self, channel=1):
        """ Return True if smoke is detected """
        return self.get_state(channel)


class SmokeV2(Smoke, HelperLowBat):
    """Smoke alarm with Battery."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.ATTRIBUTENODE.update({"ERROR_ALARM_TEST": 'c',
                                   "ERROR_ALARM_TEST": 'c'})


class GongSensor(HMEvent):
    """Wireless Gong Sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.EVENTNODE.update({"PRESS_SHORT": 'c'})


class Motion(HMBinarySensor, HMSensor):
    """Motion detection."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION": 'c'})
        self.SENSORNODE.update({"BRIGHTNESS": 'c'})

    def is_motion(self, channel=1):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def get_brightness(self, channel=1):
        """ Return brightness from 0 (dark ) to 255 (bright) """
        return int(self.getSensorData("BRIGHTNESS", channel))


class MotionV2(Motion, HelperSabotage):
    """Motion detection version 2."""
    pass


class RemoteMotion(Remote, Motion):
    """Motion detection with buttons."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION": 3})
        self.SENSORNODE.update({"BRIGHTNESS": 3})

    @property
    def ELEMENT(self):
        return 2


class LuxSensor(HMSensor):
    """Sensor for messure LUX."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"LUX": 1})

    def get_lux(self, channel=1):
        """Return messure lux."""
        return float(self.getSensorData("LUX", channel))


class ImpulseSensor(HMEvent):
    """Inpulse sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.EVENTNODE.update({"SEQUENCE_OK": 'c'})


class AreaThermostat(HMSensor):
    """Wall mount thermostat."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": 'c', "HUMIDITY": 'c'})

    def get_temperature(self, channel=1):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_humidity(self, channel=1):
        return int(self.getSensorData("HUMIDITY", channel))


class TemperatureSensor(HMSensor):
    """Temperature Sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": 'c'})

    def get_temperature_1(self, channel=1):
        return float(self.getSensorData("TEMPERATURE", channel))


class TemperatureDiffSensor(HMSensor):
    """Temperature difference Sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": 'c'})

    def get_temperature_1(self, channel=1):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_temperature_2(self, channel=2):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_diff(self, channel=3):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_diff_neg(self, channel=4):
        return float(self.getSensorData("TEMPERATURE", channel))


class WeatherSensor(HMSensor, HMBinarySensor):
    """Weather sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": 'c', 
                                "HUMIDITY": 'c',
                                "RAIN_COUNTER": 'c',
                                "WIND_SPEED": 'c',
                                "WIND_DIRECTION": 'c',
                                "WIND_DIRECTION_RANGE": 'c',
                                "SUNSHINEDURATION": 'c',
                                "BRIGHTNESS": 'c'})
        self.BINARYNODE.update({"RAINING": 'c'})

    def get_temperature(self, channel=1):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_humidity(self, channel=1):
        return int(self.getSensorData("HUMIDITY", channel))

    def get_rain_counter(self, channel=1):
        return float(self.getSensorData("RAIN_COUNTER", channel))

    def get_wind_speed(self, channel=1):
        return float(self.getSensorData("WIND_SPEED", channel))

    def get_wind_direction(self, channel=1):
        return int(self.getSensorData("WIND_DIRECTION", channel))

    def get_wind_direction_range(self, channel=1):
        return int(self.getSensorData("WIND_DIRECTION_RANGE", channel))

    def get_sunshineduration(self, channel=1):
        return int(self.getSensorData("SUNSHINEDURATION", channel))

    def get_brightness(self, channel=1):
        return int(self.getSensorData("BRIGHTNESS", channel))

    def is_raining(self, channel=1):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("RAINING", channel))


class WeatherStation(HMSensor):
    """Weather station."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": 'c',
                                "HUMIDITY": 'c',
                                "AIR_PRESSURE": 'c'})

    def get_temperature(self, channel=10):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_humidity(self, channel=10):
        return int(self.getSensorData("HUMIDITY", channel))

    def get_air_pressure(self, channel=10):
        return int(self.getSensorData("AIR_PRESSURE", channel))


DEVICETYPES = {
    "HM-Sec-SC": ShutterContact,
    "HM-Sec-SC-2": ShutterContact,
    "HM-Sec-SCo": ShutterContact,
    "ZEL STG RM FFK": ShutterContact,
    "HM-Sec-RHS": RotaryHandleSensor,
    "ZEL STG RM FDK": RotaryHandleSensor,
    "HM-Sec-RHS-2": RotaryHandleSensor,
    "HM-Sec-xx": RotaryHandleSensor,
    "HM-Sec-WDS": WaterSensor,
    "HM-Sec-WDS-2": WaterSensor,
    "HM-ES-TX-WM": PowermeterGas,
    "HM-Sen-DB-PCB": GongSensor,
    "HM-Sec-SD": Smoke,
    "HM-Sec-SD-Generic": Smoke,
    "HM-Sec-SD-2": SmokeV2,
    "HM-Sec-SD-2-Generic": SmokeV2,
    "HM-Sen-MDIR-WM55": RemoteMotion,
    "HM-Sen-MDIR-SM": Motion,
    "HM-Sen-MDIR-O": Motion,
    "HM-MD": Motion,
    "HM-Sen-MDIR-O-2": Motion,
    "HM-Sec-MDIR-3": MotionV2,
    "HM-Sec-MDIR-2": MotionV2,
    "HM-Sec-MDIR": MotionV2,
    "263 162": MotionV2,
    "HM-Sec-MD": MotionV2,
    "HM-Sen-LI-O": LuxSensor,
    "HM-Sen-EP": ImpulseSensor,
    "HM-Sen-X": ImpulseSensor,
    "ASH550I": AreaThermostat,
    "ASH550": AreaThermostat,
    "HM-WDS10-TH-O": AreaThermostat,
    "HM-WDS20-TH-O": AreaThermostat,
    "HM-WDS40-TH-I": AreaThermostat,
    "HM-WDS40-TH-I-2": AreaThermostat,
    "263 157": AreaThermostat,
    "263 158": AreaThermostat,
    "IS-WDS-TH-OD-S-R3": AreaThermostat,
    "HM-WDS100-C6-O": WeatherSensor,
    "HM-WDS100-C6-O-2": WeatherSensor,
    "KS550": WeatherSensor,
    "KS888": WeatherSensor,
    "KS550Tech": WeatherSensor,
    "KS550LC": WeatherSensor,
    "WS550": WeatherStation,
    "WS888": WeatherStation,
    "WS550Tech": WeatherStation,
    "WS550LCB": WeatherStation,
    "WS550LCW": WeatherStation,
    "HM-WDC7000": WeatherStation,
    "HM-Sec-TiS": TiltSensor,
    "HM-CC-SCD": CO2Sensor,
    "263 160": CO2Sensor,
    "HM-WDS30-OT2-SM": TemperatureDiffSensor,
    "HM-WDS30-OT2-SM-2": TemperatureDiffSensor,
    "HM-WDS30-T-O": TemperatureSensor,
    "S550IA": TemperatureSensor
}
