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

from .remote_connection import Junction, _rc
from .common_types import SAVEMODES

import numpy as np

from scipy.spatial.transform import Rotation
from pathlib import Path
import json


class API():
    def __init__(self, remote_control: Junction = None) -> None:
        if remote_control is None:
            remote_control = _rc
        self.rc = remote_control

    @staticmethod
    def path_to_artist(path: Path) -> str:
        return str(path.absolute()).replace('\\', '\\\\')

    def get_image(self) -> np.ndarray:
        """Make a projection of the current scene.

        Returns:
            np.ndarray: projection as ndarray.
        """
        self.rc.send('set imgList [Engine::Go]')
        self.rc.send('RemoteControl::SendImage [lindex $imgList 0]')
        return self.rc.get_image()
    
    def save_image(self, 
                   save_path: Path, 
                   save_mode: SAVEMODES = SAVEMODES.UINT16, 
                   save_projection_geometry: bool = True):
        """Save the current scene as projection. The projection geometry can be stored in a .json file.

        Args:
            save_path (Path): Save path of the Projection
            save_mode (SAVEMODES, optional): File type of saved projection. Defaults to SAVEMODES.UINT16.
            save_projection_geometry (bool, optional): Projection geometry of the scene. Stem of save_path is used as path. Defaults to True.
        """

        if save_projection_geometry:
            save_path_json = save_path.parent / (save_path.stem + '.json')
            with open(str(save_path_json), 'w') as f:
                json.dump(self.projection_geometry(), f, indent=4)

        if save_mode == SAVEMODES.UINT8:
            self._save_image_uint8(save_path)
        elif save_mode == SAVEMODES.UINT16:
            self._save_image_uint16(save_path)
        elif save_mode == SAVEMODES.FLOAT_TIFF:
            self._save_image_float_tiff(save_path)
        elif save_mode == SAVEMODES.FLOAT_RAW:
            self._save_image_float_raw(save_path)
        elif save_mode == SAVEMODES.PNG:
            self._save_image_png(save_path)
        
    def _save_image_uint16(self, save_path: Path):
        """Saves the current scene as porjection (.tif) and geometry (.json).

        Args:
            save_path (Path): Save path of the projection.
        """
        self.rc.send('set imgList [Engine::Go]')
        save_path_projection = str(save_path.absolute()).replace('\\', '\\\\')
        self.rc.send(f'Image::Save16bit [lindex $imgList 0] {save_path_projection} True')
        self.rc.send('foreach i $imgList {$i Delete}')

    def _save_image_uint8(self, save_path: Path):
        """Saves the current scene as porjection (.tif) and geometry (.json).

        Args:
            save_path (Path): Save path of the projection.
        """
        self.rc.send('set imgList [Engine::Go]')
        save_path_projection = str(save_path.absolute()).replace('\\', '\\\\')
        save_path_json = save_path.parent / (save_path.stem + '.json') # Image::SaveFile [lindex $imgList 0] [file join $env(HOME) Pictures/artistlib2.tif] true',
        self.rc.send(f'Image::Save8bit [lindex $imgList 0] {save_path_projection} True')
        self.rc.send('foreach i $imgList {$i Delete}')

        with open(str(save_path_json), 'w') as f:
            json.dump(self.projection_geometry(), f, indent=4)

    def _save_image_float_tiff(self, save_path: Path):
        """Saves the current scene as porjection (.tiff) and geometry (.json).

        Args:
            save_path (Path): Save path of the projection.
        """
        self.rc.send('set imgList [Engine::Go]')
        save_path_projection = str(save_path.absolute()).replace('\\', '\\\\')
        save_path_json = save_path.parent / (save_path.stem + '.json') # Image::SaveFile [lindex $imgList 0] [file join $env(HOME) Pictures/artistlib2.tif] true',
        self.rc.send(f'Image::SaveFloatTIFF [lindex $imgList 0] {save_path_projection} True')
        self.rc.send('foreach i $imgList {$i Delete}')

        with open(str(save_path_json), 'w') as f:
            json.dump(self.projection_geometry(), f, indent=4)

    def _save_image_float_raw(self, save_path: Path):
        """Saves the current scene as porjection (.raw) and geometry (.json).

        Args:
            save_path (Path): Save path of the projection.
        """
        self.rc.send('set imgList [Engine::Go]')
        save_path_projection = str(save_path.absolute()).replace('\\', '\\\\')
        save_path_json = save_path.parent / (save_path.stem + '.json') # Image::SaveFile [lindex $imgList 0] [file join $env(HOME) Pictures/artistlib2.tif] true',
        self.rc.send(f'Image::SaveFloatRawFile [lindex $imgList 0] {save_path_projection} True')
        self.rc.send('foreach i $imgList {$i Delete}')

        with open(str(save_path_json), 'w') as f:
            json.dump(self.projection_geometry(), f, indent=4)

    def _save_image_png(self, save_path: Path):
        """Saves the current scene as porjection (.png) and geometry (.json).

        Args:
            save_path (Path): Save path of the projection.
        """
        self.rc.send('set imgList [Engine::Go]')
        save_path_projection = str(save_path.absolute()).replace('\\', '\\\\')
        self.rc.send(f'Image::SavePNG [lindex $imgList 0] {save_path_projection} True')
        self.rc.send('foreach i $imgList {$i Delete}')
            
    def translate(self, id: int | str, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        """Moves an object to an absolute position. All values in [mm].

        Args:
            id (int | str): ID of the Object.
            x (float, optional): Absolute X position. Defaults to 0.0.
            y (float, optional): Absolute Y position. Defaults to 0.0.
            z (float, optional): Absolute Z position. Defaults to 0.0.
        """
        self.rc.send(f'::PartList::Invoke {str(id)} SetPosition {str(x)} {str(y)} {str(z)};')
        self.rc.send(f'::PartList::Invoke {str(id)} SetRefPos {str(x)} {str(y)} {str(z)};')

    def rotate(self, id: int | str, alpha: float = 0.0, beta: float = 0.0, gamma: float = 0.0) -> None:
        """Rotates an object to an absolute position. All values in [°].

        Args:
            id (int | str): _description_
            alpha (float, optional): Absolute alpha rotation. Defaults to 0.0.
            beta (float, optional): Absolute beta rotation. Defaults to 0.0.
            gamma (float, optional): Absolute gamma rotation. Defaults to 0.0.
        """
        position = self.get_position(id)
        self.rc.send(f'::PartList::Invoke {str(id)} SetRefPos {str(position[0])} {str(position[1])} {str(position[2])};')
        self.rc.send(f'::PartList::Invoke {str(id)} SetOrientation {str(alpha)} {str(beta)} {str(gamma)};')

    def rotate_from_rotation_matrix(self, id: int | str, rotation_matrix: np.ndarray) -> None:
        """_summary_

        Args:
            id (int | str): ID of the Object.
            rotation_matrix (np.ndarray): _description_
        """
        rotation = Rotation.from_matrix(rotation_matrix)
        euler_scipy = rotation.as_euler("ZXY", degrees=True)
        euler_scipy = [euler_scipy[1], euler_scipy[2], euler_scipy[0]]
        self.rotate(id, *euler_scipy)
    
    def get_position(self, id: int | str) -> np.ndarray:
        result = self.rc.send(f'[::PartList::Get {id} Obj] GetPosition')
        return np.float32(result[1:-1].split(" "))
    
    def get_euler_angles(self, id: int | str) -> np.ndarray:
        result = self.rc.send(f'[::PartList::Get {id} Obj] GetOrientation')
        return np.float32(result[1:-1].split(" "))
    
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
    
    def projection_geometry(self):
        source_position = np.array(self.get_position('S'))
        source_orientation = np.array(self.get_rotation_matrix('S'))
        detector_position = np.array(self.get_position('D'))
        detector_orientation = np.array(self.get_rotation_matrix('D'))

        detector_resolution = self.get_detector_resolution()
        detector_pixel_count = self.get_detector_pixel_count()

        data_dict = dict()
        data_dict['source_position_mm'] = source_position.tolist()
        data_dict['source_orientation_matrix'] = source_orientation.tolist()
        data_dict['detector_position_mm'] = detector_position.tolist()
        data_dict['detector_orientation_matrix'] = detector_orientation.tolist()

        data_dict['detector_count_px'] = detector_pixel_count.tolist()
        data_dict['detector_resolution_mm'] = detector_resolution.tolist()

        return data_dict
    
    def get_detector_resolution(self) -> np.ndarray:
        result = self.rc.send(f'::XDetector::GetResolution')
        return np.array(np.float32(result.split(" ")))

    def get_detector_pixel_count(self) -> np.ndarray:
        result = self.rc.send(f'::XDetector::GetPixelSize')
        return np.array(np.int32(result.split(" ")))
    
    def set_material(self, id: int | str, material: str):
        self.rc.send(f'::PartList::SetMaterial {material} {id}')

    def get_material(self, id: int | str):
        return_value = self.rc.send(f'::PartList::Get {id} Material')

    def load_part(self, load_path: Path, material: str = 'Al', name: str = 'Object') -> int:
        return_value = self.rc.send(f'set obj [::PartList::LoadPart "{self.path_to_artist(load_path)}" "{material}" "{name}"]')
        return int(return_value)
    
    def delete_part(self, id: int | str):
        self.rc.send(f'::PartList::Delete "{id}"')

    def set_visibility(self, id: int | str, visible: bool = True):
        visible = 'on' if visible else 'off'
        self.rc.send(f'[::PartList::Get {id} Obj] SetVisibility "{visible}"')
