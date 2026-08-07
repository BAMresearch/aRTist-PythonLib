import artistlib as a

project_folder = "$Xray(LibraryDir)/ExampleProjects/Dragon-CT.aRTist"
result_folder = "$env(HOME) Pictures/"

# Starts artist and creates a TCP connection
a.start_artist(start_UI=False)
# a.hide_ui()
# would also start artist
All = a.ArtistAll()
All.load_project(project_folder)
All.part_position_global(1, 20, 49, -3)
All.run_project()
a.show_ui()
All.save_img_project(result_folder, "Pic1.tiff")
# Saves the current state of the project
All.save_project()


# Closes artist via Junction and hard kills it if no Junction was found.
# Note: a hard kill can lead to problems when restarting.
a.close_artist()
