from __future__ import annotations
import re
from .artistwrapper_all import ArtistAll


class Project:
    """This class manages project parts by creating corresponding Python objects and synchronizing them with the parts in aRTist."""

    def __init__(self):
        self.A = ArtistAll()
        self.matches = None

        self.parts_instances = []
        self._source = Source(self)
        self._detector = Detector(self)

    def in_parts(self, path: str) -> list[Part]:
        """Creates Python objects from the parts currently available in aRTist."""
        # wenn es ein neues Project ist (.aRTist) File dann werden alle ID und token ersetzt
        if path.endswith(".aRTist"):
            self.matches = None
            # for part in Part._instances:
            for part in self.parts_instances:
                part._destroyed = True
            # Part._instances.clear()
            self.parts_instances.clear()
        self.A.load_project(path)
        part_list = self._sync_parts()
        return part_list

    def _get_state(self) -> list[str]:
        """Retrieves the current part IDs and tokens from aRTist."""
        ans = self.A.send("::PartList::Get")
        pattern = r"(\S+)\s+\{Name(?:[^\{\}]|\{[^\}]*\})*?\s+Token\s+(\S+)"
        # pattern=r"(\S+)\s+\{Name\s+.*?Token\s+(\S+)"
        return re.findall(pattern, ans)

    def _sync_parts(self) -> list[Part]:
        """Creates Python objects for parts that do not yet have corresponding objects."""
        new_matches = self._get_state()
        matches = self.matches
        part_list = []
        if matches is None:
            for ID, token in new_matches:
                if ID == "D" or ID == "S":
                    continue
                p = Part(self, ID, token)
                part_list.append(p)

            self.matches = new_matches
            return part_list

        token_list_matches = {t[1] for t in matches}

        for ID, token in new_matches:
            if ID == "D" or ID == "S":
                continue

            if token not in token_list_matches:
                p = Part(self, ID, token)
                part_list.append(p)

        self.matches = new_matches
        return part_list

    def _update_state(self) -> None:
        """Updates part IDs and tokens."""
        new_matches = self._get_state()
        matches = self.matches

        if matches is None:
            self.matches = new_matches
            return

        if set(new_matches) != set(matches):
            self._sync_parts()

            # löscht die alten Parts anhand der token

            old_token = {t[1] for t in matches}
            new_token = {t[1] for t in new_matches}
            removed_tokens = old_token - new_token

            # for part in list(Part._instances):
            for part in list(self.parts_instances):
                if part.token in removed_tokens:
                    part._destroyed = True
                    self.parts_instances.remove(part)

    def clear_project(self) -> list[Part]:
        """Clears the virtual scene."""
        self.A.clear_project()
        for part in self.parts_instances:
            part._destroyed = True
            # Part._instances.clear()
        self.parts_instances.clear()
        return self._sync_parts()

    def update_project(self) -> None:
        """This function updates the state of all parts in this project."""
        for part in list(self.parts_instances):
            part.update_part()

    def source(self) -> Source:
        return self._source

    def detector(self) -> Detector:
        return self._detector


class Part:
    """This class creates a Python object based on the configuration in Artist."""

    def __init__(self, project_obj, ID, token):
        self._destroyed = False
        self.pro = project_obj
        self.pro.parts_instances.append(self)

        self.ID = ID
        self.token = token
        self.x = None
        self.y = None
        self.z = None
        self.x_ref = None
        self.y_ref = None
        self.z_ref = None
        self.angleX = None
        self.angleY = None
        self.angleZ = None
        self.material = None

        self._get_artist_values()
        self._old_part = {}
        self._sync_old()

    def update_part(self) -> str:
        """Applies modifications to Artist."""
        ans = ""
        self.pro._update_state()

        if (self.x, self.y, self.z) != (
            self._old_part["x"],
            self._old_part["y"],
            self._old_part["z"],
        ):
            ans += self.pro.A.part_position_global(int(self.ID), self.x, self.y, self.z)

        if (self.angleX, self.angleY, self.angleZ) != (
            self._old_part["angleX"],
            self._old_part["angleY"],
            self._old_part["angleZ"],
        ):
            ans += self.pro.A.part_orientation(
                int(self.ID), self.angleX, self.angleY, self.angleZ
            )

        if (self.x_ref, self.y_ref, self.z_ref) != (
            self._old_part["x_ref"],
            self._old_part["y_ref"],
            self._old_part["z_ref"],
        ):
            ans += self.pro.A.part_position_ref(
                int(self.ID), self.x_ref, self.y_ref, self.z_ref
            )

        if self.material != self._old_part["material"]:
            ans += self.pro.A.part_material(int(self.ID), self.material)

        self._get_artist_values()
        self._sync_old()
        return ans

    def delete_part(self) -> str:
        """Removes the specified part from Artist."""
        if self._destroyed:
            raise ReferenceError("Part already destroyed")

        self.pro._update_state()
        ans = self.pro.A.delete_part(int(self.ID))
        self.pro._update_state()
        self._destroyed = True
        return ans

    def _sync_old(self) -> None:
        self._old_part = {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "x_ref": self.x_ref,
            "y_ref": self.y_ref,
            "z_ref": self.z_ref,
            "angleX": self.angleX,
            "angleY": self.angleY,
            "angleZ": self.angleZ,
            "material": self.material,
        }

    def _get_artist_values(self) -> None:
        self.x, self.y, self.z = self.pro.A.get_part_global(int(self.ID))
        self.angleX, self.angleY, self.angleZ = self.pro.A.get_part_orientation(
            int(self.ID)
        )
        self.x_ref, self.y_ref, self.z_ref = self.pro.A.get_part_ref(int(self.ID))
        self.material = self.pro.A.get_part_material(int(self.ID))

    def __getattribute__(self, name):
        destroyed = object.__getattribute__(self, "_destroyed")

        if destroyed and name not in {
            "_destroyed",
            "__class__",
            "__repr__",
            "__str__",
        }:
            raise ReferenceError("Object was destroyed")

        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if hasattr(self, "_destroyed") and self._destroyed and name != "_destroyed":
            raise ReferenceError("Object was destroyed")

        object.__setattr__(self, name, value)


class Detector:
    """Provides an object-oriented interface for the aRTist detector."""

    def __init__(self, project_obj):
        self.pro = project_obj
        self.x = None
        self.y = None
        self.z = None
        self.angleX = None
        self.angleY = None
        self.angleZ = None

        self.size = None
        self.pixel = None
        self.res = None

        self.pixelX = None
        self.pixelY = None

        self.sizeX = None
        self.sizeY = None

        self.resX = None
        self.resY = None

        self._get_artist_values()
        self._old_part = {}
        self._sync_old()

    def _sync_old(self) -> None:
        self._old_part = {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "angleX": self.angleX,
            "angleY": self.angleY,
            "angleZ": self.angleZ,
            "size": self.size,
            "pixel": self.pixel,
            "res": self.res,
            "sizeX": self.sizeX,
            "sizeY": self.sizeY,
            "pixelX": self.pixelX,
            "pixelY": self.pixelY,
            "resX": self.resX,
            "resY": self.resY,
        }

    def _get_artist_values(self) -> None:
        self.x, self.y, self.z = self.pro.A.get_detector()
        self.angleX, self.angleY, self.angleZ = self.pro.A.get_detector_orientation()
        self._set_values_none()

    def _set_values_none(self) -> None:
        self.pixelX, self.pixelY = self.pro.A.get_detector_pixel_count()
        if self.pixelX != self.pixelY:
            self.pixel = None
        else:
            self.pixel = self.pixelX

        self.sizeX, self.sizeY = self.pro.A.get_detector_size()
        if self.sizeX != self.sizeY:
            self.size = None
        else:
            self.size = self.sizeX

        self.resX, self.resY = self.pro.A.get_detector_res()
        if self.resX != self.resY:
            self.res = None
        else:
            self.res = self.resX

    def update_detector(self) -> str:
        """Applies modifications to the detector configuration in Artist."""
        ans = ""

        if (self.x, self.y, self.z) != (
            self._old_part["x"],
            self._old_part["y"],
            self._old_part["z"],
        ):
            ans = ans + self.pro.A.detector_position(self.x, self.y, self.z)

        if (self.angleX, self.angleY, self.angleZ) != (
            self._old_part["angleX"],
            self._old_part["angleY"],
            self._old_part["angleZ"],
        ):
            ans = ans + self.pro.A.detector_orientation(
                self.angleX, self.angleY, self.angleZ
            )

        val = [
            self.size,
            self.pixel,
            self.res,
            self.sizeX,
            self.sizeY,
            self.pixelX,
            self.pixelY,
            self.resX,
            self.resY,
        ]

        keys_dict = [
            "size",
            "pixel",
            "res",
            "sizeX",
            "sizeY",
            "pixelX",
            "pixelY",
            "resX",
            "resY",
        ]
        # if any(attr is not None for attr in val):
        detector_send_dict = {}
        for key, value in zip(keys_dict, val):
            if value != self._old_part[key]:
                detector_send_dict[key] = value
        if len(detector_send_dict) > 0:
            ans = ans + self.pro.A.detector_geo(**detector_send_dict)

        self._get_artist_values()
        self._sync_old()
        # self._set_values_none()
        return ans


class Source:
    """Provides an object-oriented interface for the aRTist source."""

    def __init__(self, project_obj):
        self.pro = project_obj
        self.x = None
        self.y = None
        self.z = None
        self.angleX = None
        self.angleY = None
        self.angleZ = None

        self.Tube = None
        self.V = None
        self.TMaterial = None
        self.TAngle = None
        self.TThick = None
        self.FMaterial = None
        self.FThick = None
        self.F2Material = None
        self.F2Thick = None
        self.F3Material = None
        self.F3Thick = None
        self.WMaterial = None
        self.WThick = None
        self.Angle = None
        self.Transmission = None
        self.res = None

        self.exposure = None

        self._get_artist_values()
        self._old_part = {}
        self._sync_old()

    def _sync_old(self) -> None:
        self._old_part = {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "angleX": self.angleX,
            "angleY": self.angleY,
            "angleZ": self.angleZ,
            "Tube": self.Tube,
            "V": self.V,
            "TMaterial": self.TMaterial,
            "TAngle": self.TAngle,
            "TThick": self.TThick,
            "FMaterial": self.FMaterial,
            "FThick": self.FThick,
            "F2Material": self.F2Material,
            "F2Thick": self.F2Thick,
            "F3Material": self.F3Material,
            "F3Thick": self.F3Thick,
            "WMaterial": self.WMaterial,
            "WThick": self.WThick,
            "Angle": self.Angle,
            "Transmission": self.Transmission,
            "res": self.res,
            "exposure": self.exposure,
        }

    def _get_artist_values(self) -> None:
        self.x, self.y, self.z = self.pro.A.get_source()
        self.angleX, self.angleY, self.angleZ = self.pro.A.get_source_orientation()
        spectrum_dic = self.pro.A.get_spectra()
        self._set_values_none(spectrum_dic)
        self.exposure = self.pro.A.get_exposure()

    def _set_values_none(self, spec_dic) -> None:
        self.Tube = spec_dic["Name"] if spec_dic["Name"] != "{}" else None
        self.V = spec_dic["Voltage"] if spec_dic["Voltage"] != "{}" else None
        self.TMaterial = (
            spec_dic["TargetMaterial"] if spec_dic["TargetMaterial"] != "{}" else None
        )
        self.TAngle = (
            spec_dic["TargetAngle"] if spec_dic["TargetAngle"] != "{}" else None
        )
        self.TThick = (
            spec_dic["TargetThickness"] if spec_dic["TargetThickness"] != "{}" else None
        )
        self.FMaterial = (
            spec_dic["FilterMaterial"] if spec_dic["FilterMaterial"] != "{}" else None
        )
        self.FThick = (
            spec_dic["FilterThickness"] if spec_dic["FilterThickness"] != "{}" else None
        )
        self.F2Material = (
            spec_dic["Filter2Material"] if spec_dic["Filter2Material"] != "{}" else None
        )
        self.F2Thick = (
            spec_dic["Filter2Thickness"]
            if spec_dic["Filter2Thickness"] != "{}"
            else None
        )
        self.F3Material = (
            spec_dic["Filter3Material"] if spec_dic["Filter3Material"] != "{}" else None
        )
        self.F3Thick = (
            spec_dic["Filter3Thickness"]
            if spec_dic["Filter3Thickness"] != "{}"
            else None
        )
        self.WMaterial = (
            spec_dic["WindowMaterial"] if spec_dic["WindowMaterial"] != "{}" else None
        )
        self.WThick = (
            spec_dic["WindowThickness"] if spec_dic["WindowThickness"] != "{}" else None
        )
        self.Angle = spec_dic["AngleIn"] if spec_dic["AngleIn"] != "{}" else None
        self.Transmission = (
            spec_dic["Transmission"] if spec_dic["Transmission"] != "{}" else None
        )
        self.res = spec_dic["Resolution"] if spec_dic["Resolution"] != "{}" else None

    def update_source(self) -> str:
        """Applies modifications to the source configuration in Artist."""
        ans = ""
        if (self.x, self.y, self.z) != (
            self._old_part["x"],
            self._old_part["y"],
            self._old_part["z"],
        ):
            ans = ans + self.pro.A.source_position((self.x), (self.y), (self.z))

        if (self.angleX, self.angleY, self.angleZ) != (
            self._old_part["angleX"],
            self._old_part["angleY"],
            self._old_part["angleZ"],
        ):
            ans = ans + self.pro.A.source_orientation(
                self.angleX, self.angleY, self.angleZ
            )

        Arg = [
            self.Tube,
            self.V,
            self.TMaterial,
            self.TAngle,
            self.TThick,
            self.FMaterial,
            self.FThick,
            self.F2Material,
            self.F2Thick,
            self.F3Material,
            self.F3Thick,
            self.WMaterial,
            self.WThick,
            self.Angle,
            self.Transmission,
            self.res,
        ]

        keys = [
            "Tube",
            "V",
            "TMaterial",
            "TAngle",
            "TThick",
            "FMaterial",
            "FThick",
            "F2Material",
            "F2Thick",
            "F3Material",
            "F3Thick",
            "WMaterial",
            "WThick",
            "Angle",
            "Transmission",
            "res",
        ]

        # if any(elements is not None for elements in Arg):
        # old_value_list = list(self._old_part.values())
        for key, ar in zip(keys, Arg):
            # print(old_value_list[i+6])
            if ar != self._old_part[key]:  # 6 index offset
                ans = ans + self.pro.A.set_spectra(
                    self.Tube,
                    self.V,
                    self.TMaterial,
                    self.TAngle,
                    self.TThick,
                    self.FMaterial,
                    self.FThick,
                    self.F2Material,
                    self.F2Thick,
                    self.F3Material,
                    self.F3Thick,
                    self.WMaterial,
                    self.WThick,
                    self.Angle,
                    self.Transmission,
                    self.res,
                )
                break

        if self.exposure != self._old_part["exposure"]:
            ans = ans + self.pro.A.set_exposure(self.exposure)
        self._get_artist_values()
        self._sync_old()
        # self._set_values_none()
        return ans

    def cal_spectra(self, spec_name: str = None, dest_path: str = None) -> str:
        """Finally, recalculates the spectrum after all modifications have been applied."""
        ans = self.pro.A.cal_spectra(spec_name, dest_path)
        self._get_artist_values()
        self._sync_old()
        return ans
