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

import numpy as np
from scipy.spatial.transform import Rotation
from matplotlib import pyplot as plt

from artistlib import API


def generate_trajectory(fod_mm: float, fdd_mm: float, number_of_projections: int) -> tuple[np.ndarray]:
    if fod_mm > fdd_mm:
        raise ValueError('fod > fdd.')

    rotation_angles = np.linspace(-np.pi, np.pi, number_of_projections, endpoint=False)
    rotation_object = Rotation.from_euler('Y', rotation_angles, degrees=False)

    source_initial_position = np.array([0., 0., fod_mm])
    detector_initial_position = np.array([0., 0., fod_mm - fdd_mm])

    source_positions = rotation_object.apply(source_initial_position)
    detector_positions = rotation_object.apply(detector_initial_position)
    
    return zip(source_positions, detector_positions, rotation_angles * 180 / np.pi)

def main():
    trajectory = generate_trajectory(500., 1000., 20)
    api = API()

    for scan_pose in trajectory:
        source, detector, beta_angles = scan_pose
        
        api.translate('S', *source)
        api.translate('D', *detector)
        api.rotate('S', beta=beta_angles)
        api.rotate('D', beta=beta_angles)

        image = api.get_image()
        plt.imshow(image)
        plt.show()

if __name__ == '__main__':
    main()
    