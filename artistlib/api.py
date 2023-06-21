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

from .connection import Connection
from .common_types import SolidModelTypes, SendTypes

from pathlib import Path


class ArtistApi:
    def __init__(self, connection: Connection = Connection()) -> None:
        self.connection = connection

    def open_scene(self, scene_path: str | Path) -> None:
        if isinstance(scene_path, str):
            scene_path = Path(scene_path)
        scene_path = scene_path.absolute()
        command =  [f'FileIO::OpenAny {scene_path}']
        self.connection.send(command)

    def get_object_ids(self) -> list[int]:
        command = "PartList::Query ID;\n"
        result = self.connection.send(command, SendTypes.RESULT)[0]
        return self.connection.string_to_list(result, int)
    
    def clear_objects(self) -> None:
        command = 'PartList::Clear;'
        self.connection.send(command, SendTypes.RESULT)

    def number_of_objects(self) -> int:
        command = '::PartList::Count;\n'
        return int(self.connection.send(command, SendTypes.RESULT)[0])
    
    def set_material(self, object_id: str | int, material: str):
        command =  f'::PartList::Set {str(object_id)} Material {material}'
        self.connection.send(command, SendTypes.RESULT)

    

