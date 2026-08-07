import artistlib as a
from pathlib import Path


project_folder = "$Xray(LibraryDir)/ExampleProjects/Dragon-CT.aRTist"
result_folder_pic = "$env(HOME) Pictures/"

result_folder_xrs = Path.home() / "Pictures"
load_folder_dict = Path(__file__).parent / "Test_tub3.dict"

# Build the connection to aRTist

# The ArtistProject class allows you to load projects, run aRTist simulations,
# and save the generated images
a.start_artist()
pro = a.ArtistProject()
pro.load_project(project_folder)
pro.run_project()
pro.save_img_project(result_folder_pic, "Pic1.tiff")

# The ArtistSetup class allows you to manipulate parts\project.
# For example, you can change the position of the detector, the source,
# or the parts in the scene.
setup = a.ArtistSetup()
# Example function calls
setup.detector_position(5, 9, -2)
setup.part_position_global(1, 10, 12, 20)
setup.part_orientation(1, angleX=90)

# The ArtistSource class allows you to define or load an X-ray spectrum (.xrs).
# You can either calculate a spectrum or load an existing one.
# It is also possible to load an X-ray tube definition from a .dict file.
src = a.ArtistSource()
src.set_spectra(
    "Tube3", 300, "W", 12, 0.3, "Cu", 0.5, "Cu", 0.5, "Cu", 0.5, "Be", 1.0, 12, 1, 1.0
)
src.cal_spectra()
src.cal_spectra(spec_name="Tube3_spc.xrs", dest_path=result_folder_xrs)

src.load_spectra((result_folder_xrs / "Tube3_spc.xrs"))
src.load_tube(load_folder_dict, "Test.xrs", result_folder_xrs)

# The ArtistDetector class allows you to change the detector geometry,
# including pixel count, detector size, and resolution.
#
# Relationships between parameters:
# - If you set pixel count and size, the resolution is calculated automatically.
# - If you set pixel count and resolution, the detector size is calculated.
# - If you set size and resolution, the pixel count is calculated.
#
# Notes:
# - If too many arguments are given, the function defaults to pixel and size.
# - You can specify either "size" or both "sizeX" and "sizeY".
det = a.ArtistDetector()
det.detector_geo(size=50, pixelX=100, pixelY=400)

# The ArtistAll class is a convenience wrapper that combines all
# previously mentioned classes into one interface.
Aall = a.ArtistAll()
Aall.load_project(project_folder)
Aall.part_orientation(1, angleX=-90)
Aall.detector_position(30)
Aall.detector_geo(sizeX=50, sizeY=60, res=0.5)
Aall.set_spectra(
    "Tube4", 600, "W", 12, 0.3, "Cu", 0.5, "Cu", 0.5, "Cu", 0.5, "Be", 1.0, 12, 1, 1.0
)
Aall.cal_spectra()
Aall.run_project()
