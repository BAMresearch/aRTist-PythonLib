# Copyright 2023 Simon Wittl (Deggendorf Institute of Technology)
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
from __future__ import annotations

from ..connection import Connection
from ..api import ArtistApi
from ..common_types import SendTypes


class ArtistXraySource:
    """Wrapper for the aRTist xray source
    """
    def __init__(self, connection: Connection | ArtistApi) -> None:
        """aRTist xray source.

        Args:
            connection (Connection | ArtistApi): Connection to aRTist. Note you should only use one connection for your python script. 
        """

        if isinstance(connection, ArtistApi):
            connection = connection.connection

        self.connection = connection

    @property
    def voltage_kv(self) -> float:
        command = 'array get Xsource Voltage;\n'
        return_value = self.connection.send(command, SendTypes.RESULT)[0]
        return_value = return_value.split(' ')[1]
        return float(return_value)
    
    @voltage_kv.setter
    def voltage_kv(self, voltage_kv: float) -> None:
        commands = [f'set ::Xsource(Voltage) {voltage_kv};'
                    '::XSource::ComputeSpectrum;']
        self.connection.send(commands)

    @property
    def exposure_ma(self):
        ...