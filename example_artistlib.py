
import artistlib as a

# connect to aRTist (default: host='localhost', port=3658) 
rc = a.Junction()

# single command
# print aRTist's version number
ver = a.Junction.send(rc, '::aRTist::GetVersion full')
print(ver)

# list of commands
# - load a project
# - run the simulation
# - save the resulting projection from the image viewer
cmds = [
  'FileIO::OpenAny $Xray(LibraryDir)/ExampleProjects/Schlumpfmark.aRTist',
  'Engine::GoCmd',
  'Modules::Invoke ImageViewer SaveFile [file join $env(HOME) Pictures/artistlib.tif] true']
a.Junction.send(rc, cmds)

# list of commands (2)
# - load a project
# - run the simulation without viewing the result
# - save the final projection 
# - delete the images to release the memory
cmds = [
  'FileIO::OpenAny $Xray(LibraryDir)/ExampleProjects/aRTist.aRTist',
  'set imgList [Engine::Go]',
  'Image::SaveFile [lindex $imgList 0] [file join $env(HOME) Pictures/artistlib2.tif] true',
  'foreach i $imgList {$i Delete}']
a.Junction.send(rc, cmds)
