from .artist_send import ArtistSend
import os
import shutil
import re

import logging


logger = logging.getLogger(__name__)


class ArtistSource(ArtistSend):
    """This class provides functions for modifying the source."""

    List_content = [
        "Name",
        "Voltage",
        "TargetMaterial",
        "TargetAngle",
        "TargetThickness",
        "FilterMaterial",
        "FilterThickness",
        "Filter2Material",
        "Filter2Thickness",
        "Filter3Material",
        "Filter3Thickness",
        "WindowMaterial",
        "WindowThickness",
        "AngleIn",
        "Transmission",
        "Resolution",
    ]
    STRING_FIELDS = {
        "Name",
        "WindowMaterial",
        "TargetMaterial",
        "FilterMaterial",
        "Filter2Material",
        "Filter3Material",
    }

    def load_spectra(self, path: str) -> str:
        """Loads a spectrum from an `.xrs` file into aRTist."""
        a = self.load_file(path)
        return a

    def set_exposure(self, exposure: float) -> str:
        """Sets the exposure value in aRTist."""
        self._control_number(exposure)
        a = self.send("set ::Xsource(Exposure) " + str(exposure))
        return a

    def get_exposure(self):
        return float(self.send("set ::Xsource(Exposure)"))

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
    ) -> str:
        """Sets individual spectrum parameters."""
        Arg = [
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
        ]

        cmd_list = [
            "set ::Xsource(Tube) ",
            "set ::Xsource(Voltage) ",
            "set ::Xsource(TargetMaterial) ",
            "set ::Xsource(TargetAngle) ",
            "set ::Xsource(TargetThickness) ",
            "set ::Xsource(FilterMaterial) ",
            "set ::Xsource(FilterThickness) ",
            "set ::Xsource(Filter2Material) ",
            "set ::Xsource(Filter2Thickness) ",
            "set ::Xsource(Filter3Material) ",
            "set ::Xsource(Filter3Thickness) ",
            "set ::Xsource(WindowMaterial) ",
            "set ::Xsource(WindowThickness) ",
            "set ::Xsource(AngleIn) ",
            "set ::Xsource(Transmission) ",
            "set ::Xsource(Resolution) ",
        ]

        a = ""
        self._control_number(
            V,
            TAngle,
            TThick,
            FThick,
            WThick,
            Angle,
            Transmission,
            res,
            F2Thick,
            F3Thick,
        )
        self._control_str(Tube, TMaterial, FMaterial, WMaterial, F2Material, F3Material)
        p = 0
        for value in cmd_list:
            if Arg[p] is not None:
                ar = str(Arg[p])
                a += self.send(value + ar)
            p = p + 1

        return a

    def _copy_and_rename(self, src_path: str, dest_path: str, new_name: str) -> None:
        try:
            # Datei kopieren
            copied_file = shutil.copy(src_path, dest_path)

            # Neuer kompletter Pfad mit neuem Namen
            new_path = self._replace_slashes(os.path.join(dest_path, new_name))

            # rename
            shutil.move(copied_file, new_path)

        except Exception:
            logger.exception("Unexpected error while copying and renaming file")
            raise

    def cal_spectra(
        self, spec_name: str = None, dest_path: str = None, reduce_number_bins=False
    ):
        """Calculates a spectrum and optionally saves it.

        Note:
        * If no output path is specified, the spectrum is calculated but not saved.
        * Spectrum calculation may take longer for high-voltage configurations.
        * Set reduce_number_bins to True to reduce the number of bins in the spectra to a maximum of 128 bins.
        """
        a = ""
        if self.batch_flag:
            if spec_name is not None or dest_path is not None:
                logger.warning(
                    "When using batch mode, no storage location can be specified for the calculation."
                )
            a += self.send("::XSource::ComputeSpectrum")
            if reduce_number_bins is True:
                a += self.send("::XSource::CheckSpectrum")
            return a

        # we need to set the timeout high, because the calculation can take a long time for high voltage

        old_timeout = self.jct.timeout
        self.jct.timeout = 1000
        self.jct.S.settimeout(self.jct.timeout)
        try:
            path1 = self.send("::XSource::ComputeSpectrum").strip("\n")
            if path1 == "Timeout" or path1 == "{}":
                raise RuntimeError(
                    f"Spectrum calculation failed (timeout: {self.jct.timeout}s) or unexpected error."
                )
            a += path1
            if reduce_number_bins is True:
                a += self.send("::XSource::CheckSpectrum")
        finally:
            self.jct.timeout = old_timeout
            self.jct.S.settimeout(self.jct.timeout)

        if dest_path is not None:
            dest_path = self._control_path(dest_path)[0]
            self._path_exist(dest_path)
            self._control_str(dest_path)

            if spec_name is not None:
                self._control_str(spec_name)

            self._copy_and_rename(
                src_path=path1, dest_path=dest_path, new_name=spec_name
            )

        return a

    def _read_file(self, path: str) -> None:
        with open(path, "r") as f:
            return f.read()

    def _get_content_dict(self, content: str) -> list:

        list_spectrum = []

        for el in self.List_content:
            match = re.search(rf"\b{el}\b\s+([^\s]+)", content)

            if el in self.STRING_FIELDS:
                if match:
                    list_spectrum.append(match.group(1))
                else:
                    list_spectrum.append(None)

            else:
                if match:
                    list_spectrum.append(float(match.group(1)))
                else:
                    list_spectrum.append(None)
        return list_spectrum

    def load_tube(self, path_dict: str, spec_name: str, path_dest: str) -> None:
        """Loads a `.dict` file, applies the spectrum settings, and calculates the resulting spectrum."""
        path_dict, path_dest = self._control_path(path_dict, path_dest)
        self._path_exist(path_dict, path_dest)
        self._control_str(path_dict, spec_name, path_dest)
        try:
            content = self._read_file(str(path_dict))

            values_spec = self._get_content_dict(content)

            self.set_spectra(*values_spec)

            self.cal_spectra(spec_name, str(path_dest))
        except Exception:
            logger.exception("Unexpected error while loading tube data")
            raise

    def get_spectra(self):
        """Gets the current spectrum and returns it as a dict."""
        spectrum_dic = {}
        for el in self.List_content:
            out = self.send("array get Xsource " + el).split(" ")[1].strip("\n")
            if el in self.STRING_FIELDS:
                spectrum_dic[el] = out
                continue
            if out != "{}" and out != "":
                spectrum_dic[el] = float(out)
                continue
            spectrum_dic[el] = out

        return spectrum_dic

    def get_spectra_one_value(self, spectrum_parameter):
        """Returns only the specified spectrum parameter.
        **Note**:
        * Possible values are:
        'Name', 'Voltage', 'TargetMaterial', 'TargetAngle', 'TargetThickness', 'FilterMaterial', 'FilterThickness', 'Filter2Material', 'Filter2Thickness', 'Filter3Material', 'Filter3Thickness', 'WindowMaterial', 'WindowThickness', 'AngleIn', 'Transmission', 'Resolution'.
        """

        self._control_str(spectrum_parameter)

        if spectrum_parameter in self.List_content:
            out = (
                self.send("array get Xsource " + spectrum_parameter)
                .split(" ")[1]
                .strip("\n")
            )
            if spectrum_parameter in self.STRING_FIELDS:
                return out
            if out != "{}" and out != "":
                return float(out)
            return out
        else:
            logger.warning("Wrong spectrum_parameter please use: ", self.List_content)

    def set_source_type(self, source_type: str = "Mono"):
        """Sets the type of the source.
        **Note**
        * source_type has to be either "Mono" or "General".
        """
        if source_type not in ("Mono", "General"):
            logger.warning("source_type must be either 'Mono' or 'General'")
            return ""

        return self.send(f"set ::Xsource(Tube) {source_type}")
