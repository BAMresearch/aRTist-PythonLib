"""Class to use CtScan Modul via Python"""

import logging

from .artist_send import ArtistSend

logger = logging.getLogger(__name__)


class CT(ArtistSend):
    """Provides access to the CTScan module through Python"""

    def run_CT(self) -> str:
        """Runs a CT scan."""
        self.send("::Modules::Run CtScan")
        a = ""
        a = self.send("::Modules::Module3::Execute")
        return a

    def set_CT(
        self,
        Angle: float = None,
        Steps: float = None,
        path: str = None,
        File_Name: str = None,
        File_Type: str = None,
        run_Feldkamp: bool = None,
        PixelType: str = None,
        Direction: str = None,
        Scattermode: str = None,
        ScatterIntervall: float = None,
    ) -> str:
        """Configures all CTScan parameters and validates the provided arguments.
        * File_Type must be either "{BAM CT}" or "TIFFs".
        * PixelType must be either "float" or "16bit".
        * Direction must be either "clockwise" or "counterclockwise".
        * Scattermode must be either "{force McRay}" or "{as configured}".
        **Note:** The Feldkamp reconstruction method is only available when `File_Type = "{BAM CT}"`.
        """
        self.send("::Modules::Run CtScan")

        self._control_number(Angle, Steps, ScatterIntervall)
        self._control_str(path, File_Name, PixelType, Direction)
        self._control_path(path)
        a = ""

        if Angle is not None:
            a += self.send("set ::Modules::Module3::CtScan(Angle) " + str(Angle))
        if Steps is not None:
            a += self.send("set ::Modules::Module3::CtScan(Steps) " + str(Steps))
        if path is not None:
            a += self.send("set ::Modules::Module3::CtScan(Directory) " + str(path))
        if File_Name is not None:
            a += self.send("set ::Modules::Module3::CtScan(File) " + str(File_Name))

        if File_Type == "{BAM CT}":
            a += self.send("set ::Modules::Module3::CtScan(Output) {BAM CT}")
            if run_Feldkamp:
                a += self.send("set ::Modules::Module3::CtScan(Feldkamp) 1")
            elif not run_Feldkamp:
                a += self.send("set ::Modules::Module3::CtScan(Feldkamp) 0")

        elif File_Type == "TIFFs":
            a += self.send("set ::Modules::Module3::CtScan(Output) TIFFs")
        elif File_Type is not None:
            logger.warning(
                "Wrong FileType: please use '{BAM CT}' or 'TIFFs'. Uses last set FileType."
            )

        if PixelType == "float":
            a += self.send("set ::Modules::Module3::CtScan(PixelType) float")
        elif PixelType == "16bit":
            a += self.send("set ::Modules::Module3::CtScan(PixelType) 16bit")
        elif PixelType is not None:
            logger.warning(
                "Wrong PixelType: please use 'float' or '16bit'. Uses last set PixelType."
            )

        if Direction == "clockwise":
            a += self.send("set ::Modules::Module3::CtScan(Direction) clockwise")
        elif Direction == "counterclockwise":
            a += self.send("set ::Modules::Module3::CtScan(Direction) counterclockwise")
        elif Direction is not None:
            logger.warning(
                "Wrong Direction: please use 'clockwise' or 'counterclockwise'. Uses last set Direction."
            )

        if Scattermode == "{force McRay}":
            a += self.send("set ::Modules::Module3::CtScan(ScatterMode) {force McRay}")
        elif Scattermode == "{as configured}":
            a += self.send(
                "set ::Modules::Module3::CtScan(ScatterMode) {as configured}"
            )
        elif Scattermode is not None:
            logger.warning(
                "Wrong Scattermode: please use '{force McRay}' or '{as configured}'. Uses last set Scattermode."
            )

        if ScatterIntervall is not None:
            a += self.send(
                "set ::Modules::Module3::CtScan(ScatterInterval) "
                + str(ScatterIntervall)
            )

        return a
