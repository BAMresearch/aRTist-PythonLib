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

from .remote_connection import Junction

import numpy as np
from scipy.spatial.transform import Rotation


class API():
    def __init__(self, remote_control: Junction = Junction()) -> None:
        self.rc = remote_control

    def get_image(self) -> np.ndarray:
        self.rc.send('set imgList [Engine::Go]')
        self.rc.send('RemoteControl::SendImage [lindex $imgList 0]')
        return self.rc.get_image()
    
    def translate(self, id: int | str, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.rc.send(f'::PartList::Invoke {str(id)} SetPosition {str(x)} {str(y)} {str(z)};')
        self.rc.send(f'::PartList::Invoke {str(id)} SetRefPos {str(x)} {str(y)} {str(z)};')

    def rotate(self, id: int | str, alpha: float = 0.0, beta: float = 0.0, gamma: float = 0.0) -> None:
        position = self.get_position(id)
        self.rc.send(f'::PartList::Invoke {str(id)} SetRefPos {str(position[0])} {str(position[1])} {str(position[2])};')
        self.rc.send(f'::PartList::Invoke {str(id)} SetOrientation {str(alpha)} {str(beta)} {str(gamma)};')

    def rotate_from_rotation_matrix(self, id: int | str, rotation_matrix: np.ndarray) -> None:
        rotation = Rotation.from_matrix(rotation_matrix)
        euler_scipy = rotation.as_euler("ZXY", degrees=True)
        euler_scipy = [euler_scipy[1], euler_scipy[2], euler_scipy[0]]
        self.rotate(id, *euler_scipy)
    
    def get_position(self, id: int | str) -> np.ndarray:
        result = self.rc.send(f'[::PartList::Get {id} Obj] GetPosition')
        return np.float32(result[1:-2].split(" "))
    
    def get_euler_angles(self, id: int | str) -> np.ndarray:
        result = self.rc.send(f'[::PartList::Get {id} Obj] GetOrientation')
        return np.float32(result[1:-2].split(" "))
    
    def get_rotation_matrix(self, id: int | str) -> np.ndarray:
        euler_angles = self.get_euler_angles(id)

        R_x = Rotation.from_euler("X", euler_angles[0], degrees=True).as_matrix()
        R_y = Rotation.from_euler("Y", euler_angles[1], degrees=True).as_matrix()
        R_z = Rotation.from_euler("Z", euler_angles[2], degrees=True).as_matrix()

        rotation = R_z
        rotation = rotation.dot(R_x)
        rotation = rotation.dot(R_y)

        return rotation
    
    def get_orientation(self, id) -> np.ndarray:
        rotation = Rotation.from_matrix(self.get_rotation_matrix(id))
        return rotation.as_quat()
