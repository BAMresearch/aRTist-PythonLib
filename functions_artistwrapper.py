import artistlib as a

# import wrapper as w
from pathlib import Path
# from artistlib.artistwrapper_all import ArtistAll

project_folder = "$Xray(LibraryDir)/ExampleProjects/Dragon-CT.aRTist"

result_folder_pic = "$env(HOME) Pictures/"

result_folder_xrs = Path.home() / "Pictures"
load_folder_dict = Path(__file__).parent / "Test_tub3.dict"


w = a.ArtistAll()

w.load_project(project_folder)
w.detector_geo(sizeX=300, sizeY=400, pixel=600)
old_detector_pos = w.get_detector()
print("det pos:", old_detector_pos)
w.detector_position(z=-70)
old_source_pos = w.get_source()
print("s pos", old_source_pos)
w.source_position(z=200)

part_pos = w.get_part_global(1)
print("obj pos:", part_pos)
part_pos_ref = w.get_part_ref(1)
print("obj pos ref", part_pos_ref)
w.part_position_global(1, x=10, y=5, z=30)
w.part_position_ref(1, x=0, y=0, z=160)

part_or = w.get_part_orientation(1)
print("obj or", part_or)
w.part_orientation(1, angleZ=90)
w.part_rotate(1, "world", 90, axisX=0, axisY=0, axisZ=90)
w.part_rotate_center(1, 90, 0, 0, 0, 0, 0, 0)

w.part_material(1, "Al")

# w.set_spectra('Tube3',300, 'W', 12, 0.3, 'Cu', 0.5, 'Be', 1.0, 12, 1, 1.0)
w.set_spectra(
    "Tube3", 300, "W", 12, 0.3, "Cu", 0.5, "Cu", 0.5, "Cu", 0.5, "Be", 1.0, 12, 1, 1.0
)
w.cal_spectra()
w.cal_spectra(spec_name="Tube3_spc.xrs", dest_path=result_folder_xrs)

w.load_spectra((result_folder_xrs / "Tube3_spc.xrs"))
w.load_tube(load_folder_dict, "Test.xrs", result_folder_xrs)


w.run_project()
w.save_img_project(result_folder_pic, "Pic3.tif")

w.set_exposure(15.5)

M = a.Material("Sand6")
M.density = 1.5
M.composition = "Si 0.47 O 0.53"
M.comment = "Test"
M.add()
