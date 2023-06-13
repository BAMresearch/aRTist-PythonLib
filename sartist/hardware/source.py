# Copyright 2023 TH DEGGENDORF (contact simon.wittl@th-deg.de)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..api import get_data_from_artist, get_material_list
from warnings import warn


class ArtistXraySource:
    def __init__(self):
        self._max_voltage = 750
        self._tube = "General"
        self._computed = False
        self._transmission = False
        self._voltage = 150
        self._target_thickness = 1
        self._window_thickness = 1
        self._reference_activity = 1.0
        self._resolution = 10
        self._activity_unit = "GBq"
        self._target_angle_in = 21.
        self._window_material = "Al"
        self._max_current = 10.
        self._max_voltage = 450.
        self._max_power = 5000.
        self._exposure_date = "Today"
        self._name = "Python Source"
        self._filter_thickness = 0.0
        self._max_power = 750
        self._exposure = 1.0
        self._half_life = 0.0
        self._reference_date = "Yesterday"
        self._filter_material = "void"
        self._target_angle = 45
        self._target_material = "W"

        self._activity_unit_list = ['mA', 'GBq']
        self._recomended_bins = 20
        self.material_list = get_material_list()

        self._pull()

    def _pull(self, verbose: bool = False):
        command = "SaRTist::GetSpectrum"

        if verbose:
            print(command)

        data = get_data_from_artist(command).split("!?")
        names = data[::2]
        values = data[1::2]

        spectrum = dict()

        for i in range(len(names)):
            try:
                value = float(values[i])
            except ValueError:
                if i == len(names) - 1:
                    value = values[i]
                else:
                    value = values[i][:-1]
                if value == " ":
                    value = 0.0

            spectrum[names[i][:-1]] = value

        self.max_voltage = spectrum["MaxVoltage"] if isinstance(spectrum["MaxVoltage"], float) else self.max_voltage
        self.tube = spectrum["Tube"]
        self.computed = spectrum["computed"]
        self.transmission = spectrum["Transmission"]
        self.voltage = spectrum["Voltage"]
        self.target_thickness = spectrum["TargetThickness"]
        self.reference_activity = spectrum["ReferenceActivity"]
        self.resolution = spectrum["Resolution"]
        self.activity_unit = spectrum["ActivityUnit"]
        self.target_angle_in = spectrum["AngleIn"]
        self.window_material = spectrum["WindowMaterial"]
        self.max_current = spectrum["MaxCurrent"]
        self.exposure_date = spectrum["ExposureDate"]
        self.filter_thickness = spectrum["FilterThickness"]
        self.max_power = spectrum["MaxPower"] if isinstance(spectrum["MaxPower"], float) else self.max_power
        self.exposure = spectrum["Exposure"]
        self.half_life = spectrum["HalfLife"]
        self.reference_date = spectrum["ReferenceDate"]
        self.filter_material = spectrum["FilterMaterial"]
        self.target_angle = spectrum["TargetAngle"]
        self.target_material = spectrum["TargetMaterial"]
        self.window_thickness = spectrum["WindowThickness"]

    def _push(self, verbose: bool = False):
        command = f"SaRTist::SetSpectrum {self._max_voltage} {self._tube} {self._computed} {self._transmission} {self._voltage} " \
                  f"{self._target_thickness} {self._window_thickness} \"{self._reference_activity}\" {self._resolution} {self._activity_unit} " \
                  f"{self._target_angle_in} \"{self._window_material}\" {self._max_current} \"{self._exposure_date}\"  \"{self._name}\" " \
                  f"{self._filter_thickness} {self._max_power} {self._exposure} {self._half_life} \"{self._reference_date}\" " \
                  f"\"{self._filter_material}\" {self._target_angle} \"{self._target_material}\""

        if verbose:
            print(command)

        get_data_from_artist(command)

    @property
    def activity_unit(self):
        return self._activity_unit

    @activity_unit.setter
    def activity_unit(self, unit: str):
        if unit not in self._activity_unit_list:
            raise ValueError(f"activity_unit must be either mA or GBq. It is: {unit}")
        self._activity_unit = unit
        self._push()

    @property
    def current_in_ma(self):
        return self._exposure

    @current_in_ma.setter
    def current_in_ma(self, current):
        if current > self._max_current:
            warn(f"Current is higer then max current {current} / {self._max_current}. Value is set to max current: {self._max_current}")
            current = self._max_current

        self._exposure = current
        self._push()

    def _check_material(self, material):
        if material not in self.material_list:
            raise ValueError(f"Material must be known. The material {material} is not registerd in aRTist.")

    @property
    def filter_material(self):
        return self._filter_material

    @filter_material.setter
    def filter_material(self, material: str):
        self._check_material(material)
        self._filter_material = material
        self._push()

    @property
    def filter_thickness(self):
        return self._filter_thickness

    @filter_thickness.setter
    def filter_thickness(self, thickness: float):
        self._filter_thickness = thickness
        self._push()

    @property
    def max_current(self):
        if isinstance(self._max_current, str):
            self._max_current = 1000.
        return self._max_current

    @max_current.setter
    def max_current(self, current: float):
        if isinstance(current, str):
            pass

        self._max_current = current
        if self.max_power < self.max_current * self.max_voltage:
            self.max_power = self.max_current * self.max_voltage
            warn(f"The set maximum power is set too low. It is adjusted to {self._max_power}W")
        self._push()

    @property
    def max_power(self: float):
        if isinstance(self._max_power, str):
            self._max_power = 1000.
        return self._max_power

    @max_power.setter
    def max_power(self, power: float):
        if isinstance(power, str):
            pass

        self._max_power = power
        if self._max_power < self._max_current * self._max_voltage:
            self._max_power = self._max_current * self._max_voltage
            warn(f"The set maximum power is set too low. It is adjusted to {self._max_power}W")
        self._push()

    @property
    def max_voltage(self):
        if isinstance(self._max_voltage, str):
            self._max_voltage = 450.
        return self._max_voltage

    @max_voltage.setter
    def max_voltage(self, voltage: float):
        if isinstance(voltage, str):
            pass

        self._max_voltage = voltage
        if self._max_power < self._max_current * self._max_voltage:
            self._max_power = self._max_current * self._max_voltage
            warn(f"The set maximum power is set too low. It is adjusted to {self._max_power}W")
        self._push()

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value: float):
        if isinstance(value, str):
            return
        


        self._resolution = value
        bins = self._voltage // self._resolution
        if bins > 128:
            warn(f"Resolution is set to: {bins} bins. Highest number is 128. Resolution is adjusted.")
            self._resolution = self._voltage / 128 + 1
        elif bins < self._recomended_bins:
            warn(f"The resolutions is adjusted that the number of bins fits {self._recomended_bins}")
            self._resolution = int(self._voltage // self._recomended_bins)
        self._push()

    @property
    def transmission(self):
        return bool(self._transmission)

    @transmission.setter
    def transmission(self, value: bool):
        self._transmission = float(value)
        self._push()

    @property
    def voltage_in_kv(self):
        return self._voltage

    @voltage_in_kv.setter
    def voltage_in_kv(self, voltage: float):
        
        if self._voltage > self._max_voltage:
            warn(f"The specified voltage of {voltage}kv is to high. It is set to the maximum voltage of {self._max_voltage}kV")
            self._voltage = self._max_voltage
        else:
            self._voltage = voltage

        bins = int(self._voltage) / int(self._resolution)
        if bins > 128:
            self.resolution = self._voltage // 128 + 1
            warn(f"Resolution is adjusted to 128 bins.")
        elif bins < self._recomended_bins:
            warn(f"The resolutions is adjusted that the number of bins fits {self._recomended_bins}")
            self.resolution = self._voltage / self._recomended_bins

        self._push()
