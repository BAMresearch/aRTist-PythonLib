import artistlib as a

# connect to aRTist (default: host='localhost', port=3658) 
rc = a.Junction()

# print aRTist's version number
ver = a.Junction.send(rc, '::aRTist::GetVersion full')
print(ver)

# - load a project
# - run the simulation
# - save the resulting projection from the image viewer
a.Junction.send(rc, 'FileIO::OpenAny $Xray(LibraryDir)/ExampleProjects/Schlumpfmark.aRTist')
a.Junction.send(rc, 'Engine::GoCmd')
ans = "Saved as: "
ans += a.Junction.send(rc, 'Modules::Invoke ImageViewer SaveFile [file join $env(HOME) Pictures/artistlib.tif] true')
print(ans)

# - load a project
# - run the simulation without viewing the result
# - transfer the final projection 
# - saving the projection image  >>>> This requires aRTist 2.12.7 or higher! <<<<
# - delete the images to release the memory
a.Junction.send(rc, 'FileIO::OpenAny $Xray(LibraryDir)/ExampleProjects/aRTist.aRTist')
a.Junction.send(rc, 'set imgList [Engine::Go]')
a.Junction.send(rc, 'RemoteControl::SendImage [lindex $imgList 0]')
a.Junction.save_image(rc, "transferred.tif")
a.Junction.send(rc, 'foreach i $imgList {$i Delete}')
print("Saved as: transferred.tif")