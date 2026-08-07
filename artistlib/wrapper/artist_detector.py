from .artist_send import ArtistSend


class ArtistDetector(ArtistSend):
    def _h(self, cmdx, cmdy, dependent_var, Xwidget_name, Ywidget_name):
        a = ""
        a += self.send("set ::Xsetup_private(DGauto) " + dependent_var)
        a += self.send(cmdx)
        a += self.send(cmdy)
        Xcmd_widget = (
            "::XDetector::UpdateGeometry $::XDetector::widget(" + Xwidget_name + ")"
        )
        a += self.send(Xcmd_widget)
        Ycmd_widget = (
            "::XDetector::UpdateGeometry $::XDetector::widget(" + Ywidget_name + ")"
        )
        a += self.send(Ycmd_widget)
        return a

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
    ) -> str:
        """Changes the detector geometry by modifying either:

        * Pixel count and detector size
        * Pixel count and resolution
        * Detector size and resolution

        The remaining parameter is calculated automatically.

        You can provide separate X and Y values for pixel count, detector size, and resolution.

        **Note:**

        * If too many parameters are provided, the resolution is recalculated automatically.
        * If `pixel=100`, `pixelX=50`, and `pixelY=70` are provided, the function uses `pixelX=50` and `pixelY=70`."""

        a = ""
        self._control_number(size, pixel, res, sizeX, sizeY, pixelX, pixelY, resX, resY)
        if pixelX is None or pixelY is None:
            pixelX = pixel
            pixelY = pixel

        elif pixelX is not None and pixelY is not None:
            pixel = 1

        if sizeX is None or sizeY is None:
            sizeX = size
            sizeY = size

        elif sizeX is not None and sizeY is not None:
            size = 1

        if resX is None or resY is None:
            resX = res
            resY = res

        elif resX is not None and resY is not None:
            res = 1

        if pixel is not None and size is not None:
            if pixelX == pixelY and sizeX == sizeY:
                a += self.send("set ::Xsetup(SquarePixel) 1")
            else:
                a += self.send("set ::Xsetup(SquarePixel) 0")

            a += self._h(
                "set ::Xsetup(DetectorPixelX) " + str(pixelX),
                "set ::Xsetup(DetectorPixelY) " + str(pixelY),
                "Resolution",
                "XPixel",
                "YPixel",
            )
            a += self._h(
                "set ::Xsetup_private(DGSx) " + str(sizeX),
                "set ::Xsetup_private(DGSy) " + str(sizeY),
                "Resolution",
                "XPixel",
                "YPixel",
            )

            return a

        if pixel is not None and res is not None:
            if pixelX == pixelY and resX == resY:
                a += self.send("set ::Xsetup(SquarePixel) 1")
            else:
                a += self.send("set ::Xsetup(SquarePixel) 0")

            a += self._h(
                "set ::Xsetup(DetectorPixelX) " + str(pixelX),
                "set ::Xsetup(DetectorPixelY) " + str(pixelY),
                "Size",
                "XSize",
                "YSize",
            )
            a += self._h(
                "set ::Xsetup_private(DGdx) " + str(resX),
                "set ::Xsetup_private(DGdy) " + str(resY),
                "Size",
                "XSize",
                "YSize",
            )

            return a

        if size is not None and res is not None:
            if sizeX == sizeY and resX == resY:
                a += self.send("set ::Xsetup(SquarePixel) 1")
            else:
                a += self.send("set ::Xsetup(SquarePixel) 0")

            a += self._h(
                "set ::Xsetup_private(DGSx) " + str(sizeX),
                "set ::Xsetup_private(DGSy) " + str(sizeY),
                "Pixel",
                "XPixel",
                "YPixel",
            )
            a += self._h(
                "set ::Xsetup_private(DGdx) " + str(resX),
                "set ::Xsetup_private(DGdy) " + str(resY),
                "Pixel",
                "XPixel",
                "YPixel",
            )

            return a

        if pixel is not None:
            if pixelX == pixelY:
                a += self.send("set ::Xsetup(SquarePixel) 1")
            else:
                a += self.send("set ::Xsetup(SquarePixel) 0")

            a += self._h(
                "set ::Xsetup(DetectorPixelX) " + str(pixelX),
                "set ::Xsetup(DetectorPixelY) " + str(pixelY),
                "Resolution",
                "XPixel",
                "YPixel",
            )

            return a

        if size is not None:
            if sizeX == sizeY:
                a += self.send("set ::Xsetup(SquarePixel) 1")
            else:
                a += self.send("set ::Xsetup(SquarePixel) 0")

            a += self._h(
                "set ::Xsetup_private(DGSx) " + str(sizeX),
                "set ::Xsetup_private(DGSy) " + str(sizeY),
                "Resolution",
                "XSize",
                "YSize",
            )

            return a

        if res is not None:
            if resX == resY:
                a += self.send("set ::Xsetup(SquarePixel) 1")
            else:
                a += self.send("set ::Xsetup(SquarePixel) 0")

            a += self._h(
                "set ::Xsetup_private(DGdx) " + str(resX),
                "set ::Xsetup_private(DGdy) " + str(resY),
                "Pixel",
                "XResolution",
                "YResolution",
            )
            return a

        return a

    def get_detector_pixel_count(self) -> tuple[float, float]:
        """Provides the pixel count of the detector. In x and y values."""
        a = self.send("::XDetector::GetPixelSize").split(" ")
        return float(a[0]), float(a[1])

    def get_detector_res(self) -> tuple[float, float]:
        """Provides the resolution of the detector. In x and y values."""
        a = self.send("::XDetector::GetResolution").split(" ")
        return float(a[0]), float(a[1])

    def get_detector_size(self) -> tuple[float, float]:
        """Provides the size of the detector. In x and y values."""
        a = self.send("::PartList::Invoke D GetSize").split(" ")
        return float(a[0]), float(a[1])

    def set_Flat_Field_Correction(self, apply_FFC: bool = False) -> str:
        """Turn the Flat Field Correction of the detector on or off."""
        if apply_FFC is False:
            return self.send("set ::Xdetector(FFCorrRun) 0")
        if apply_FFC is True:
            return self.send("set ::Xdetector(FFCorrRun) 1")
