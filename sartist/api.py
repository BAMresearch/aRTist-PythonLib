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



from enum import IntEnum
import os
import time
import json
import socket
import subprocess

import numpy as np
import warnings

from typing import Union, Tuple
from PIL import Image

from .version import __SaRTistTemp__, __send__, __local__
from .convert import mat_to_artist, artist_to_mat, image_to_fhg, fhg_name_generator, _get_header
from .connection import get_data_from_artist, _call_command, __aRTistPath__, __sources__, __detectors__, __aRTistVersion__


def load_part(path_to_part: str, name="Part", material="Al") -> str:
    """
    Loads a mesh into aRTist and set its _name annd material


    :param path_to_part: Path to mesh double "\" required.
    :param name: Optional Name of the part in aRTist
    :param material: Material in aRTist. Default is Fe.
    :return: Object ID as string.
    """
    path_to_part = os.path.abspath(path_to_part).replace("\\", "\\\\")
    command = "SaRTist::LoadPart \"{}\" \"{}\" \"{}\"".format(path_to_part, name, material)
    return get_data_from_artist(command)


def move(id_obj: Union[int, str], x: float = 0.0, y: float = 0.0, z: float = 0.0, verbose=False, relative: bool = False) -> None:
    """
    Moves a Object/Source/Detector to a position x y z.
    Movement can be absolute or relative to its current positio.

    :param id_obj: string or int of the object.
    :param x: position in mm
    :param y: position in mm
    :param z: position in mm
    :param verbose: (bool) print sme informations
    :param relative: (bool) if True: momvement is relativ. default: Absolut (False)
    :return: None
    """
    if relative:
        position = get_position(id_obj)

        x += position[0]
        y += position[1]
        z += position[2]

    command = f"SaRTist::Move {str(id_obj)} {str(x)} {str(y)} {str(z)}"
    get_data_from_artist(command, verbose=verbose)


def transform(obj_id: Union[int, str], transformation_matrix: np.ndarray, verbose=False, relative: bool = False) -> None:
    """
    Takes a 4x4 Transformation matrix, converts it to euler angle and translation and transfomr the specified object

    :param obj_id: Str/Int of the object
    :param transformation_matrix: Transformation Matrix as ndarray
    :param verbose: Print some information (bool)
    :param relative: MOvement relative (True), default value: False
    :return: None
    """
    euler_angle, translation = mat_to_artist(transformation_matrix)
    move(obj_id, x=translation[0], y=translation[1], z=translation[2], verbose=verbose, relative=relative)
    rotate(obj_id, alpha=euler_angle[0], beta=euler_angle[1], gamma=euler_angle[2], verbose=verbose, relative=relative)


def rotate(id_obj: Union[int, str], alpha: float = 0.0, beta: float = 0.0, gamma: float = 0.0, verbose=False, relative: bool = False) -> None:
    """
    Rotates the specified object relative or absolute.

    :param id_obj:
    :param alpha: X-Value of the ZXY-Eulerrotation
    :param beta: Y-Value of the ZXY-Eulerrotation
    :param gamma: Z-Value of the ZXY-Eulerrotation
    :param verbose: Print
    :param relative:
    :return:
    """
    if relative:
        orientation = get_orientation(id_obj)

        alpha += orientation[0]
        beta += orientation[1]
        gamma += orientation[2]

    command = f"SaRTist::Rotate {str(id_obj)} {str(alpha)} {str(beta)} {str(gamma)}"
    get_data_from_artist(command, verbose=verbose)


def scale(id_obj: Union[int, str], s: float=None, sx: float = 1.0, sy: float = 1.0, sz: float = 1.0, verbose=False):
    if s is not None:
        sx, sy, sz = s, s, s
    command = f"SaRTist::Scale {str(id_obj)} {str(sx)} {str(sy)} {str(sz)}"
    get_data_from_artist(command, verbose=verbose)


def delete(id_obj: Union[int, str], verbose=False):
    command = "SaRTist::Delete %s" % id_obj
    get_data_from_artist(command, verbose=verbose)


def set_material(id_obj: Union[int, str], material: str):
    command = "SaRTist::SetMaterial %s \"%s\"" % (id_obj, material)
    _call_command(command)


def load_spectrum(spectrum: Union[str, int]):
    if isinstance(spectrum, int):
        sources_json = os.path.join(
            __sources__(),
            'sources.json')

        with open(sources_json, 'r') as f:
            data = json.load(f)

        if spectrum >= len(data):
            raise ValueError("Spectrums number not in list.")

        spectrum = __sources__() / data[spectrum]

    command = "SaRTist::LoadSpectrum \"%s\"" % os.path.abspath(spectrum).replace("\\", "\\\\")
    _call_command(command)


def get_available_spectras(verbose=False):
    data: list
    sources_json = __sources__() / 'sources.json'

    with open(sources_json, 'r') as f:
        data = json.load(f)

    if verbose:
        for i, source in enumerate(data):
            print(f"{i}:\t {source}")
        print("\n")

    source_dict = dict()
    for i in range(len(data)):
        if data[i].endswith('.xrs'):
            source_name = str(data[i]).split('.')[0]
            source_name = source_name.replace(' ', '')
            source_name = source_name.replace('-', '_')
            source_name = source_name.upper()

            source_dict[source_name] = i

    return IntEnum('Sources', source_dict)


def get_available_detectors(verbose=False):
    detectors_json = __detectors__() / 'detector.json'

    with open(detectors_json, 'r') as f:
        data = json.load(f)

    if verbose:
        for i, detector in enumerate(data):
            print(f"{i}:\t {detector}")
        print("\n")

    detector_dict = dict()
    for i in range(len(data)):
        if data[i].endswith('.aRTdet'):
            detector_name = str(data[i]).split('.')[0]
            detector_name = detector_name.replace(' ', '')
            detector_name = detector_name.replace('-', '_')
            detector_name = detector_name.upper()

            detector_dict[detector_name] = i

    return IntEnum('Detectors', detector_dict)



def load_detector(detector: Union[str, int]):

    if isinstance(detector, int):
        detector_json = __detectors__() / 'detector.json'

        with open(detector_json, 'r') as f:
            data = json.load(f)

        if detector >= len(data):
            raise ValueError("Detector number not in list.")

        detector = __detectors__() / data[detector]

    command = "SaRTist::LoadDetector \"%s\"" % os.path.abspath(detector).replace("\\", "\\\\")
    _call_command(command)


def get_detector_specifiations(verbose=False):
    command = "::XDetector::GetResolution"
    resolution = np.array(get_data_from_artist(command).split(" "), dtype=np.float32)

    command = "::XDetector::GetPixelSize"
    pixels = np.array(get_data_from_artist(command).split(" "), dtype=np.int16)
    return pixels, resolution


def save_image(output_path: str, verbose=False):
    """
    Computes a radilogy and saves the .tiff image.

    :param output_path:
    :param verbose:
    :return:
    """
    output_path = os.path.abspath(output_path)
    
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except WindowsError:
            warnings.warn("Win Error. Start python in admin mode.")

    command = "SaRTist::MakeSnapshot_TIFF \"%s\"" % output_path.replace("\\", "\\\\")
    get_data_from_artist(command, verbose=verbose)

    while not os.path.exists(output_path):
        time.sleep(0.1)


def get_projection(number_of_projections: int = 1, fdd: float = None, fod: float = None, dtype: type = np.uint16, verbose=False) -> Tuple[np.ndarray]:
    """
    Computes a radiology and returns the projection.

    :param number_of_projections:
    :param fdd:
    :param fod:
    :param dtype:
    :param verbose:
    :return:
    """
    temp_name = __SaRTistTemp__ / f"temp_image_{np.random.randint(0, 100)}.tiff"

    save_image(str(temp_name.absolute()))
    image = Image.open(temp_name)
    array = np.array(image.getdata(), dtype=dtype).reshape((image.width, image.height))
    intensity_null = np.max(array)

    detector_matrix = get_transform("D")
    source_matrix = get_transform("S")

    pixels, resolution = get_detector_specifiations()

    header = _get_header(detector_matrix, source_matrix, resolution, pixels, number_of_projections, fdd, fod)
    header.inull_value = intensity_null

    return header, array


def save_projection(folder: str, projection_number: int, number_of_projections: int, base_name: str = None, fdd: float = None, fod: float = None):
    """
    Save a projection as FhG projection.

    :param folder:
    :param projection_number:
    :param number_of_projections:
    :param base_name:
    :param fdd:
    :param fod:
    :return:
    """
    temp_name = __SaRTistTemp__ / "temp_image.tiff"
    save_image(temp_name)

    detector_matrix = get_transform("D")
    source_matrix = get_transform("S")

    pixels, resolution = get_detector_specifiations()

    if base_name is None:
        image_to_fhg(temp_name, folder, detector_matrix, source_matrix, resolution, pixels,
                     projection_number, number_of_projections, fdd=fdd, fod=fod)
    else:
        image_to_fhg(temp_name, folder, detector_matrix, source_matrix, resolution, pixels,
                     projection_number, number_of_projections, fdd=fdd, fod=fod,
                     name_generator=fhg_name_generator(core_name=base_name))


def get_part_list(return_source_and_detector=False):
    part_list = get_data_from_artist("PartList::Query Obj -not-only-selected -with-setup").split(" ")
    part_list = list(part_list)
    if not return_source_and_detector:
        part_list = part_list[2:]
    return part_list


def get_part_list_as_id(return_source_and_detector=False):
    part_list = get_data_from_artist("PartList::Query ID -not-only-selected -with-setup").split(" ")
    part_list = list(part_list)
    if not return_source_and_detector:
        part_list = part_list[2:]
    return part_list


def get_material_list():
    material_list_str = _call_command(
        "SaRTist::SendToPython \"Materials::getall\"",
        get_return=True)
    return string_to_list_with_brackets(material_list_str)


def get_image_names():
    return _call_command("SaRTist::SendToPython \"Engine::Go\"", get_return=True).split(" ")


def get_orientation(obj_id: Union[int, str]):
    command = "[::PartList::Get %s Obj] GetOrientation" % str(obj_id)
    return np.float32(get_data_from_artist(command).split(" "))


def get_position(obj_id: Union[int, str]):
    command = "[::PartList::Get %s Obj] GetPosition" % str(obj_id)
    return np.float32(get_data_from_artist(command).split(" "))


def get_transform(obj_id: Union[int, str]):
    orientation = get_orientation(obj_id)
    position = get_position(obj_id)
    return artist_to_mat(position, orientation)


def string_to_list_with_brackets(string_input: str):
    return_list = list()
    in_bracket = 0

    for letter_loop in range(len(string_input)):
        letter = string_input[letter_loop]
        if letter == " " and in_bracket == 0:
            return_list.append("")
        elif letter_loop == 0:
            if letter == "{":
                in_bracket += 1
            else:
                return_list.append(letter)
        else:
            if letter == "{" and in_bracket == 0:
                in_bracket += 1
            elif letter == "}":
                in_bracket -= 1
                if in_bracket > 0:
                    return_list[-1] = return_list[-1] + letter
            else:
                return_list[-1] = return_list[-1] + letter
                if letter == "{":
                    in_bracket += 1
    return return_list


def is_running():
    """
    Checks if aRTist is running.

    :return: True if aRTist is running.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(__local__)
    try:
        s.connect_ex(__send__)
        _ = s.recv(1024)
        _ = s.recv(1024)
    except socket.error:
        return False
    return True

def generate_flat_field_image(verbose=False):
    command = "XDetector::FFCorrGen"
    _call_command(command, verbose=verbose)


def _start_artist_from_python() -> None:
    """
    Opens aRTist in a new threat.

    :return:
    """
    path_to_exe = os.path.join(
        __aRTistPath__() / "bin64" / "aRTist.exe"
    )
    subprocess.Popen(path_to_exe, creationflags=subprocess.CREATE_NEW_CONSOLE)
