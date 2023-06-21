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
    artist = artistlib.ArtistApi()
    object_ids = artist.get_object_ids()
    print(artist.number_of_objects())
    artist.set_material(object_ids[0], 'Al')

if __name__ == '__main__':
    main()