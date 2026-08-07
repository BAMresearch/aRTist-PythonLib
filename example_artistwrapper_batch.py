import artistlib as a
from pathlib import Path

# connect to artist
# jct = a.Junction()
a.ArtistSend.set_global_batch(True)
w = a.ArtistAll()


# the following paths only work with load_project, load_save_project and save_img_project. It is used for this example.
# for your project use absolute paths!
# like for example: 'C:/Users/MaxMustermann/Pictures/'
project_folder = "$Xray(LibraryDir)/ExampleProjects/Dragon-CT.aRTist"
result_folder = "$env(HOME) Pictures/"

# first a minimal example
# this loads a project and automatically saves it
an = w.load_save_project(project_folder, result_folder, "Pic.tif")
print(an)
# you can do the same in smaller steps

w.load_project(project_folder)
w.run_project()
w.save_img_project(result_folder, "Pic2.tif")

# you can modify artist before you run the project with run_project

# you can change the Detector Geometry with Detector_Geo, which means changing either Pixel and Size or Pixel and Resolution or Size and Resolution
w.load_project(path_to_project=project_folder)
w.detector_geo(size=100, pixel=600)
w.run_project()

# you can also change the X and Y values separately for Pixel Size and Resolution
w.load_project(project_folder)
w.detector_geo(sizeX=50, sizeY=100, resX=0.5, resY=0.8)
w.run_project()

# Note: if you give too many arguments it automatically changes the Resolution.
# Note: if you give pixel= 100 and pixelX=50 and pixelY= 70 the function uses pixelX=50 and pixelY= 70.

# You can also change the position of the Detector and the Source.
# You give the X, Y, Z in global coordinates.

w.load_project(project_folder)
w.source_position(x=10, y=20, z=30)
w.detector_position(x=3, y=0, z=-30)
w.run_project()
# If you only give one or two values, the other value will not change.
# You can change the Spectrum by calling either set_spectra() or set_spectra2() for more Options.

w.load_project(project_folder)
w.set_spectra(
    Tube="Tube3",
    V=300,
    TMaterial="W",
    TAngle=12,
    TThick=0.3,
    FMaterial="Cu",
    FThick=0.5,
    WMaterial="Be",
    WThick=1.0,
    Angle=12,
    Transmission=1,
    res=1.0,
)
w.set_spectra(
    "Tube3", 300, "W", 12, 0.3, "Cu", 0.5, "Cu", 0.5, "Cu", 0.5, "Be", 1.0, 12, 1, 1.0
)

# Than you have to calculate the spectrum with cal_spectra.
# If you want to save the spectrum just give it the right name (.xrs) and the path.

w.cal_spectra()
# or
result_folder = Path.home() / "Pictures"

w.cal_spectra(spec_name="Tube3_spc.xrs", dest_path=result_folder)
# Note: this may take some time for high Voltage.

w.run_project()

# You can load a spectrum with load_spectra().

w.load_project(project_folder)
w.load_spectra((result_folder / "Tube3_spc.xrs"))
w.run_project()

# In artist you can create Tubes and save them as .dict files.
# load_tube reads this .dict and creates the spectrum in artist, so you can use it over and over again.

#'Test_tub3.dict' must be located in the same folder as this .py file for this example.
# you can specify an absolute path for your own project.

load_folder = Path(__file__).parent / "Test_tub3.dict"

w.load_project(project_folder)
w.load_tube(path_dict=load_folder, spec_name="Test_tub3.xrs", path_dest=result_folder)
w.load_spectra((result_folder / "Tube3_spc.xrs"))
w.run_project()

# You also can manipulate the position, orientation (rotation) and Material of a part (part or whole project).
w.load_project(project_folder)
w.part_position_global(ID=1, x=40, y=30, z=-10)
w.part_orientation(1, angleX=90, angleY=45, angleZ=10)
w.part_material(1, "Al")
w.run_project()

w.apply()
# Note: part_material(1,'Al') needs a material from the material list of artist.

# There are some more functions like: part_position_ref(ID) , get_part_orientation(ID), part_orientation(ID,angleX=None,angleY=None,angleZ=None).
# part_rotate(ID,system,alpha,axisX,axisY,axisZ), part_rotate_center(ID,alpha,x,y,z,Cx,Cy,Cz), get_part_global(ID)...
