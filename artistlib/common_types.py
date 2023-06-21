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
from enum import IntEnum


class SendTypes:
    RESULT = 'RESULT'
    TIME_OUT = 'timed out'
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    ALL = '*'

class SolidModelTypes(IntEnum):
    CUBOID = 0
    ELLIPSSOID = 1
    CYLINDER = 2
    TUBE = 3
    CONE = 4
    TEXT = 5
    WEDGE = 6
    STEP_WEDGE = 7


class CommandTypes(IntEnum):
    CONNECTION = 0
    SEND = 1