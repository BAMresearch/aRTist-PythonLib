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

from ..api import get_data_from_artist


class ArtistFocalSpot:
    def __init__(self):
        self._spot_width = 0.5
        self._spot_height = 0.5
        self._lorentz = 0.0
        self._resolution = 301

    def _pull(self, verbose: bool = False):
        command = "SaRTist::GetSpot"

        if verbose:
            print(command)

        data = get_data_from_artist(command).split("!?")
        names = data[::2]
        values = data[1::2]

        spot = dict()

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

            spot[names[i][:-1]] = value

        self._spot_width = spot["SpotWidth"]
        self._spot_height = spot["SpotHeight"]
        self._lorentz = spot["SpotLorentz"]
        self._resolution = spot["SpotRes"]

    def _push(self, verbose: bool = False):
        command = f"SaRTist::SetSpot {self._spot_width} {self._spot_height} {self._lorentz} {self._resolution}"

        if verbose:
            print(command)

    @property
    def spot_width(self):
        return (3. + 6. * self._lorentz) * self._spot_width / self._resolution

    @spot_width.setter
    def spot_width(self, width: float):
        self._pull()
        self._spot_width = width * self._resolution / (3. + 6. * self._lorentz)
        self._push()

    @property
    def spot_height(self):
        return (3. + 6. * self._lorentz) * self._spot_height / self._resolution

    @spot_height.setter
    def spot_height(self, height: float):
        self._pull()
        self._spot_height = height * self._resolution / (3. + 6. * self._lorentz)
        self._push()

    def set_spot(self, size: float):
        self.spot_width = size
        self.spot_height = size
