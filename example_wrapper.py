import artistlib as a
from pathlib import Path

project_folder = "$Xray(LibraryDir)/ExampleProjects/Dragon-CT.aRTist"
result_folder = Path.home() / "Pictures"
# Starts aRTist and activates remote control.
# a.ArtistAll() also starts aRTist and activates remote control.
a.start_artist()
wrapper = a.ArtistAll()
# Loads a project (.artist) or a part (.stl) based on the provided path.
wrapper.load_project(project_folder)

# Translation of the part with the given ID, to the given coordinates.
#
# part_orientation rotates the part with the given ID
# part_material sets the material of the part with the given ID.
wrapper.part_position_global(ID=1, x=10, y=10, z=-10)
wrapper.part_position_global(ID=1, x=30)
wrapper.part_orientation(1, angleX=90, angleY=45, angleZ=10)
wrapper.part_material(1, "Al")

# Translation of the detector.
# Rotation of the detector.
# detector_geo can change the Detector Geometry with Detector_Geo, which means changing either Pixel and Size or Pixel and Resolution or Size and Resolution.
wrapper.detector_position(x=30, y=20)
wrapper.detector_orientation(x=5)
wrapper.detector_geo(size=100, pixel=600)

# Translation of the source.
# Rotation of the source.
wrapper.source_position(z=155)
wrapper.source_orientation(x=1)

# Sets the individual values of the spectrum.
# Calculates the spectrum and saves it to a path.
wrapper.set_spectra(
    "Tube3", 300, "W", 12, 0.3, "Cu", 0.5, "Cu", 0.5, "Cu", 0.5, "Be", 1.0, 12, 1, 1.0
)
wrapper.cal_spectra(spec_name="Tube3_spc.xrs", dest_path=result_folder)

#
# Loads a dict file and extracts spectrum values and calculates the spectrum.
# Loads an already calculated spectrum.
load_folder = Path(__file__).parent / "Test_tub3.dict"
wrapper.load_tube(
    path_dict=load_folder, spec_name="Test_tub3.xrs", path_dest=result_folder
)
wrapper.load_spectra((result_folder / "Tube3_spc.xrs"))

# Runs the current project, starts the simulation.
# Saves the image to a path with a given name.
wrapper.run_project()
wrapper.save_img_project(result_folder, "Pic2.tif")

# Deletes a part with the given ID.
# Resets artist.
wrapper.delete_part(ID=1)
wrapper.clear_project()

# closes aRTist.
# a.close_artist()
