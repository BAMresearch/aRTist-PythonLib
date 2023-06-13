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


from shutil import copy2 as copyfile
from .version import __SaRTistTCL__, __SaRTistPath__
from .connection import __detectors__, __sources__
import json


def update_artist_data():
    input("START aRTist abd PYTHON must be in admin mode to copy data ...\n[ENTER]")
    
    path_to_repo_detectors = __SaRTistPath__ / "data" / "detectors"
    path_to_repo_sources = __SaRTistPath__ / "data" / "tubes"
    detectors = __detectors__()
    sources = __sources__()

    for detector in path_to_repo_detectors.glob('*.aRTdet'):
        detector_path = path_to_repo_detectors / detector.name
        detector_path_new = detectors / detector.name

        copyfile(detector_path, detector_path_new)

    for source in path_to_repo_sources.glob('*.xrs'):
        sources_path = path_to_repo_sources / source.name

        source_path_new = sources / source.name

        copyfile(sources_path, source_path_new)

    detectors_in_bam = __detectors__().glob('*')
    sources_in_bam =__sources__().glob('*')

    detector_json = __detectors__() / 'detector.json'
    sources_json = __sources__() / 'sources.json'

    data = list()

    for detector in detectors_in_bam:
        if detector not in data:
            data.append(str(detector.name))

    with open(detector_json, 'w') as f:
        json.dump(data, f)

    data = list()

    for source in sources_in_bam:
        if source not in data:
            data.append(str(source.name))

    with open(sources_json, 'w') as f:
        json.dump(data, f)




def install():
    # Copies all detectors and sources to aRTist ...
    update_artist_data()
