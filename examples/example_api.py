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

import artistlib

def main():
    ### Test Connection() class
    connection = artistlib.Connection()
    ver = connection.send(['::aRTist::GetVersion;\n'])
    cmd = f'puts "aRTist {ver} remote controlled by >>>example.py<<<."\n'
    connection.send(cmd)
    print('Some text written to aRTist\'s console.')


    ### Test API
    artist = artistlib.ArtistApi()  # Create handle
    object_ids = artist.get_object_ids()  # Get list of all object ids of aRTist
    print(artist.number_of_objects)  # print the number of objects
    artist.set_material(object_ids[0], 'Al')  # Change the material of an object.

    ### Hardware components as python class

    xray_source = artistlib.hardware.ArtistXraySource(artist)  # Create a hardware object of the xray source, the same connection object is used. 
    current_voltage = xray_source.voltage_kv  # Wrap the properties of the aRTist xray source as properties of a python class
    print(f'Current voltage in aRTist: {current_voltage}') 

    xray_source.voltage_kv = 20.  # Wrap the python setter
    changed_voltage = xray_source.voltage_kv
    print(f'Changed voltage in aRTist: {changed_voltage}')


if __name__ == '__main__':
    main()