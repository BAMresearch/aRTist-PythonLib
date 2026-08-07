from .artist_send import ArtistSend
from .artist_setup import ArtistSetup
from .artist_project import ArtistProject
from .artist_detector import ArtistDetector
from .artist_source import ArtistSource

from .start.artist_start import start_artist

# from functools import wraps


class ArtistAll(ArtistSend):
    """A wrapper class that provides access to all available classes and offers autocomplete support."""

    def __init__(
        self,
        path_specific_version=None,
        start_UI: bool = True,
        batch: bool = None,
        multiple_starts=False,
        host="localhost",
        port=3658,
        bufferSize=1024,
        timeout=5,
    ):

        self.start = start_artist(
            path_specific_version=path_specific_version,
            start_UI=start_UI,
            port=port,
            multiple_starts=multiple_starts,
        )
        super().__init__(
            batch=batch, host=host, port=port, bufferSize=bufferSize, timeout=timeout
        )
        self.project = ArtistProject()
        self.detector = ArtistDetector()
        self.setup = ArtistSetup()
        self.source = ArtistSource()

    # @wraps(ArtistProject.load_save_project,assigned=("__doc__",),updated=())
    def load_save_project(
        self, project_path: str, save_img_to: str, img_name: str
    ) -> str:
        return self.project.load_save_project(project_path, save_img_to, img_name)

    def load_project(self, path_to_project: str) -> str:
        return self.project.load_project(path_to_project)

    def run_project(self) -> str:
        return self.project.run_project()

    def save_img_project(self, path_save_img: str, img_name: str) -> str:
        return self.project.save_img_project(path_save_img, img_name)

    def get_part_global(self, ID: int) -> str:
        return self.setup.get_part_global(ID)

    def part_position_global(
        self, ID: int, x: float = None, y: float = None, z: float = None
    ) -> str:
        return self.setup.part_position_global(ID, x, y, z)

    def get_part_ref(self, ID: int) -> tuple[float, float, float]:
        return self.setup.get_part_ref(ID)

    def part_position_ref(
        self, ID: int, x: float = None, y: float = None, z: float = None
    ) -> str:
        return self.setup.part_position_ref(ID, x, y, z)

    def get_part_orientation(self, ID: int) -> tuple[float, float, float]:
        return self.setup.get_part_orientation(ID)

    def part_orientation(
        self, ID: int, angleX: float = None, angleY: float = None, angleZ: float = None
    ) -> str:
        return self.setup.part_orientation(ID, angleX, angleY, angleZ)

    def part_rotate(
        self,
        ID: int,
        system: str,
        alpha: float,
        axisX: float,
        axisY: float,
        axisZ: float,
    ) -> str:
        return self.setup.part_rotate(ID, system, alpha, axisX, axisY, axisZ)

    def part_rotate_center(
        self,
        ID: int,
        alpha: float,
        x: float,
        y: float,
        z: float,
        Cx: float,
        Cy: float,
        Cz: float,
    ) -> str:
        return self.setup.part_rotate_center(ID, alpha, x, y, z, Cx, Cy, Cz)

    def part_material(self, ID: int, Material: str) -> str:
        return self.setup.part_material(ID, Material)

    def get_detector(self) -> tuple[float, float, float]:
        return self.setup.get_detector()

    def get_source(self) -> tuple[float, float, float]:
        return self.setup.get_source()

    def source_position(self, x: float = None, y: float = None, z: float = None) -> str:
        return self.setup.source_position(x, y, z)

    def detector_position(
        self, x: float = None, y: float = None, z: float = None
    ) -> str:
        return self.setup.detector_position(x, y, z)

    def get_source_orientation(self) -> tuple[float, float, float]:
        return self.setup.get_source_orientation()

    def source_orientation(
        self, x: float = None, y: float = None, z: float = None
    ) -> str:
        return self.setup.source_orientation(x, y, z)

    def get_detector_orientation(self):
        return self.setup.get_detector_orientation()

    def detector_orientation(self, x: float = None, y: float = None, z: float = None):
        return self.setup.detector_orientation(x, y, z)

    def detector_geo(
        self,
        size: float = None,
        pixel: float = None,
        res: float = None,
        sizeX: float = None,
        sizeY: float = None,
        pixelX: float = None,
        pixelY: float = None,
        resX: float = None,
        resY: float = None,
    ):
        return self.detector.detector_geo(
            size, pixel, res, sizeX, sizeY, pixelX, pixelY, resX, resY
        )

    def load_spectra(self, path: str):
        return self.source.load_spectra(path)

    def set_spectra(
        self,
        Tube: str = None,
        V: float = None,
        TMaterial: str = None,
        TAngle: float = None,
        TThick: float = None,
        FMaterial: str = None,
        FThick: float = None,
        F2Material: str = None,
        F2Thick: float = None,
        F3Material: str = None,
        F3Thick: float = None,
        WMaterial: str = None,
        WThick: float = None,
        Angle: float = None,
        Transmission: float = None,
        res: float = None,
    ):
        return self.source.set_spectra(
            Tube,
            V,
            TMaterial,
            TAngle,
            TThick,
            FMaterial,
            FThick,
            F2Material,
            F2Thick,
            F3Material,
            F3Thick,
            WMaterial,
            WThick,
            Angle,
            Transmission,
            res,
        )

    def cal_spectra(
        self, spec_name: str = None, dest_path: str = None, reduce_number_bins=False
    ):
        return self.source.cal_spectra(spec_name, dest_path, reduce_number_bins)

    def load_tube(self, path_dict: str, spec_name: str, path_dest: str):
        return self.source.load_tube(path_dict, spec_name, path_dest)

    def set_exposure(self, exposure: float):
        return self.source.set_exposure(exposure)

    def delete_part(self, ID: int):
        return self.setup.delete_part(ID)

    def clear_project(self):
        return self.project.clear_project()

    def save_project(self):
        return self.project.save_project()

    def get_part_material(self, ID: int):
        return self.setup.get_part_material(ID)

    def get_detector_pixel_count(self):
        return self.detector.get_detector_pixel_count()

    def get_detector_res(self):
        return self.detector.get_detector_res()

    def get_detector_size(self):
        return self.detector.get_detector_size()

    def get_size(self, ID: int):
        return self.setup.get_size(ID)

    def set_size(self, ID: int, x: float, y: float, z: float):
        return self.setup.set_size(ID, x, y, z)

    def get_spectra(self):
        return self.source.get_spectra()

    def get_spectra_one_value(self, spectrum_parameter: str):
        return self.source.get_spectra_one_value(spectrum_parameter)

    def get_exposure(self):
        return self.source.get_exposure()

    def set_source_type(self, source_type="Mono"):
        return self.source.set_source_type(source_type)

    def set_Flat_Field_Correction(self, apply_FFC=False):
        return self.detector.set_Flat_Field_Correction(apply_FFC)

    def set_visibility(self, ID: int, visible: bool = True):
        return self.setup.set_visibility(ID, visible)
