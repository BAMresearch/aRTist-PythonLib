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
from __future__ import annotations

from .api import transform, save_projection
from scipy.spatial.transform import Rotation
import numpy as np
from pathlib import Path


def circular_trajectory(folder: str | Path, number_of_projections: int = 1000, initial_transform: np.ndarray = np.eye(4), fod: float = 1500, fdd: float = 2000):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    source = np.eye(4)
    detector = np.eye(4)

    source[2, 3] = -fod
    detector[2, 3] = fdd - fod

    angles = np.linspace(0, np.pi * 2, number_of_projections, endpoint=False)
    rotation_matrix = np.eye(4)
    transformation = np.eye(4)

    for i, alpha in enumerate(angles):
        rotation = Rotation.from_euler("Y", alpha)
        rotation_matrix[:3, :3] = rotation.as_matrix()
        transformation = np.dot(rotation_matrix, initial_transform, out=transformation)
        #transformation = rotation_matrix.dot(initial_transform)
        transform("S", transformation.dot(source))
        transform("D", transformation.dot(detector))

        save_projection(folder, i, number_of_projections, fdd=fdd, fod=fod)

        if (i + 1) % 100 == 0:
            print(f"Projection: \t {i + 1} / {number_of_projections}")
