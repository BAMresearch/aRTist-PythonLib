import artistlib as a

# connect to aRTist (default: host='localhost', port=3658) 
jct = a.Junction()

# print aRTist's version number
ver = jct.send('::aRTist::GetVersion full')
print(ver)

# - load a project
# - run the simulation
# - save the resulting projection from the image viewer
jct.send('FileIO::OpenAny $Xray(LibraryDir)/ExampleProjects/Schlumpfmark.aRTist')
jct.send('Engine::GoCmd')
ans = "Saved as: "
ans += jct.send('Modules::Invoke ImageViewer SaveFile [file join $env(HOME) Pictures/artistlib.tif] true')
print(ans)

# - load a project
# - run the simulation without viewing the result
# - transfer the final projection 
# - saving the projection image  >>>> This requires aRTist 2.12.7 or higher! <<<<
# - delete the images to release the memory
jct.send('FileIO::OpenAny $Xray(LibraryDir)/ExampleProjects/aRTist.aRTist')
jct.send('set imgList [Engine::Go]')
jct.send('RemoteControl::SendImage [lindex $imgList 0]')
jct.save_image("transferred.tif")
jct.send('foreach i $imgList {$i Delete}')
print("Saved as: transferred.tif")