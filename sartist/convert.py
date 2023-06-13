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


import os
import numpy as np
from typing import Tuple
from scipy.spatial.transform import Rotation

from PythonTools.ezrt_header import EzrtHeader, ACQUISITIONGEOMETRY
from PythonTools.py2raw import py2raw
from PIL import Image


def mat_to_artist(transformation_matrix: np.ndarray, euler_convention: str = "zxy") -> Tuple[np.ndarray, np.ndarray]:
    if not transformation_matrix.shape == (4, 4):
        raise ValueError(f"Shape of the transformation martrix has to be (4, 4)."
                         f"It is: {transformation_matrix.shape}")
    elif not transformation_matrix[3, :3].reshape(3).tolist() == [0, 0, 0]:
        raise ValueError(f"A Transformationmatrix of the form:"
                         f"Rotation (3, 3) Transformation (1, 3)"
                         f"Zeros    (3, 1)                [1.0] "
                         f"Is required.")

    """
    R_z * R_x * R_y
    
    [-sin(alpha) * sin(beta) * sin(gamma) + cos(beta) * cos(gamma),     -sin(gamma) * cos(alpha),   sin(alpha) * sin(gamma) * cos(beta) + sin(beta) * cos(gamma)],
    [sin(alpha) * sin(beta) * cos(gamma) + sin(gamma) * cos(beta),      cos(alpha) * cos(gamma),    -sin(alpha) * cos(beta) * cos(gamma) + sin(beta) * sin(gamma)],
    [-sin(beta) * cos(alpha),                                           sin(alpha),                  cos(alpha) * cos(beta)]]

    alpha = arcsin(matrix[3, 2])
    matrix[3, 3] = cos(alpha) * cos(beta) -> beta = arcos(matrix[3, 3] / cos(alpha))
    matrix[1, 2] = -sin(gamma) * cos(alpha) -> gamma = -arcsin(matrix[1, 2] / cos(alpha)
    """

    translation_vektor = transformation_matrix[:, 3]

    rotation = Rotation.from_matrix(transformation_matrix[:3, :3])
    euler_scipy = rotation.as_euler("ZXY", degrees=True)
    euler_scipy = [euler_scipy[1], euler_scipy[2], euler_scipy[0]]

    return euler_scipy, translation_vektor


def artist_to_mat(position: np.ndarray, euler_angles: np.ndarray) -> np.ndarray:
    transformation = np.eye(4)
    R_z = Rotation.from_euler("Z", euler_angles[2], degrees=True).as_matrix()
    R_x = Rotation.from_euler("X", euler_angles[0], degrees=True).as_matrix()
    R_y = Rotation.from_euler("Y", euler_angles[1], degrees=True).as_matrix()

    rotation = R_z
    rotation = rotation.dot(R_x)
    rotation = rotation.dot(R_y)

    transformation[:3, :3] = rotation
    transformation[:3, 3] = position
    return transformation


def fhg_name_generator(core_name: str = "projection", suffix=".raw"):
    """
    Generates a FhG _name for the specified projection number

    :param core_name:
    :param suffix:
    :return:
    """
    def generator(projection_number: int):
        return f"{core_name}_{projection_number:04d}{suffix}"
    return generator


def image_to_fhg(input_path: str, output_folder: str,
                 detector_matrix: np.ndarray, source_matrix: np.ndarray,
                 detector_resolution: np.ndarray, detector_size: np.ndarray,
                 projection_number: int, number_of_projections: int = None,
                 core_name: str = 'projection',
                 name_generator=fhg_name_generator(),
                 fdd: float = None, fod: float = None) -> None:
    """
    Converts an image to a FhG projection.
    Therefore the current aRTist setup is used.

    :param input_path:
    :param output_folder:
    :param detector_matrix:
    :param source_matrix:
    :param detector_resolution:
    :param detector_size:
    :param projection_number:
    :param number_of_projections:
    :param core_name:
    :param name_generator:
    :param fdd:
    :param fod:
    :return:
    """

    if not os.path.exists(output_folder):
        base_path = os.path.split(output_folder)[0]
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

    input_path = os.path.abspath(input_path)
    image = Image.open(input_path)
    array = np.array(image.getdata(), dtype=np.uint16).reshape((image.width, image.height))
    intensity_null = np.max(array)

    # Compute the projection _name / path
    projection_name = name_generator(projection_number)
    projection_path = os.path.join(os.path.abspath(output_folder), projection_name)

    header = _get_header(detector_matrix, source_matrix, detector_resolution, detector_size, number_of_projections, fdd, fod)
    header.inull_value = intensity_null

    py2raw(array, projection_path, input_header=header)


def _get_header(detector_matrix: np.ndarray, source_matrix: np.ndarray,
                detector_resolution: np.ndarray, detector_size: np.ndarray,
                number_of_projections: int = None,
                fdd: float = None, fod: float = None) -> EzrtHeader:

    header = EzrtHeader()

    header.detector_width_in_um = detector_resolution[0] * detector_size[0] 
    header.detector_height_in_um = detector_resolution[1] * detector_size[1]
    header.number_horizontal_pixels = detector_size[0]
    header.number_vertical_pixels = detector_size[1]

    header.agv_source_position = source_matrix[:3, 3].reshape(3)
    header.agv_source_direction = source_matrix[:3, 2]

    header.agv_detector_center_position = detector_matrix[:3, 3].reshape(3)
    header.agv_detector_line_direction = -detector_matrix[:3, 0].reshape(3)
    header.agv_detector_col_direction = detector_matrix[:3, 1].reshape(3)

    header.image_width = detector_size[0]
    header.image_height = detector_size[1]

    header.bit_depth = 16
    header.number_of_images = 1
    header.number_projection_angles = number_of_projections
    header.pixel_width_in_um = detector_resolution[0]


    header.acquisition_geometry = ACQUISITIONGEOMETRY.ARBITRARY

    if fdd is not None:
        header.focus_detector_distance_in_mm = fdd

    if fod is not None:
        header.focus_object_distance_in_mm = fod

    return header
