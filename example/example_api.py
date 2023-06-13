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
import sartist
from matplotlib import pyplot as plt


def main():
    # Clear all objects in the scene
    objects = sartist.api.get_part_list_as_id()
    for part in objects:
        sartist.api.delete(part)

    
    # Load a part
    dragon = sartist.api.__aRTistPath__() / "Data" / "Library" / "ExampleParts" / "Fun" / "Dragon.stl"
    dragon_id = sartist.api.load_part(dragon, "dragon", "Al")

    # Move source, detector and rotate object
    fod = 1500
    fdd = 2000
    sartist.api.move("D", x=100, z=(fod-fdd))
    sartist.api.move("S", z=fod)
    sartist.api.rotate(dragon_id, alpha=30, beta=15)
    sartist.api.scale(dragon_id, sx=1.1, sy=1.1, sz=1.1)

    # Show the projection
    image = sartist.api.get_projection()[1]
    plt.imshow(image)
    plt.show()

    # Change the xray parameters
    source = sartist.hardware.ArtistXraySource()
    source.current_in_ma = 250
    source.voltage_in_kv = 50

    detector = sartist.hardware.ArtistDetector()
    detector.exposure = .1

    # Simulate a projection with low voltage
    image_low_voltage = sartist.api.get_projection()[1]

    # And High voltage
    source.voltage_in_kv = 450
    image_high_voltage = sartist.api.get_projection()[1]

    fig, axs = plt.subplots(2, 1)
    axs[0].imshow(image_low_voltage)
    axs[1].imshow(image_high_voltage)
    plt.show()


if __name__ == "__main__":
    main()

