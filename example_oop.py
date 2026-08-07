import artistlib as a

path = "$Xray(LibraryDir)/ExampleProjects/Helix-CT.aRTist"
path1 = "$Xray(LibraryDir)/ExampleParts/Fun/Dragon.stl"

result_folder_pic = "$env(HOME) Pictures/"

# pro handles the project and creates the parts from aRTist
pro = a.Project()
pillow, patient, table, tomograph = pro.in_parts(path)

# changes the values in python
patient.x = -12
table.x = -15
pillow.x = 20
tomograph.x = -4

patient.angleX = 90
patient.angleZ = 90

# Sends the changes to aRTist.
pro.update_project()

Dragon = pro.in_parts(path1)[0]
Dragon.z = 30
pro.update_project()

Dragon.x = 16

# Updates only the single part.
Dragon.update_part()

# Deletes the part.
pillow.delete_part()

patient.y = 20

Dragon.z = 10

pro.update_project()

# Changes the detector.
det = pro.detector()
det.x = 50
det.angleX = 10
det.pixel = 5000
det.size = 250
det.update_detector()

# Changes the source.
src = pro.source()
src.angleX = 5
src.x = 19
src.V = 100
src.Tube = "Test_Name"
src.angleZ = 10
src.res = 20
src.update_source()
src.cal_spectra()

# Runs the simulation and saves the picture.
pro.A.run_project()
pro.A.save_img_project(result_folder_pic, "Pic_oop.tiff")
