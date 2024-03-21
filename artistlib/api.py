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
        save_path = save_path.resolve()
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

    def scale(self, id: int | str, x: float = 1.0) -> None:
        """Moves an object to an absolute position. All values in [mm].

        Args:
            id (int | str): ID of the Object.
            x (float, optional): Absolute X position. Defaults to 0.0.
            y (float, optional): Absolute Y position. Defaults to 0.0.
            z (float, optional): Absolute Z position. Defaults to 0.0.
        """
        self.rc.send(f'::PartList::Invoke {str(id)} SetScale {str(x)} {str(x)} {str(x)};')

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
        """Rotates an object to an absolute position.

        Args:
            id (int | str): ID of the Object.
            rotation_matrix (np.ndarray): Rotationmatix in world coordinate system.
        """
        rotation = Rotation.from_matrix(rotation_matrix)
        euler_scipy = rotation.as_euler("ZXY", degrees=True)
        euler_scipy = [euler_scipy[1], euler_scipy[2], euler_scipy[0]]
        self.rotate(id, *euler_scipy)
    
    def get_position(self, id: int | str) -> np.ndarray:
        """Returns the current position of the object in [mm].

        Args:
            id (int | str): ID of the Object.

        Returns:
            np.ndarray: position (x,y,z) in [mm].
        """
        result = self.rc.send(f'[::PartList::Get {id} Obj] GetPosition')
        return np.float32(result[1:-1].split(" "))
    
    def get_euler_angles(self, id: int | str) -> np.ndarray:
        """Returns the current orientation of the object as euler angles in the ZXY convention.

        Args:
            id (int | str): ID of the Object.


        Returns:
            np.ndarray: Euler angle in ZXY convention.
        """
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
        """Return the current orientation of the object as quarternion.

        Args:
            id (int | str): ID of the Object.

        Returns:
            np.ndarray: Quarternion of the object in the wolrd coordinate system.
        """
        rotation = Rotation.from_matrix(self.get_rotation_matrix(id))
        return rotation.as_quat()
    
    def projection_geometry(self) -> dict:
        """Returns the current projection geometry of the scene. All positions are in [mm].

        Returns:
            dict: Dictionary of the projection geometry. Keys are: 'focal_spot_position_mm', 
            'focal_spot_orientation_matrix', 'detector_center_position_mm', 
            'detector_center_orientation_matrix', 'detector_center_orientation_quat',
            'detector_count_px' and 'detector_resolution_mm'
        """
        source_position = np.array(self.get_position('S'))
        source_orientation = np.array(self.get_rotation_matrix('S'))
        detector_position = np.array(self.get_position('D'))
        detector_orientation = np.array(self.get_rotation_matrix('D'))

        detector_resolution = self.get_detector_resolution()
        detector_pixel_count = self.get_detector_pixel_count()

        data_dict = dict()
        data_dict['focal_spot_position_mm'] = source_position.tolist()
        data_dict['focal_spot_orientation_matrix'] = source_orientation.tolist()
        data_dict['detector_center_position_mm'] = detector_position.tolist()
        data_dict['detector_center_orientation_matrix'] = detector_orientation.tolist()
        data_dict['detector_center_orientation_quat'] = Rotation.from_matrix(detector_orientation).as_quat().tolist()

        data_dict['detector_count_px'] = detector_pixel_count.tolist()
        data_dict['pixel_pitch_mm'] = detector_resolution.tolist()

        return data_dict
    
    def get_detector_resolution(self) -> np.ndarray:
        """Returns the current pixel pitch of the detector as array

        Returns:
            np.ndarray: Pixel pitch of the detector (u, v).
        """
        result = self.rc.send(f'::XDetector::GetResolution')
        return np.array(np.float32(result.split(" ")))

    def get_detector_pixel_count(self) -> np.ndarray:
        """Returns the current pixel count of the detector.

        Returns:
            np.ndarray: Pixel count (u, v).
        """
        result = self.rc.send(f'::XDetector::GetPixelSize')
        return np.array(np.int32(result.split(" ")))
    
    def set_material(self, id: int | str, material: str):
        """Changes the material of the object.

        Args:
            id (int | str): ID of the Object.
            material (str): Matiral as string. !!!Must be in the material database of artist!!!
        """
        self.rc.send(f'::PartList::SetMaterial {material} {id}')

    def get_material(self, id: int | str):
        """Returns the material of the object.

        Args:
            id (int | str): ID of the Object.
        """
        return_value = self.rc.send(f'::PartList::Get {id} Material')
        return return_value

    def load_part(self, load_path: Path, material: str = 'Al', name: str = 'Object') -> int:
        """Loads a mesh file into the artist scene. Returns the object id for further mainpulations.

        Args:
            load_path (Path): Path object pointing to the mesh file.
            material (str, optional): Material of the mesh file. Defaults to 'Al'.
            name (str, optional): Displayed name in the aRTist GUI. Defaults to 'Object'.

        Returns:
            int: Object ID for further Manipulations.
        """
        return_value = self.rc.send(f'set obj [::PartList::LoadPart "{self.path_to_artist(load_path)}" "{material}" "{name}"]')
        return int(return_value)
    
    def delete_part(self, id: int | str):
        """Delets the object from the scene.

        Args:
            id (int | str): ID of the Object.
        """
        self.rc.send(f'::PartList::Delete "{id}"')

    def set_visibility(self, id: int | str, visible: bool = True):
        """Sets the Object in/visiible.

        Args:
            id (int | str): ID of the Object.
            visible (bool, optional): Visible: True. Defaults to True.
        """
        visible = 'on' if visible else 'off'
        self.rc.send(f'[::PartList::Get {id} Obj] SetVisibility "{visible}"')

    def clear_scene(self):
        """Clears all objects from the scene.
        """
        self.rc.send('::PartList::Clear')

