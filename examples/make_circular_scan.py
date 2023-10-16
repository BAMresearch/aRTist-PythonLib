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

import matplotlib.pyplot as plt
from PythonTools.py2raw import py2raw
from PythonTools.ezrt_header import EzrtHeader
from artistlib import API

artist_api = API()
print(artist_api.get_position('S'))
print(artist_api.get_euler_angles('S'))
print(artist_api.get_rotation_matrix('D'))

artist_api.rotate('S', beta=77)

source_matrix = artist_api.get_rotation_matrix('S')
print(source_matrix)

artist_api.rotate_from_rotation_matrix('S', source_matrix)

source_matrix = artist_api.get_rotation_matrix('S')
print(source_matrix)

image = artist_api.get_image()
artist_api.translate('S', 0, -130, 190)

plt.imshow(image)
plt.show()

