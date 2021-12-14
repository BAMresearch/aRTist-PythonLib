# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:23:40 2020

@author: dschumac
"""
import socket

def connect(Host, Port, timeout):
    S = socket.socket()             # Create socket (for TCP)
    S.connect((Host, Port))         # Connect to aRTist
    S.settimeout(timeout)
    return S

def send(socket, x):
    total = ""
    for i in range(len(x)):
       # print(i+1, "of", len(x), " commands send")  
       # print(x[i])
        socket.send(x[i].encode())
        total = total + listen(1)
    return total

def listen(socket, buffer_size, timeout, command_no):
    total = ""
    stop = False
    if (command_no == 0):
        socket.settimeout(0.2)
    while (not stop):# and ("SUCCESS" not in total) and ("ERROR" not in total):     # Solange server antwortet und nicht "SUCCESS" enthält
        try:
            msg = socket.recv(buffer_size).decode()                                     # 
        except socket.timeout as e:
            err = e.args[0]
            if err == "timed out":
                print("Timeout\n")
                stop = True
                continue
        else:
            if ("SUCCESS" in msg):
                total = total + msg
               # print(msg)
                stop = True
                continue
            elif ("ERROR" in msg):
                total = total + msg
               # print(msg)
                stop = True
                global error
                error = error + 1 
                continue
            else:
               # print(msg)
                if (command_no == 0):
                    print(msg)
                total = total + msg
    socket.settimeout(timeout)
    return total

''' aRTist spezifische Kommandos '''
def open_scence(Path):
    STR = ["""FileIO::OpenAny """+ Path +""";
"""]
    return STR

def setup_detector(x, y, px):
    STR = ["""set ::Xdetector(Type) {flat panel};
""","""set ::Xsetup_private(DGauto) {Size};
""","""set ::Xsetup(DetectorPixelX) """+ str((int(x))) +""";
""","""set ::Xsetup(DetectorPixelY) """+ str((int(y))) +""";
""","""set ::Xsetup_private(DGdx) """+ str(px) +""";
""","""set ::Xsetup_private(DGdy) """+ str(px) +""";
""","""set ::Xdetector(AutoD) {max};
""","""set ::Xdetector(RefGV) 50000;
""","""::XDetector::UpdateGeometry 1;
"""]
    return STR

def setup_source(pos, kV, mA):
    STR = ["""set ::Xsetup(SourceSampling) {point};
""","""set ::Xsource(Exposure) """+ str(mA) +""";
""","""set ::Xsource(Tube) {Mono};
""","""set ::Xsource(Voltage) """+ str(kV) +""";
""","""::PartList::Invoke S SetPosition 0 0 """+ str(pos) +""";
""","""::PartList::Invoke S SetRefPos 0 0 """+ str(pos) +""";
""","""set ::Xdetector(FFCorrRun) 0;
""","""XDetector::FFCorrClearCmd;
""","""::XSource::spectrumOK;
"""]  # set ::Engine::RenderPreview 0;
    return STR

def setup_FFcorr():
    STR = ["""::XDetector::FFCorrGenCmd;
"""]
    return STR

def create_sphere(R):
    R = 2 * R
    STR = ["""::Modules::Run Solid;
""","""set ::Modules::Module7::Solid(Type) {ellipsoid};
""","""set ::Modules::Module7::Solid(Equilateral) 1;
""","""set ::Modules::Module7::Solid(X) """+ str(R) +""";
""","""set ::Modules::Module7::Solid(PhiResolution) 80;
""","""set ::Modules::Module7::Solid(ThetaResolution) 80;
""","""set ::Modules::Module7::Solid(GridEllipsoid) 1;
""","""set ::Modules::Module7::Solid(VolumeCorrect) 1;
"""]
    return STR

def set_material(ID, mat):
    STR = ["""::PartList::Set """+ str(ID) +""" Material """+ mat +""";
"""]
    return STR

def set_position(ID, x, y, z):
    STR = ["""::PartList::Invoke """+ str(ID) +""" SetPosition """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
""","""::PartList::Invoke """+ str(ID) +""" SetRefPos """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
"""]
    return STR

def translate(ID, x, y, z):
    STR = ["""::PartList::Invoke """+ str(ID) +""" Translate world """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
"""]
    return STR


def aRTist_set_vis_AllParts(state): #state = "on"/"off"
    STR = ["""::PartList::SetVisibility """+state+""";
           """] #::PartList::Set parts Visible off;
    return STR

def aRTist_set_vis(ID, state):
    STR = ["""::PartList::Set """+str(ID)+""" Visible """+state+""";
           """]
    return STR

def resize(ID, size):
    STR = ["""::PartList::Invoke """+str(ID)+""" SetSize """+str(size)+""" """+str(size)+""" """+str(size)+""";
"""]
    return STR

def make_image():
    STR = ["""::Engine::StartStopCmd;
"""]
    return STR

def save_image(Path):
    STR = ["""::Modules::Execute ImageViewer Save16bit """+ Path +""" 1;
"""]
    return STR

#def delete(O1, O2):
#    STR = ""
#    while (O1 <= O2):
#        STR = STR + """::PartList::Delete """+ str(O1)+""";
#"""
#        O1 = O1 + 1
#    return STR

def fire():
    STR = ["""::Modules::Module7::GenerateCmd;
"""]
#::Modules::Module7::Close;"
    return STR            

# def aRTist_SETUP_CT(angle, steps, OutDir, OutName, OutFormat, PType, RunFDK, OnlySelObj, Direction, Scat, ScatInt):
#     #OutFormat ({BAM CT}, TIFFs)
#     #PType (16bit, float)
#     #Direction (clockwise, counterclockwise)
#     #Scat (off, McRay)
#     STR = ["""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Angle) """+ str(angle) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Steps) """+ str(steps) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Directory) """+ OutDir +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(File) """+ OutName +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Output) """+ str(OutFormat) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(PixelType) """+ str(PType) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Feldkamp) """+ str(RunFDK) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Selected) """+ str(OnlySelObj) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Direction) """+ str(Direction) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(ScatterMode) """+ Scat +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(ScatterInterval) """+ str(ScatInt) +""";
#            """]
#     return STR

# def aRTist_SETUP_FDK(VType, Interp, OutFormat):
#     #VType (8bit, 16bit, 32bit, float)
#     #OutFormat ({BAM CT}, VTK, RAW)
#     STR = ["""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(VoxelType) """+ str(VType) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Interpolate) """+ str(Interp) +""";
#            ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(FileType) """+ str(OutFormat) +""";
#            """]
#     return STR

# def aRTist_Run_CT():
#     STR = ["""::Modules::Module""" +str(CTModNo)+"""::Execute; 
#            """]
#     return STR

################# Extract results from aRTist answer string ###################
def Extract_resultStr(aRTist_string):
    startI = aRTist_string.find('RESULT ') + 7
    endI = aRTist_string.find('\r\nSUCCESS', startI)
    result = aRTist_string[startI:endI]
    return result


