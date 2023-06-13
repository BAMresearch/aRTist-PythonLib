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



from ..api import get_part_list_as_id, rotate, move, get_transform
from ..convert import mat_to_artist


class ArtistObjectMover:
    def __init__(self):
        self._part_list = dict()

        self._x = 0.
        self._y = 0.
        self._z = 0.

        self._alpha = 0
        self._beta = 0
        self._gamma = 0

    def get_part_list(self):
        part_list = get_part_list_as_id()

        for part in part_list:

            if self._part_list.get(part, None) is None:
                self._part_list[part] = get_transform(part)

    def transform_absolute(self, x=None, y=None, z=None, alpha=None, beta=None, gamma=None):
        self.get_part_list()

        if x is not None:
            self._x = x

        if y is not None:
            self._y = y

        if z is not None:
            self._z = z

        if alpha is not None:
            self._alpha = alpha

        if beta is not None:
            self._beta = beta

        if gamma is not None:
            self._gamma = gamma

        for part in self._part_list:
            rotate(part, alpha=self._alpha, beta=self._beta, gamma=self._gamma)
            move(part, x=self._x, y=self._y, z=self._z)

    def transform_relativ(self, x=None, y=None, z=None, alpha=None, beta=None, gamma=None):
        self.get_part_list()

        if x is not None:
            self._x = x

        if y is not None:
            self._y = y

        if z is not None:
            self._z = z

        if alpha is not None:
            self._alpha = alpha

        if beta is not None:
            self._beta = beta

        if gamma is not None:
            self._gamma = gamma

        for part in self._part_list:
            euler, translation = mat_to_artist(self._part_list[part])
            rotate(part, alpha=self._alpha + euler[0], beta=self._beta + euler[1], gamma=self._gamma + euler[2])
            move(part, x=self._x + translation[0], y=self._y + translation[1], z=self._z + translation[2])
