from .artist_send import ArtistSend
import logging

logger = logging.getLogger(__name__)


class ArtistSetup(ArtistSend):
    """This class provides functions for controlling the aRTist setup, including moving, rotating, and querying the positions of parts, the detector, and the source."""

    def _coordinate_check(self, x, y, z, x_b, y_b, z_b) -> tuple[float, float, float]:
        one_value_None = False
        if x is None:
            x = x_b
            one_value_None = True
        if y is None:
            y = y_b
            one_value_None = True
        if z is None:
            z = z_b
            one_value_None = True

        if self.batch_flag and one_value_None:
            raise Exception(
                "When using batch mode, please specify all three coordinate values."
            )
        return x, y, z

    def get_coordinates(self, cmd: str, ID: int) -> tuple[float | None, float | None, float | None]:
        # p = self.send(cmd).split()
        # changed for live time no batching
        # throws an warning we need to change it
        if self.batch_flag:
            #logger.warning("When using batch mode, get_coordinates returns 0, 0, 0.")
            logger.info("While using batch mode,  get_coordinates returns None")
            return None, None, None

        p = self.send(cmd).split()
        if len(p) != 3:
            raise Exception(f"Unexpected response from Artist for ID {ID}: '{p}'")

        return float(p[0]), float(p[1]), float(p[2])

    def delete_part(self, ID: int) -> str:
        """Deletes a part with the specified ID."""
        self._control_number(ID)
        a = self.send("::PartList::Delete " + str(ID))
        return a

    def get_part_global(self, ID: int) -> tuple[float, float, float]:
        """Returns the global position of a part. **Note:** Part IDs are integer values starting at 1. The first created part has ID 1, the second has ID 2, and so on."""
        self._control_number(ID)
        return self.get_coordinates(
            "::PartList::Invoke " + str(ID) + " GetPosition", ID
        )

    def part_position_global(
        self, ID: int, x: float = None, y: float = None, z: float = None
    ) -> str:
        """Sets the global position of a part.
        **Note:** Coordinates that are not provided remain unchanged."""

        self._control_number(ID, x, y, z)

        x_b, y_b, z_b = self.get_part_global(ID)
        x, y, z = self._coordinate_check(x, y, z, x_b, y_b, z_b)

        a = self.send(
            "::PartList::Invoke "
            + str(ID)
            + " SetPosition "
            + str(x)
            + " "
            + str(y)
            + " "
            + str(z)
        )
        return a

    def get_part_ref(self, ID: int) -> tuple[float, float, float]:
        """Returns the reference position of a part."""
        self._control_number(ID)
        return self.get_coordinates("::PartList::Invoke " + str(ID) + " GetRefPos", ID)

    def part_position_ref(
        self, ID: int, x: float = None, y: float = None, z: float = None
    ) -> str:
        """Sets the reference position of a part.
        **Note:** Coordinates that are not provided remain unchanged."""
        self._control_number(ID, x, y, z)
        x_b, y_b, z_b = self.get_part_ref(ID)
        x, y, z = self._coordinate_check(x, y, z, x_b, y_b, z_b)

        a = self.send(
            "::PartList::Invoke "
            + str(ID)
            + "  SetRefPos "
            + str(x)
            + " "
            + str(y)
            + " "
            + str(z)
        )
        return a

    def group_transform_rotate(
        self,
        IDs: list,
        alpha: float,
        x: float,
        y: float,
        z: float,
        Cx: float,
        Cy: float,
        Cz: float,
    ) -> str:
        """Rotates a group of parts specified by a list of IDs."""
        self._control_number(alpha, x, y, z, Cx, Cy, Cz)
        if IDs == "parts":
            ID_string = IDs
        else:
            if not isinstance(IDs, list):
                IDs = [IDs]
            ID_string = "{"
            for ID in IDs:
                self._isnumber(ID)
                ID_string += str(ID) + " "
            ID_string += "}"

        return self.send(
            "::PartList::Invoke "
            + ID_string
            + " Rotate world "
            + str(alpha)
            + " "
            + str(x)
            + " "
            + str(y)
            + " "
            + str(z)
            + " "
            + '"'
            + str(Cx)
            + " "
            + str(Cy)
            + " "
            + str(Cz)
            + '"'
        )

    ### Oriantation of the Object (Rotation)
    def group_transform_translation(
        self,
        IDs: list,
        x: float,
        y: float,
        z: float,
    ) -> str:
        """Moves a group of parts specified by a list of IDs."""
        self._control_number(x, y, z)
        if IDs == "parts":
            ID_string = IDs
        else:
            if not isinstance(IDs, list):
                IDs = [IDs]
            ID_string = "{"
            for ID in IDs:
                self._isnumber(ID)
                ID_string += str(ID) + " "
            ID_string += "}"

        return self.send(
            "::PartList::Invoke "
            + ID_string
            + " Translate world "
            + str(x)
            + " "
            + str(y)
            + " "
            + str(z)
        )

    def get_part_orientation(self, ID: int) -> tuple[float, float, float]:
        """Returns the orientation of a part."""
        self._control_number(ID)
        return self.get_coordinates(
            "::PartList::Invoke " + str(ID) + " GetOrientation", ID
        )

    def part_orientation(
        self, ID: int, angleX: float = None, angleY: float = None, angleZ: float = None
    ) -> str:
        """Sets the orientation of a part.
        **Note:** Values that are not provided remain unchanged."""

        self._control_number(ID, angleX, angleY, angleZ)

        x_b, y_b, z_b = self.get_part_orientation(ID)
        angleX, angleY, angleZ = self._coordinate_check(
            angleX, angleY, angleZ, x_b, y_b, z_b
        )

        a = self.send(
            "::PartList::Invoke "
            + str(ID)
            + " SetOrientation "
            + str(angleX)
            + " "
            + str(angleY)
            + " "
            + str(angleZ)
        )
        return a

    def part_rotate(
        self,
        ID: int,
        system: str,
        alpha: float,
        axisX: float,
        axisY: float,
        axisZ: float,
    ) -> str:
        """Rotates a part around the specified x, y, or z axis by the angle `alpha`. The coordinate system must be specified as either `"world"` or `"object"`"""
        self._control_number(ID, alpha, axisX, axisY, axisZ)
        self._control_str(system)
        if not (system == "world" or system == "object"):
            raise Exception("System should be 'world' or 'part not:'", system)
        a = self.send(
            " ::PartList::Invoke "
            + str(ID)
            + " Rotate "
            + str(system)
            + " "
            + str(alpha)
            + " "
            + str(axisX)
            + " "
            + str(axisY)
            + " "
            + str(axisZ)
        )

        return a

    # funktioniert im Moment nicht: "world" und "" um CX CY CZ
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
        """Rotates a part around a specified center point using the given rotation axis and angle."""
        self._control_number(ID, alpha, x, y, z, Cx, Cy, Cz)
        a = self.send(
            "::PartList::Invoke "
            + str(ID)
            + " Rotate world "
            + str(alpha)
            + " "
            + str(x)
            + " "
            + str(y)
            + " "
            + str(z)
            + " "
            + '"'
            + str(Cx)
            + " "
            + str(Cy)
            + " "
            + str(Cz)
            + '"'
        )

        return a

    def part_material(self, ID: int, Material: str) -> str:
        """Assigns a material to a part. **Note:** The material must already exist in aRTist."""
        self._control_number(ID)
        self._control_str(Material)

        a = self.send("::PartList::Set " + str(ID) + " Material " + str(Material))
        return a

    def get_part_material(self, ID: int) -> str:
        """Returns the material of the part with the specified ID."""
        self._control_number(ID)
        a = self.send("::PartList::Get " + str(ID) + " Material")
        return a

        ### Position von Detector/Source ändern

    def get_detector(self) -> tuple[float, float, float]:
        """Returns the current detector position as x, y, z coordinates."""
        return self.get_coordinates("Detector GetPosition", "D")

    def get_source(self) -> tuple[float, float, float]:
        """Returns the current source position as x, y, z coordinates."""
        return self.get_coordinates("Source GetPosition", "S")

    def source_position(self, x: float = None, y: float = None, z: float = None) -> str:
        """Sets the source position."""
        self._control_number(x, y, z)
        x_b, y_b, z_b = self.get_source()
        x, y, z = self._coordinate_check(x, y, z, x_b, y_b, z_b)

        a = self.send("Source SetPosition " + str(x) + " " + str(y) + " " + str(z))
        return a

    def detector_position(
        self, x: float = None, y: float = None, z: float = None
    ) -> str:
        """Sets the detector position."""
        self._control_number(x, y, z)
        x_b, y_b, z_b = self.get_detector()
        x, y, z = self._coordinate_check(x, y, z, x_b, y_b, z_b)

        a = self.send("Detector SetPosition " + str(x) + " " + str(y) + " " + str(z))
        return a

    def get_source_orientation(self) -> tuple[float, float, float]:
        """Returns the source orientation."""
        return self.get_coordinates("Source GetOrientation", "S")

    def source_orientation(
        self, x: float = None, y: float = None, z: float = None
    ) -> str:
        """Sets the source orientation."""
        self._control_number(x, y, z)
        x_b, y_b, z_b = self.get_source_orientation()
        x, y, z = self._coordinate_check(x, y, z, x_b, y_b, z_b)
        a = self.send("Source  SetOrientation " + str(x) + " " + str(y) + " " + str(z))

        return a

    def get_detector_orientation(self) -> tuple[float, float, float]:
        """Returns the detector orientation."""
        return self.get_coordinates("Detector GetOrientation", "D")

    def detector_orientation(
        self, x: float = None, y: float = None, z: float = None
    ) -> str:
        """Sets the detector orientation."""
        self._control_number(x, y, z)
        x_b, y_b, z_b = self.get_detector_orientation()
        x, y, z = self._coordinate_check(x, y, z, x_b, y_b, z_b)
        a = self.send("Detector SetOrientation " + str(x) + " " + str(y) + " " + str(z))

        return a

    def get_size(self, ID: int) -> tuple[float, float, float]:
        """Gets the size of the part with the specified ID."""

        self._control_number(ID)
        p = self.send("::PartList::Invoke " + str(ID) + " GetSize").split(" ")
        if len(p) != 3:
            raise Exception(f"Unexpected response from Artist for ID {ID}: '{p}'")

        return float(p[0]), float(p[1]), float(p[2])

    def set_size(self, ID: int, x: float, y: float, z: float) -> str:
        """Sets the size of the part with the specified ID."""
        self._control_number(ID, x, y, z)
        bx, by, bz = self.get_size(ID)
        x, y, z = self._coordinate_check(x, y, z, bx, by, bz)
        a = self.send(
            "::PartList::Invoke "
            + str(ID)
            + " SetSize "
            + str(x)
            + " "
            + str(y)
            + " "
            + str(z)
        )
        return a

    def set_visibility(self, ID: int, visible: bool = True) -> str:
        """Sets the visibility of a part."""
        self._control_number(ID)
        if visible:
            return self.send("::PartList::Set " + str(ID) + " Visible on")
        if not visible:
            return self.send("::PartList::Set " + str(ID) + " Visible off")
