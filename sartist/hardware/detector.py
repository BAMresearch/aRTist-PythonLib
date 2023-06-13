from ..api import get_data_from_artist, get_projection, get_detector_specifiations, generate_flat_field_image
from warnings import warn
from typing import Union


class ArtistDetector:
    def __init__(self):
        self._unsharpness = 0.001
        self._unsharpness_default_value = 0.001
        self._long_range_unsharpness = 0.0
        self._long_range_ratio = 0.01
        self._exposure = 1.
        self._auto_d_pos_x = None
        self._auto_d_pos_y = None
        self._type = "Flatpanel"
        self._noise = 0.0
        self._scan_mode = False

        self._flat_field_correction = True
        self._flat_field_corrections_auto = True
        self._flat_field_correction_scale = 0.1

        self._refference_gv = 50000
        self._number_of_frames = 1
        self._auto_detector = "max"

        self.detector_list = list()
        self.get_availabe_detectors()

        pixels, resolution = get_detector_specifiations()

        self.pixel_count_x = pixels[0]
        self.pixel_count_y = pixels[1]

        self.pixel_width_x = resolution[0]
        self.pixel_width_y = resolution[1]

        self._pull()

    def get_availabe_detectors(self):
        detecors_string = get_data_from_artist("XDetector::getall")
        detecors_string = detecors_string.replace("1:1 ", "")
        self.detector_list = detecors_string.split("} {")

        self.detector_list[0] = self.detector_list[0][1:]
        self.detector_list[-1] = self.detector_list[-1][:-1]
        self.detector_list.append("1:1")

    def _pull(self, verbose: bool = False):
        command = "SaRTist::GetDetector"

        if verbose:
            print(command)

        data = get_data_from_artist(command).split("!?")
        names = data[::2]
        values = data[1::2]

        detector = dict()

        for i in range(len(names)):
            try:
                value = float(values[i])
            except ValueError:
                if i == len(names) - 1:
                    value = values[i]
                else:
                    value = values[i][:-1]
                if value == " ":
                    value = 0.0

            detector[names[i][:-1]] = value

        if detector['NoiseFactorOn'] == 1:
            self._noise = detector['NoiseFactor']
        else:
            self._noise = False

        if detector['UnsharpnessOn'] == 0:
            self._unsharpness = False
        else:
            self._unsharpness = detector['Unshapness']

        self._exposure = detector['Scale']
        self._type = detector['Type']
        self._scan_mode = detector['ScanMode']
        self._long_range_unsharpness = detector['LRUnsharpness']
        self._long_range_ratio = detector['LRRatio']
        self._flat_field_corrections_auto = detector['FFCorrAutoScale']
        self._flat_field_correction = detector['FFCorrRun']
        self._auto_d_pos_x = detector['AutoDPosX']
        self._auto_d_pos_y = detector['AutoDPosY']
        self._auto_detector = detector['AutoD']
        self._number_of_frames = detector['NrOfFrames']
        self._refference_gv = detector['RefGV']

    def _push(self, verbose: bool = False):
        if isinstance(self._noise, float):
            noise_factor_on = 1
            noise_factor = self._noise
        else:
            noise_factor_on = 0
            noise_factor = 0.001

        if isinstance(self._unsharpness, float):
            unsharpness_on = 1
            unsharpness = self._unsharpness
        else:
            unsharpness_on = 0
            unsharpness = 0.001

        command = f"SaRTist::SetDetector {self._long_range_unsharpness} {self._exposure} {self._auto_d_pos_y} {self._auto_d_pos_x} " \
                  f"\"{self._type}\" {noise_factor_on} \"{self._scan_mode}\" {unsharpness} {self._flat_field_corrections_auto} " \
                  f"{self._flat_field_correction} {unsharpness_on} {self._flat_field_correction_scale} {self._refference_gv} " \
                  f"{self._number_of_frames} {self._long_range_ratio} \"{self._auto_detector}\" {noise_factor}"

        if verbose:
            print(command)

        get_data_from_artist(command)

    @property
    def unsharpness(self):
        return float(self._unsharpness)

    @unsharpness.setter
    def unsharpness(self, value: Union[bool, float] = 0.001):
        value = float(value)
        if value < 0 or value >= 0:
            warn(f"A value between [0, 1] is expected. Set it to defaultvalue {self._unsharpness_default_value}.")
        elif value == 0.:
            value = False

        self._unsharpness = value
        self._push()

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, time):
        self._exposure = time
        self._push()

    @staticmethod
    def get_projection():
        return get_projection()[1]

    @property
    def noise(self):
        return self._noise

    @noise.setter
    def noise(self, value):
        self._noise = value
        self._push()


    @property
    def auto_detector(self):
        return self._auto_detector

    @auto_detector.setter
    def auto_detector(self, value):
        self._auto_detector = value
        self._push()


    @property
    def flat_field_correction(self):
        return self._flat_field_correction

    @flat_field_correction.setter
    def flat_field_correction(self, value):
        self._flat_field_correction = value
        self._push()
        generate_flat_field_image()
        return self._flat_field_correction


    @property
    def detector_type(self):
        return self._type

    @detector_type.setter
    def detector_type(self, value):
        self._type = value
        self._push()

    