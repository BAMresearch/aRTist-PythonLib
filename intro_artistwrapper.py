import artistlib as a
from pathlib import Path

# connect to artist
# to use the wrapper
w = a.ArtistAll()

# paths for this example
# use absolut paths for your project!
project_folder = "$Xray(LibraryDir)/ExampleProjects/Dragon-CT.aRTist"
result_folder = "$env(HOME) Pictures/"

w.load_save_project(project_folder, result_folder, "Test_pic.tif")

# loads a project
w.load_project(project_folder)
# changes the global position of the part with the ID 1
w.part_position_global(ID=1, x=40, y=30, z=-10)
# changes the orientation of the part with the ID 1
w.part_orientation(ID=1, angleX=90, angleY=45, angleZ=10)
# changes the material of the the part with the ID 1
w.part_material(ID=1, Material="Al")
# changes the global position of the source
w.source_position(x=10, y=20, z=30)
# changes the global position of the detector
w.detector_position(x=3, y=0, z=-30)
# changes the geometry of the detector: Pixel, Size or Resolution
w.detector_geo(sizeX=50, sizeY=100, resX=0.5, resY=0.8)
# sets the spectrum
w.set_spectra(
    "Tube3", 300, "W", 12, 0.3, "Cu", 0.5, "Cu", 0.5, "Cu", 0.5, "Be", 1.0, 12, 1, 1.0
)
# calculates the spectrum
w.cal_spectra()
# runs the project
w.run_project()
# saves the images of the project
w.save_img_project(result_folder, "Test_pic2.tif")


load_folder = Path(__file__).parent
# loads a Tube from a .dict file, set the spectrum and calculates it then saves the spectrum in an .xrs.
w.load_tube(
    path_dict=(load_folder / "Test_tub3.dict"),
    spec_name="Test.xrs",
    path_dest=load_folder,
)
# loads a spectrum into artist
w.load_spectra(path=(load_folder / "Test.xrs"))

# there a more functions like: get_detector, get_source, get_part_global, get_part_orientation, get_part_ref, part_position_ref....
# look at example_artistwrapper.py for more explanations
